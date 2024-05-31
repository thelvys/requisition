import uuid
from django.db import models
from django.urls import reverse
from djmoney.models.fields import MoneyField
from djmoney.money import Money

from config import settings
from accounts.models import Department

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
    """Modèle pour les revues de demandes de fonds."""
    REVIEW_CHOICES = (
        ('pending', 'En attente'),
        ('approved', 'Approuvée'),  
        ('checked', 'Vérifiée'),
        ('rejected', 'Rejetée'),
    )

    requisition = models.ForeignKey(Requisition, on_delete=models.CASCADE, related_name="reviews", verbose_name="Demande")
    status = models.CharField(max_length=10, choices=REVIEW_CHOICES, default='pending', verbose_name="Statut") 
    comment = models.TextField(blank=True, null=True, verbose_name="Commentaire")
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, verbose_name="Réviseur")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    modified_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")

    class Meta:
        unique_together = ['requisition', 'reviewer']
        verbose_name = "Revue de demande de fonds"
        verbose_name_plural = "Revues de demandes de fonds"

    def __str__(self):
        return self.status
    


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