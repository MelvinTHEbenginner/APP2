from django.core.mail import send_mail
from django.conf import settings

def envoyer_email_confirmation_commande(commande):
    """
    Envoie un email de confirmation à l'acheteur après la création d'une commande.
    
    Args:
        commande: L'instance de la commande qui vient d'être créée
    """
    sujet = f"Confirmation de votre commande #{commande.id}"
    
    # Récupérer les produits de la commande pour les afficher dans l'email
    lignes_commande = commande.lignedecommande_set.all()
    details_produits = []
    
    for ligne in lignes_commande:
        details_produits.append(f"- {ligne.quantite}x {ligne.produit.nom} ({ligne.prix_unitaire} €)")
    
    # Calculer le total de la commande
    total = sum(ligne.quantite * ligne.prix_unitaire for ligne in lignes_commande)
    
    # Corps du message
    message = f"""
Bonjour {commande.acheteur.username},

Nous vous confirmons la réception de votre commande #{commande.id}.

Détails de votre commande:
{''.join(details_produits)}

Total: {total} €

Vous recevrez prochainement des informations concernant la livraison de votre commande.

Merci de votre confiance,
L'équipe Agritech
"""
    
    # Envoyer l'email
    send_mail(
        sujet,
        message,
        settings.DEFAULT_FROM_EMAIL,  # L'expéditeur défini dans settings.py
        [commande.acheteur.email],    # Le destinataire
        fail_silently=False,
    )
    
    return True