from django.contrib import admin
from .models import Profile, CategorieProduit, Produit, Commande, LigneDeCommande, Avis

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'localisation')
    search_fields = ('user__username', 'localisation')
    fieldsets = (
        ('Informations de l\'utilisateur', {
            'fields': ('user',)
        }),
        ('Informations du profil', {
            'fields': ('photo', 'description', 'localisation', 'latitude', 'longitude', 'certifications')
        }),
    )

@admin.register(CategorieProduit)
class CategorieProduitAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'vendeur', 'categorie', 'prix', 'quantite', 'date_ajout', 'est_actif')
    list_filter = ('categorie', 'vendeur', 'est_actif', 'date_ajout')
    search_fields = ('nom', 'description', 'vendeur__username')
    date_hierarchy = 'date_ajout'
    ordering = ('-date_ajout',)
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'categorie', 'vendeur', 'prix', 'quantite', 'est_actif')
        }),
        ('Description et détails', {
            'fields': ('photo', 'description', 'saisonnalite')
        }),
        ('Dates', {
            'fields': ('date_ajout',)
        }),
    )

class LigneDeCommandeInline(admin.TabularInline):
    model = LigneDeCommande
    extra = 1
    raw_id_fields = ('produit',)

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('id', 'acheteur', 'date_commande', 'est_livree')
    list_filter = ('acheteur', 'est_livree', 'date_commande')
    search_fields = ('id', 'acheteur__username')
    date_hierarchy = 'date_commande'
    ordering = ('-date_commande',)
    inlines = [LigneDeCommandeInline]
    fieldsets = (
        ('Informations de la commande', {
            'fields': ('acheteur', 'date_commande', 'est_livree', 'transaction_id')
        }),
    )

@admin.register(LigneDeCommande)
class LigneDeCommandeAdmin(admin.ModelAdmin):
    list_display = ('commande', 'produit', 'quantite', 'prix_unitaire')
    list_filter = ('commande',)
    search_fields = ('commande__id', 'produit__nom')
    raw_id_fields = ('commande', 'produit')

@admin.register(Avis)
class AvisAdmin(admin.ModelAdmin):
    list_display = ('produit', 'auteur', 'note', 'date_creation')
    list_filter = ('produit', 'auteur', 'note', 'date_creation')
    search_fields = ('produit__nom', 'auteur__username', 'commentaire')
    date_hierarchy = 'date_creation'
    ordering = ('-date_creation',)
    fieldsets = (
        ('Informations de l\'avis', {
            'fields': ('produit', 'auteur', 'note', 'commentaire')
        }),
        ('Date de création', {
            'fields': ('date_creation',)
        }),
    )