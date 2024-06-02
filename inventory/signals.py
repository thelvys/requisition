from django.db.models.signals import post_save, post_delete
from django.core.mail import send_mail
from django.dispatch import receiver
from .models import Stock, StockThreshold

@receiver([post_save, post_delete], sender=Stock)
def check_stock_levels(sender, instance, **kwargs):
    """Vérifie les niveaux de stock et envoie des alertes si nécessaire."""
    try:
        threshold = StockThreshold.objects.get(item=instance.item)
    except StockThreshold.DoesNotExist:
        # Pas de seuil défini pour cet article, rien à faire
        return

    if instance.quantity <= threshold.min_quantity and not threshold.alert_sent:
        # Envoyer une alerte par e-mail (ou autre moyen de notification)
        send_mail(
            'Alerte de stock bas',
            f'Le stock de {instance.item} est tombé à {instance.quantity} dans l\'entrepôt {instance.warehouse}.',
            'from@example.com',  # Remplacez par votre adresse e-mail
            ['to@example.com'],  # Remplacez par les adresses e-mail des destinataires
            fail_silently=False,
        )
        threshold.alert_sent = True
        threshold.save()
    elif instance.quantity > threshold.min_quantity and threshold.alert_sent:
        # Réinitialiser l'alerte si le stock est réapprovisionné
        threshold.alert_sent = False
        threshold.save()
