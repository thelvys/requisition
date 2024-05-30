import uuid
from django.db import models
from django.urls import reverse
from djmoney.models.fields import MoneyField
from djmoney.money import Money

from config import settings
from accounts.models import Department

class Requisition(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Brouillon'),  # Traduction plus claire
        ('submitted', 'Soumise'), # Changement de nom pour plus de précision
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)
    narration = models.CharField(max_length=250)
    amount = MoneyField(max_digits=19, decimal_places=2, default_currency='USD')
    exchange_rate = models.DecimalField(max_digits=11, decimal_places=4, default=1)  # Champ pour stocker le taux de change
    amount_converted = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    cost_center = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)  # Utilisation de chaînes pour les références
    budget = models.ForeignKey('Budget', on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')  # Nom plus explicite
    attachments = models.ManyToManyField('Attachment', blank=True)  # Relation ManyToMany pour les pièces jointes
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_requisitions')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-modified_at',)
        constraints = [
            models.UniqueConstraint(fields=['requester', 'narration'], name='unique_request_per_user')  # Contrainte d'unicité
        ]

    def __str__(self):
        return self.narration

    def save(self, *args, **kwargs):
        if self.status == 'submitted' and not self.amount_converted:
            self.amount_converted = self.amount.amount * self.exchange_rate  # Utilisation du taux enregistré
        super().save(*args, **kwargs)

    @property
    def converted_amount_display(self):
        """Affiche le montant converti en utilisant MoneyField pour le formatage."""
        if self.amount_converted:
            return Money(self.amount_converted, 'CDF')
        return None

    def get_absolute_url(self):
        return reverse("requisition:detail", args=[str(self.id)])


class Review(models.Model):
    REVIEW_CHOICES = (
        ('pending', 'En attente'),
        ('approved', 'Approuvée'),  # Correction orthographique
        ('checked', 'Vérifiée'),
        ('rejected', 'Rejetée'),
    )

    requisition = models.ForeignKey(Requisition, on_delete=models.CASCADE, related_name="reviews")
    status = models.CharField(max_length=10, choices=REVIEW_CHOICES, default='pending')  # Nom plus explicite
    comment = models.TextField(blank=True, null=True)
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['requisition', 'reviewer']

    def __str__(self):
        return self.status