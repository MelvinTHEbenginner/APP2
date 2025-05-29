from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('categorie/<int:categorie_id>/', views.liste_produits_par_categorie, name='liste_produits_par_categorie'),
    path('produit/<int:produit_id>/', views.detail_produit, name='detail_produit'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('ajouter_produit/', views.ajouter_produit, name='ajouter_produit'),
    path('commander/<int:produit_id>/', views.passer_commande, name='passer_commande'),
    path('commandes/', views.liste_commandes, name='liste_commandes'),
    path('commandes/<int:commande_id>/', views.detail_commande, name='detail_commande'),
    path('produit/<int:produit_id>/ajouter_avis/', views.ajouter_avis, name='ajouter_avis'),
    path('carte/', views.carte_producteurs, name='carte_producteurs'),
    path('commande/<int:commande_id>/payer/', views.initier_paiement_mobile, name='initier_paiement_mobile'),
    path('commande/<int:commande_id>/verifier/', views.verifier_paiement_mobile, name='verifier_paiement_mobile'),
    path('paiement/reussi/<int:commande_id>/', views.paiement_reussi, name='paiement_reussi'),
    path('paiement/echoue/<int:commande_id>/', views.paiement_echoue, name='paiement_echoue'),
    path('admin/vendeurs-a-confirmer/', views.liste_vendeurs_a_confirmer, name='liste_vendeurs_a_confirmer'),
    path('admin/confirmer-vendeur/<int:user_id>/', views.confirmer_vendeur, name='confirmer_vendeur'),
    path('vendeur/<int:vendeur_id>/contacter/', views.contacter_vendeur, name='contacter_vendeur'),
    
    # URLs pour la messagerie
    path('messagerie/', views.liste_conversations, name='liste_conversations'),
    path('messagerie/nouveau/<int:user_id>/', views.demarrer_conversation, name='demarrer_conversation'),
    path('messagerie/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('messagerie/<int:conversation_id>/supprimer/', views.supprimer_conversation, name='supprimer_conversation'),
    
    # URL pour la page de formation
    path('formation/', views.formation, name='formation'),
]