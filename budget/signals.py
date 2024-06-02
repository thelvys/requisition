from django.db.models.signals import post_save
from django.dispatch import receiver
from cashflow.models import Payment
from budget.models import Expense, RequisitionBudget

@receiver(post_save, sender=Payment)
def create_expense_from_payment(sender, instance, created, **kwargs):
    """Crée une dépense à partir d'un paiement."""
    if created:
        # Trouvez la ligne budgétaire correspondante à la requisition
        try:
            requisition_budget = RequisitionBudget.objects.get(requisition=instance.requisition)
            budget_item = requisition_budget.budget_item
        except RequisitionBudget.DoesNotExist:
            # Gérer le cas où la requisition n'est pas liée à un budget
            return

        # Créez la dépense
        Expense.objects.create(
            requisition=instance.requisition,
            budget_item=budget_item,
            amount=instance.amount,
            date=instance.payment_date,
            description=f"Paiement de la demande {instance.requisition}",
        )
