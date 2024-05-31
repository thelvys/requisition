import uuid
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey  # Utilisez django-mptt pour la hiérarchie
from djmoney.models.fields import MoneyField

from config import settings


class AccountGroup(MPTTModel):
    """Modèle pour regrouper les comptes de manière hiérarchique."""
    name = models.CharField(max_length=100, verbose_name="Nom du groupe")
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name="Groupe parent")

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class CashAccount(models.Model):
    """Représente un compte de caisse ou un compte bancaire."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account_number = models.CharField(max_length=50, unique=True, verbose_name="Numéro de compte")
    name = models.CharField(max_length=100, verbose_name="Nom du compte")
    account_group = TreeForeignKey(AccountGroup, on_delete=models.PROTECT, verbose_name="Groupe de compte")
    currency = models.CharField(max_length=3, choices=settings.CURRENCY_CHOICES, default='CDF', verbose_name="Devise")
    balance = MoneyField(max_digits=19, decimal_places=2, default_currency='CDF', verbose_name="Solde")

    def __str__(self):
        return f"{self.account_number} - {self.name} ({self.currency})"



class Payment(models.Model):
    """Enregistre un paiement effectué pour une demande."""
    requisition = models.ForeignKey('requisition.Requisition', on_delete=models.CASCADE, verbose_name="Demande")
    cash_account = models.ForeignKey(CashAccount, on_delete=models.PROTECT, verbose_name="Compte utilisé")
    # Le montant et la devise sont déterminés par le compte utilisé
    amount = MoneyField(max_digits=19, decimal_places=2, default_currency='CDF', verbose_name="Montant payé")
    payment_date = models.DateField(verbose_name="Date de paiement")
    reference = models.CharField(max_length=100, blank=True, verbose_name="Référence")

    def __str__(self):
        return f"Paiement de {self.amount} pour {self.requisition}"

    def save(self, *args, **kwargs):
        # Assurez-vous que la devise du paiement correspond à celle du compte
        self.amount.currency = self.cash_account.currency
        super().save(*args, **kwargs)
