from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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



class Avis(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    NOTE_CHOICES = [(i, str(i)) for i in range(1, 6)]
    note = models.IntegerField(choices=NOTE_CHOICES)
    commentaire = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avis de {self.auteur.username} sur {self.produit.num}"

class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_modification']

    def __str__(self):
        return f"Conversation {self.id}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    expediteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_envoyes')
    destinataire = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_recus', null=True)
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['date_envoi']
    
    def __str__(self):
        return f"Message de {self.expediteur.username} dans la conversation {self.conversation.id}"


def get_unread_messages_count(self):
    return self.messages_recus.filter(lu=False).count()


from django.contrib.auth.models import User as BaseUser
BaseUser.add_to_class('get_unread_messages_count', get_unread_messages_count)
    
