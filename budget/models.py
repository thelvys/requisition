from django.db import models
from djmoney.models.fields import MoneyField

from requisitions.models import Requisition  # Importez le modèle Requisition

class BudgetPeriod(models.Model):
    """Modèle pour définir les différentes périodes budgétaires."""

    PERIOD_WEEK = 'week'
    PERIOD_MONTH = 'month'
    PERIOD_QUARTER = 'quarter'  # Un trimestre est un quart d'année
    PERIOD_YEAR = 'year'
    PERIOD_CHOICES = [
        (PERIOD_WEEK, 'Semaine'),
        (PERIOD_MONTH, 'Mois'),
        (PERIOD_QUARTER, 'Trimestre'),
        (PERIOD_YEAR, 'Année'),
    ]

    period_type = models.CharField(max_length=10, choices=PERIOD_CHOICES, verbose_name="Type de période")
    start_date = models.DateField(verbose_name="Date de début")
    end_date = models.DateField(verbose_name="Date de fin")

    class Meta:
        verbose_name = "Période budgétaire"
        verbose_name_plural = "Périodes budgétaires"

    def __str__(self):
        return f"{self.get_period_type_display()} du {self.start_date} au {self.end_date}"


class Budget(models.Model):
    """Modèle représentant un budget pour un centre de coût et une période."""

    cost_center = models.ForeignKey('accounts.Department', on_delete=models.CASCADE, verbose_name="Centre de coût")
    period = models.ForeignKey(BudgetPeriod, on_delete=models.CASCADE, verbose_name="Période")
    amount = MoneyField(max_digits=19, decimal_places=2, default_currency='CDF', verbose_name="Montant budgété")

    class Meta:
        unique_together = ('cost_center', 'period')
        verbose_name = "Budget"
        verbose_name_plural = "Budgets"

    def __str__(self):
        return f"Budget de {self.amount} pour {self.cost_center} en {self.period}"


class BudgetItem(models.Model):
    """Ligne d'un budget, représentant une catégorie de dépenses."""

    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='items', verbose_name="Budget")
    category = models.CharField(max_length=100, verbose_name="Catégorie")
    amount = MoneyField(max_digits=19, decimal_places=2, default_currency='CDF', verbose_name="Montant alloué")

    def __str__(self):
        return f"{self.category} - {self.amount}"


class RequisitionBudget(models.Model):
    """Modèle pour lier une demande à un budget."""

    requisition = models.OneToOneField(Requisition, on_delete=models.CASCADE, verbose_name="Demande")
    budget_item = models.ForeignKey(BudgetItem, on_delete=models.PROTECT, verbose_name="Ligne budgétaire")

    def __str__(self):
        return f"Demande {self.requisition} liée au budget {self.budget_item.budget}"
