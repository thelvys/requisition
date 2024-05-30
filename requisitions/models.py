from django.db import models
from django.contrib.auth.models import AbstractUser
from djmoney.models.fields import MoneyField


class CustomUser(AbstractUser):
    # Champs supplémentaires pour l'utilisateur (ex: département, titre...)
    department = models.CharField(max_length=100)
    supervisor = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

class Group(models.Model):
    name = models.CharField(max_length=100)
    parent_group = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    members = models.ManyToManyField(CustomUser, related_name='groups')

class Requisition(models.Model):
    requester = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_submitted = models.DateTimeField(auto_now_add=True)
    details = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'En Attente'),
        ('approved', 'Approuvé'),
        ('rejected', 'Rejeté'),
    ])
    current_approver = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='requisitions_to_approve')
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')  # Ajout du champ montant
    shared_with = models.ManyToManyField(CustomUser, related_name='shared_requisitions', blank=True)  # Ajout du champ ManyToManyField
