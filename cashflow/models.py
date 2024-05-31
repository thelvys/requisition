import uuid
from django.db import models
from treebeard.mp_tree import MP_Node
from djmoney.models.fields import MoneyField

from config import settings


class AccountGroup(MP_Node):
    """Modèle pour regrouper les comptes de manière hiérarchique (Materialized Path)."""
    name = models.CharField(max_length=100, verbose_name="Nom du groupe")
    node_order_by = ['name']  # Trie les nœuds par ordre alphabétique

    def __str__(self):
        return self.name


class CashAccount(models.Model):
    """Représente un compte de caisse ou un compte bancaire."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account_number = models.CharField(max_length=50, unique=True, verbose_name="Numéro de compte")
    name = models.CharField(max_length=100, verbose_name="Nom du compte")
    account_group = models.ForeignKey(AccountGroup, on_delete=models.PROTECT, verbose_name="Groupe de compte")
    currency = models.CharField(max_length=3, choices=settings.CURRENCY_CHOICES, default='CDF', verbose_name="Devise")
    balance = MoneyField(max_digits=19, decimal_places=2, default_currency='CDF', verbose_name="Solde")
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigned_accounts', 
        verbose_name="Attribué à"
    )

    def __str__(self):
        return f"{self.account_number} - {self.name} ({self.currency})"
    

class AccountAssignmentHistory(models.Model):
    """Enregistre l'historique des attributions de comptes."""
    cash_account = models.ForeignKey(CashAccount, on_delete=models.CASCADE, verbose_name="Compte")
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Attribué à")
    assigned_at = models.DateTimeField(auto_now_add=True, verbose_name="Date d'attribution")

    def __str__(self):
        return f"{self.cash_account} attribué à {self.assigned_to} le {self.assigned_at}"


class AccountTransfer(models.Model):
    """Enregistre les transferts de fonds entre comptes, avec conversion de devise si nécessaire."""
    from_account = models.ForeignKey(CashAccount, on_delete=models.CASCADE, related_name='outgoing_transfers', verbose_name="Compte source")
    to_account = models.ForeignKey(CashAccount, on_delete=models.CASCADE, related_name='incoming_transfers', verbose_name="Compte destination")
    amount = MoneyField(max_digits=19, decimal_places=2, default_currency='CDF', verbose_name="Montant transféré (devise source)")
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="Taux de change")
    amount_converted = MoneyField(max_digits=19, decimal_places=2, default_currency='CDF', verbose_name="Montant converti (devise destination)")
    transfer_date = models.DateField(verbose_name="Date du transfert")
    reference = models.CharField(max_length=100, blank=True, verbose_name="Référence")

    def __str__(self):
        return f"Transfert de {self.amount} de {self.from_account} vers {self.to_account}"

    def save(self, *args, **kwargs):
        # Vérifiez si les devises sont différentes
        if self.from_account.currency != self.to_account.currency:
            # Calculez le montant converti en utilisant le taux de change
            self.amount_converted = self.amount * self.exchange_rate
            self.amount_converted.currency = self.to_account.currency  # Définissez la devise correcte
        else:
            # Si les devises sont identiques, pas de conversion
            self.amount_converted = self.amount
            self.exchange_rate = 1  # Définissez le taux de change à 1

        super().save(*args, **kwargs)


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
