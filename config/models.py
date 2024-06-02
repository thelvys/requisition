import uuid
from decimal import Decimal

from django.db import models

from config import settings


class ExchangeRate(models.Model):
    """Modèle pour stocker les taux de change."""
    source_currency = models.CharField(max_length=3, choices=settings.CURRENCY_CHOICES, verbose_name="Devise source")
    target_currency = models.CharField(max_length=3, choices=settings.CURRENCY_CHOICES, verbose_name="Devise cible")
    rate = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="Taux de change")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")

    class Meta:
        unique_together = ('source_currency', 'target_currency')
        verbose_name = "Taux de change"
        verbose_name_plural = "Taux de change"

    def __str__(self):
        return f"{self.source_currency} -> {self.target_currency} : {self.rate}"


class Period(models.Model):
    """Période comptable (exercice)."""
    name = models.CharField(max_length=50, verbose_name="Nom de l'exercice")
    start_date = models.DateField(verbose_name="Date de début")
    end_date = models.DateField(verbose_name="Date de fin")
    is_closed = models.BooleanField(default=False, verbose_name="Clôturé")

    class Meta:
        verbose_name = "Période comptable"
        verbose_name_plural = "Périodes comptables"

    def __str__(self):
        return self.name