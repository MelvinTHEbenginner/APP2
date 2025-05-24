from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    USER_ROLES = [
        ('acheteur', 'Acheteur'),
        ('vendeur', 'Vendeur'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile_pics/', blank=True)
    description = models.TextField(blank=True)
    localisation = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    certifications = models.FileField(upload_to='certifications/', blank=True)
    role = models.CharField(max_length=10, choices=USER_ROLES, default='acheteur')
    is_vendeur_confirmed = models.BooleanField(default=False)
    telephone = models.CharField(max_length=20, blank=True, verbose_name="Numéro de téléphone")
    whatsapp = models.CharField(max_length=20, blank=True, verbose_name="WhatsApp")
    accepte_contact = models.BooleanField(default=True, verbose_name="Accepte d'être contacté")

    def __str__(self):
        return self.user.username

class CategorieProduit(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nom

class Produit(models.Model):
    vendeur = models.ForeignKey(User, on_delete=models.CASCADE)
    categorie = models.ForeignKey(CategorieProduit, on_delete=models.CASCADE)
    nom = models.CharField(max_length=255)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    quantite = models.PositiveIntegerField()
    photo = models.ImageField(upload_to='produits/', blank=True)
    description = models.TextField(blank=True)
    date_ajout = models.DateTimeField(auto_now_add=True)
    est_actif = models.BooleanField(default=True)
    saisonnalite = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.nom

class Commande(models.Model):
    acheteur = models.ForeignKey(User, on_delete=models.CASCADE)
    date_commande = models.DateTimeField(auto_now_add=True)
    est_livree = models.BooleanField(default=False)
    total = models.DecimalField(max_digits=10, decimal_places=2)  

    def __str__(self):
        return f"Commande #{self.id}"

class LigneDeCommande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantite} x {self.produit.nom} dans la commande #{self.commande.id}"

# ... autres imports et modèles ...

class Avis(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    NOTE_CHOICES = [(i, str(i)) for i in range(1, 6)]
    note = models.IntegerField(choices=NOTE_CHOICES)
    commentaire = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avis de {self.auteur.username} sur {self.produit.nom}"
    
