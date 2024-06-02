import uuid
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from djmoney.models.fields import MoneyField

from config.models import ExchangeRate
from groups.models import Category


class Supplier(models.Model):
    """Fournisseur de produits."""
    name = models.CharField(max_length=255, verbose_name="Nom")
    country = models.CharField(max_length=255, verbose_name="Pays")
    code = models.CharField(max_length=190, unique=True, verbose_name="Code")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    modified_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")

    class Meta:
        ordering = ["-modified_at"]
        verbose_name = "Fournisseur"
        verbose_name_plural = "Fournisseurs"

    def __str__(self):
        return self.name


class Warehouse(models.Model):
    """Emplacement de stockage des produits."""
    name = models.CharField(max_length=255, verbose_name="Nom")
    address = models.TextField(verbose_name="Adresse")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name="Responsable")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    modified_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")

    class Meta:
        verbose_name = "Entrepôt"
        verbose_name_plural = "Entrepôts"

    def __str__(self):
        return self.name


class Item(models.Model):
    """Produit stocké."""
    name = models.CharField(max_length=255, verbose_name="Nom")
    specification = models.CharField(max_length=255, verbose_name="Spécification")
    code = models.CharField(max_length=190, unique=True, verbose_name="Code")
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    supplier = models.ManyToManyField(Supplier, verbose_name="Fournisseurs")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    modified_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")

    class Meta:
        ordering = ["-modified_at"]
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return self.name


class Stock(models.Model):
    """Quantité d'un produit dans un entrepôt."""
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name="Entrepôt")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="Article")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Quantité")

    class Meta:
        unique_together = ('warehouse', 'item')
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"

    def __str__(self):
        return f"{self.quantity} x {self.item} dans {self.warehouse}"


class Order(models.Model):
    """Commande de produits auprès d'un fournisseur."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_order = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, verbose_name="Utilisateur")
    order_num = models.CharField(max_length=190, unique=True, verbose_name="Numéro de commande")
    invoice_num = models.CharField(max_length=190, unique=True, verbose_name="Numéro de facture")
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="orders", verbose_name="Fournisseur")
    amount = MoneyField(max_digits=19, decimal_places=2, default_currency="USD", verbose_name="Montant")
    amount_converted = MoneyField(
        max_digits=19,
        decimal_places=2,
        default_currency="CDF",
        blank=True,
        null=True,
        verbose_name="Montant converti",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    modified_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")

    class Meta:
        ordering = ["-modified_at"]
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"

    def __str__(self):
        return self.order_num

    def save(self, *args, **kwargs):
        if self.amount.currency != self.currency_saved:
            try:
                exchange_rate = ExchangeRate.objects.get(
                    source_currency=self.amount.currency,
                    target_currency=self.currency_saved
                ).rate
            except ExchangeRate.DoesNotExist:
                raise ValueError(f"Aucun taux de change trouvé pour {self.amount.currency} -> {self.currency_saved}")

            self.amount_converted = self.amount.convert_to(self.currency_saved, exchange_rate)
        else:
            self.amount_converted = self.amount

        super().save(*args, **kwargs)

    @property
    def get_amount_converted(self):
        """Retourne le montant converti sous forme d'objet Money ou le montant original."""
        return self.amount_converted or self.amount

    def get_absolute_url(self):
        return reverse("order:detail", args=[str(self.id)])


class OrderItem(models.Model):
    """Ligne d'une commande, détaille les articles commandés."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Commande")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="Article")
    quantity = models.PositiveIntegerField(verbose_name="Quantité")
    unit_price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', verbose_name="Prix unitaire")

    class Meta:
        verbose_name = "Ligne de commande"
        verbose_name_plural = "Lignes de commande"

    def __str__(self):
        return f"{self.quantity} x {self.item} pour {self.order}"

    @property
    def total_price(self):
        """Calcule le prix total de la ligne de commande."""
        return self.quantity * self.unit_price



class Carrier(models.Model):
    """Entreprise ou personne qui assure le transport des marchandises."""
    name = models.CharField(max_length=255, verbose_name="Nom")
    contact_person = models.CharField(max_length=255, blank=True, verbose_name="Personne de contact")
    phone_number = models.CharField(max_length=20, blank=True, verbose_name="Numéro de téléphone")
    email = models.EmailField(blank=True, verbose_name="Adresse e-mail")

    class Meta:
        verbose_name = "Transporteur"
        verbose_name_plural = "Transporteurs"

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    """Moyen de transport utilisé pour une expédition."""
    license_plate = models.CharField(max_length=20, unique=True, verbose_name="Plaque d'immatriculation")
    vehicle_type = models.CharField(max_length=50, verbose_name="Type de véhicule")
    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE, verbose_name="Transporteur")

    class Meta:
        verbose_name = "Véhicule"
        verbose_name_plural = "Véhicules"

    def __str__(self):
        return f"{self.license_plate} ({self.vehicle_type})"


class Shipment(models.Model):
    """Expédition de produits depuis un entrepôt."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='shipments', verbose_name="Commande") 
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name="Entrepôt")
    shipped_at = models.DateTimeField(null=True, blank=True, verbose_name="Date d'expédition")
    carrier = models.ForeignKey(Carrier, on_delete=models.PROTECT, verbose_name="Transporteur")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT, verbose_name="Véhicule")
    tracking_number = models.CharField(max_length=100, blank=True, verbose_name="Numéro de suivi")

    class Meta:
        verbose_name = "Expédition"
        verbose_name_plural = "Expéditions"

    def __str__(self):
        return f"Expédition n°{self.id} de la commande {self.order} depuis {self.warehouse}"


