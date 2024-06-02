import uuid
from django.utils import timezone
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from djmoney.models.fields import MoneyField
from djmoney.money import Money

from config import settings
from groups.models import Department

from inventory.models import Item


class Requisition(models.Model):
    """Modèle représentant une demande de fonds."""
    STATUS_DRAFT = "draft"
    STATUS_SUBMITTED = "submitted"
    STATUS_CHOICES = (
        (STATUS_DRAFT, "Brouillon"),
        (STATUS_SUBMITTED, "Soumise"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, verbose_name="Demandeur")
    narration = models.CharField(max_length=250, verbose_name="Description")
    amount = MoneyField(max_digits=19, decimal_places=2, default_currency='USD', verbose_name="Montant (USD)")
    exchange_rate = models.DecimalField(max_digits=11, decimal_places=4, default=1, verbose_name="Taux de change") 
    amount_converted = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True, verbose_name="Montant converti (CDF)")
    cost_center = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, verbose_name="Centre de coût") 
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_DRAFT, verbose_name="Statut")
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_requisitions', verbose_name="Approuvé par")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    modified_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")

    class Meta:
        ordering = ('-modified_at',)
        constraints = [
            models.UniqueConstraint(fields=['requester', 'narration'], name='unique_request_per_user') 
        ]
        verbose_name = "Demande de fonds"
        verbose_name_plural = "Demandes de fonds"

    def __str__(self):
        return self.narration

    def save(self, *args, **kwargs):
        if self.status == self.STATUS_SUBMITTED and not self.amount_converted:
            self.amount_converted = self.amount.amount * self.exchange_rate 
        super().save(*args, **kwargs)

    @property
    def converted_amount_display(self):
        """Affiche le montant converti en utilisant MoneyField pour le formatage."""
        return Money(self.amount_converted, 'CDF') if self.amount_converted else None

    def get_absolute_url(self):
        return reverse("requisition:detail", args=[str(self.id)])


class Review(models.Model):
    REVIEW_PENDING = 'pending'
    REVIEW_APPROVED = 'approved'
    REVIEW_REJECTED = 'rejected'
    REVIEW_CHOICES = [
        (REVIEW_PENDING, 'En attente'),
        (REVIEW_APPROVED, 'Approuvée'),
        (REVIEW_REJECTED, 'Rejetée'),
    ]

    requisition = models.ForeignKey(Requisition, on_delete=models.CASCADE, related_name='reviews', verbose_name="Demande")
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Réviseur")
    level = models.PositiveIntegerField(verbose_name="Niveau d'approbation")  # Ajout du champ level
    status = models.CharField(max_length=10, choices=REVIEW_CHOICES, default=REVIEW_PENDING, verbose_name="Statut")
    approved_at = models.DateTimeField(null=True, blank=True, verbose_name="Date d'approbation")
    comments = models.TextField(blank=True, verbose_name="Commentaires")

    class Meta:
        unique_together = ('requisition', 'level')  # Assurez-vous qu'il n'y a qu'une seule review par niveau pour chaque requisition
        ordering = ['level']
        verbose_name = "Revue"
        verbose_name_plural = "Revues"

    def __str__(self):
        return f"Revue de {self.reviewer} pour {self.requisition} (Niveau {self.level})"

    def save(self, *args, **kwargs):
        if self.status == self.REVIEW_APPROVED and not self.approved_at:
            self.approved_at = timezone.now()

            # Notification par e-mail à l'approbateur suivant
            next_level = self.requisition.reviews.filter(level=self.level + 1).first()
            if next_level:
                send_mail(
                    'Nouvelle demande à approuver',
                    f'La demande {self.requisition} nécessite votre approbation.',
                    'from@example.com',  # Remplacez par votre adresse e-mail
                    [next_level.reviewer.email],
                    fail_silently=False,
                )
            else:
                # Toutes les étapes d'approbation ont été complétées
                self.requisition.status = Requisition.STATUS_APPROVED
                self.requisition.save()

                # Envoyer une notification au demandeur
                send_mail(
                    'Demande approuvée',
                    f'Votre demande {self.requisition} a été approuvée.',
                    'from@example.com',  # Remplacez par votre adresse e-mail
                    [self.requisition.requester.email],
                    fail_silently=False,
                )
        elif self.status == self.REVIEW_REJECTED:
            self.requisition.status = Requisition.STATUS_REJECTED
            self.requisition.save()

            # Envoyer une notification au demandeur (rejet)
            send_mail(
                'Demande rejetée',
                f'Votre demande {self.requisition} a été rejetée.',
                'from@example.com',  # Remplacez par votre adresse e-mail
                [self.requisition.requester.email],
                fail_silently=False,
            )

        super().save(*args, **kwargs)
    


class RequisitionItem(models.Model):
    """Détaille les éléments d'une demande de fonds."""
    requisition = models.ForeignKey('requisition.Requisition', on_delete=models.CASCADE, related_name='items', verbose_name="Demande")
    description = models.CharField(max_length=255, verbose_name="Description")
    quantity = models.PositiveIntegerField(null=True, blank=True, verbose_name="Quantité")
    unit_price = MoneyField(max_digits=14, decimal_places=2, null=True, blank=True, default_currency='CDF', verbose_name="Prix unitaire")
    total_price = MoneyField(max_digits=19, decimal_places=2, null=True, blank=True, default_currency='CDF', verbose_name="Prix total")
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Article (optionnel)")

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        if self.quantity and self.unit_price:
            self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)


class RequisitionShare(models.Model):
    requisition = models.ForeignKey(Requisition, on_delete=models.CASCADE, related_name='shares', verbose_name="Demande")
    shared_with = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Partagé avec")
    can_approve = models.BooleanField(default=False, verbose_name="Peut approuver")

    class Meta:
        unique_together = ('requisition', 'shared_with')
        verbose_name = "Partage de demande"
        verbose_name_plural = "Partages de demande"

    def __str__(self):
        return f"Demande {self.requisition} partagée avec {self.shared_with}"