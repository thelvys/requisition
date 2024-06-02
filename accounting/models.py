from django.db import models
from djmoney.models.fields import MoneyField
from treebeard.mp_tree import MP_Node

from config import settings

from config.models import ExchangeRate
from cashflow.models import AccountTransfer, Payment


class Account(MP_Node):
    """Plan comptable basé sur l'OHADA, avec prise en charge de plusieurs devises."""

    class_number = models.IntegerField(choices=[(i, i) for i in range(1, 10)], verbose_name="Classe")
    code = models.CharField(max_length=20, unique=True, verbose_name="Code du compte")
    name = models.CharField(max_length=100, verbose_name="Nom du compte")
    account_type = models.CharField(
        max_length=20,
        choices=[
            ('asset', 'Actif'),
            ('liability', 'Passif'),
            ('equity', 'Capitaux propres'),
            ('income', 'Revenus'),
            ('expense', 'Dépenses'),
        ],
        verbose_name="Type de compte"
    )
    currency = models.CharField(max_length=3, choices=settings.CURRENCY_CHOICES, default='CDF', verbose_name="Devise")

    node_order_by = ['class_number', 'code']

    class Meta:
        verbose_name = "Compte"
        verbose_name_plural = "Plan comptable"

    def __str__(self):
        return f"{self.code} - {self.name} ({self.currency})"



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


class Journal(models.Model):
    """Journal comptable (ex: Ventes, Achats, Banque, etc.)."""
    
    name = models.CharField(max_length=100, verbose_name="Nom du journal")
    code = models.CharField(max_length=10, unique=True, verbose_name="Code du journal")

    class Meta:
        verbose_name = "Journal"
        verbose_name_plural = "Journaux"

    def __str__(self):
        return self.name


class Transaction(models.Model):
    """Transaction financière (vente, achat, paiement, etc.)."""
    date = models.DateField(verbose_name="Date")
    journal = models.ForeignKey(Journal, on_delete=models.PROTECT, verbose_name="Journal")
    reference = models.CharField(max_length=50, blank=True, verbose_name="Référence")
    description = models.CharField(max_length=255, verbose_name="Description")
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Paiement")
    account_transfer = models.ForeignKey(AccountTransfer, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Transfert de compte")

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

    def __str__(self):
        return f"{self.date} - {self.description}"


class TransactionItem(models.Model):
    """Ligne d'une transaction (débit/crédit)."""
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='items', verbose_name="Transaction")
    account = models.ForeignKey(Account, on_delete=models.PROTECT, verbose_name="Compte")
    amount = MoneyField(max_digits=19, decimal_places=2, default_currency='CDF', verbose_name="Montant")
    is_debit = models.BooleanField(verbose_name="Débit")

    def __str__(self):
        return f"{self.account} - {self.amount} ({'Débit' if self.is_debit else 'Crédit'})"

    def save(self, *args, **kwargs):
        # Conversion automatique du montant si la devise du compte est différente
        if self.amount.currency != self.account.currency:
            try:
                exchange_rate = ExchangeRate.objects.get(
                    source_currency=self.amount.currency,
                    target_currency=self.account.currency
                ).rate
            except ExchangeRate.DoesNotExist:
                raise ValueError(f"Aucun taux de change trouvé pour {self.amount.currency} -> {self.account.currency}")

            self.amount = self.amount.convert_to(self.account.currency, exchange_rate)

        super().save(*args, **kwargs)