class ShipmentItem(models.Model):
    """Ligne d'un envoi, détaille les articles expédiés et leur quantité."""
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='items', verbose_name="Expédition")
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, verbose_name="Ligne de commande")
    quantity = models.PositiveIntegerField(verbose_name="Quantité expédiée")

    class Meta:
        verbose_name = "Article expédié"
        verbose_name_plural = "Articles expédiés"
        unique_together = ('shipment', 'order_item')

    def __str__(self):
        return f"{self.quantity} x {self.order_item.item} dans l'expédition {self.shipment}"


class ShipmentStatusUpdate(models.Model):
    """Suivi de l'état d'une expédition."""
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name="status_updates", verbose_name="Expédition")
    status = models.CharField(max_length=50, verbose_name="Statut")
    location = models.CharField(max_length=255, blank=True, verbose_name="Emplacement")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Horodatage")

    class Meta:
        verbose_name = "Mise à jour du statut d'expédition"
        verbose_name_plural = "Mises à jour du statut d'expédition"

    def __str__(self):
        return f"{self.status} - {self.shipment}"



class StockTransfer(models.Model):
    """Transfert de produits entre entrepôts, nécessitant l'approbation des responsables."""
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'En attente'),
        (STATUS_APPROVED, 'Approuvé'),
        (STATUS_REJECTED, 'Rejeté'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    from_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="outgoing_transfers", verbose_name="Entrepôt source")
    to_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="incoming_transfers", verbose_name="Entrepôt destination")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="Article")
    quantity = models.PositiveIntegerField(verbose_name="Quantité")
    transfer_date = models.DateTimeField(auto_now_add=True, verbose_name="Date de demande")
    comments = models.TextField(blank=True, verbose_name="Commentaires")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING, verbose_name="Statut")
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Approuvé par"
    )
    approved_at = models.DateTimeField(null=True, blank=True, verbose_name="Date d'approbation")

    class Meta:
        verbose_name = "Transfert de stock"
        verbose_name_plural = "Transferts de stock"

    def __str__(self):
        return f"Transfert de {self.quantity} x {self.item} de {self.from_warehouse} vers {self.to_warehouse}"

    def save(self, *args, **kwargs):
        # Logique pour mettre à jour les stocks uniquement si le transfert est approuvé
        if self.status == self.STATUS_APPROVED and not self.approved_at:
            self.approved_at = timezone.now()  # Enregistrez la date d'approbation
            # Mettez à jour les stocks ici (diminuer dans from_warehouse, augmenter dans to_warehouse)
        super().save(*args, **kwargs)


class Machine(models.Model):
    """Machine utilisée dans le processus de production."""
    name = models.CharField(max_length=100, verbose_name="Nom")
    code = models.CharField(max_length=50, unique=True, verbose_name="Code")
    description = models.TextField(blank=True, verbose_name="Description")

    class Meta:
        verbose_name = "Machine"
        verbose_name_plural = "Machines"

    def __str__(self):
        return f"{self.code} - {self.name}"
    

class ProductionOrder(models.Model):
    """Ordre de production d'un produit fini."""
    order_number = models.CharField(max_length=50, unique=True, verbose_name="Numéro de l'ordre")
    product = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="Produit fini")
    quantity = models.PositiveIntegerField(verbose_name="Quantité à produire")
    start_date = models.DateField(verbose_name="Date de début")
    due_date = models.DateField(verbose_name="Date d'échéance")
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'En attente'),
            ('in_progress', 'En cours'),
            ('completed', 'Terminé'),
            ('cancelled', 'Annulé'),
        ],
        default='pending',
        verbose_name="Statut"
    )

    class Meta:
        verbose_name = "Ordre de production"
        verbose_name_plural = "Ordres de production"

    def __str__(self):
        return f"Ordre de production {self.order_number} - {self.product}"


class BillOfMaterials(models.Model):
    """Nomenclature (BOM) définissant les composants d'un produit fini."""
    product = models.OneToOneField(Item, on_delete=models.CASCADE, related_name='bill_of_materials', verbose_name="Produit fini")

    class Meta:
        verbose_name = "Nomenclature"
        verbose_name_plural = "Nomenclatures"

    def __str__(self):
        return f"BOM pour {self.product}"


class BillOfMaterialsItem(models.Model):
    """Ligne d'une nomenclature, associant un composant et sa quantité."""
    bill_of_materials = models.ForeignKey(BillOfMaterials, on_delete=models.CASCADE, related_name='items', verbose_name="Nomenclature")
    component = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="Composant")
    quantity = models.PositiveIntegerField(verbose_name="Quantité")

    class Meta:
        verbose_name = "Ligne de nomenclature"
        verbose_name_plural = "Lignes de nomenclature"

    def __str__(self):
        return f"{self.quantity} x {self.component} pour {self.bill_of_materials.product}"



class ProductionStep(models.Model):
    """Étape de production d'un produit fini."""
    production_order = models.ForeignKey(ProductionOrder, on_delete=models.CASCADE, verbose_name="Ordre de production")
    description = models.CharField(max_length=255, verbose_name="Description")
    machine = models.ForeignKey(Machine, on_delete=models.PROTECT, verbose_name="Machine")  # Nouvelle relation
    estimated_time = models.DurationField(verbose_name="Temps estimé")
    completed = models.BooleanField(default=False, verbose_name="Terminé")

    class Meta:
        verbose_name = "Étape de production"
        verbose_name_plural = "Étapes de production"

    def __str__(self):
        return f"{self.description} (sur {self.machine})"