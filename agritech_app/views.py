from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q, Sum
from django.core import serializers
from django.contrib import messages
from .models import Produit, CategorieProduit, Profile, Commande, LigneDeCommande, Avis, Conversation, Message
from .forms import ProduitForm, ProfileForm, AvisForm, CustomUserCreationForm, UserProfileForm # Utilisation du nouveau formulaire d'inscription
from .utils import envoyer_email_confirmation_commande
from .decorators import admin_required, vendeur_confirme_required, acheteur_required
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactVendeurForm


def is_admin(user):
    """Vérifie si l'utilisateur est un administrateur (staff Django)"""
    return user.is_authenticated and user.is_staff


def is_confirmed_vendeur(user):
    """Vérifie si l'utilisateur est un vendeur confirmé"""
    if user.is_authenticated and hasattr(user, 'profile'):
        return user.profile.role == 'vendeur' and user.profile.is_vendeur_confirmed
    return False

def is_acheteur(user):
    """Vérifie si l'utilisateur est un acheteur"""
    if user.is_authenticated and hasattr(user, 'profile'):
        return user.profile.role == 'acheteur'
    return False

def home(request):
    produits = Produit.objects.filter(est_actif=True).order_by('-date_ajout')
    categories = CategorieProduit.objects.all()
    query = request.GET.get('q')
    
    if query:
        produits = produits.filter(Q(nom__icontains=query) | Q(description__icontains=query))
    
    context = {
        'produits': produits,
        'categories': categories,
        'query': query,
    }
    
    # Si l'utilisateur est authentifié et est un administrateur, afficher le nombre de vendeurs à confirmer
    if request.user.is_authenticated and request.user.is_staff:
        context['nb_vendeurs_a_confirmer'] = Profile.objects.filter(
            role='vendeur',
            is_vendeur_confirmed=False
        ).count()
    
    return render(request, 'home.html', context)

def liste_produits_par_categorie(request, categorie_id):
    categorie = get_object_or_404(CategorieProduit, pk=categorie_id)
    produits = Produit.objects.filter(categorie=categorie, est_actif=True)
    context = {'categorie': categorie, 'produits': produits}
    return render(request, 'liste_produits.html', context)

def detail_produit(request, produit_id):
    produit = get_object_or_404(Produit, pk=produit_id)
    context = {'produit': produit}
    return render(request, 'detail_produit.html', context)

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            
            user.is_staff = False
            user.is_superuser = False
            user.save()
            
            # pour creer mon putain de profile
            role = form.cleaned_data.get('role', 'acheteur')
            Profile.objects.create(
                user=user, 
                role=role,
                # Vendeurs non confirmés par défaut
                is_vendeur_confirmed=(role != 'vendeur')
            )
            
            login(request, user)
            if role == 'vendeur':
                messages.info(request, "Votre compte vendeur a été créé, mais doit être confirmé par un administrateur avant d'être actif.")
            else:
                messages.success(request, "Votre compte a été créé avec succès.")
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  
    else:
        form = AuthenticationForm()
    return render(request, 'agritech_app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "Vous avez été déconnecté avec succès.")
    return redirect('home')  

@login_required
def profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user, role='acheteur')

    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Votre profil a été mis à jour avec succès.")
            return redirect('profile')
    else:
        user_form = UserProfileForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'profile.html', context)


def is_confirmed_vendeur(user):
    if user.is_authenticated and hasattr(user, 'profile'):
        return user.profile.role == 'vendeur' and user.profile.is_vendeur_confirmed
    return False

@login_required
def ajouter_produit(request):
    # possible tu le maitre ou vendeur 
    if not (request.user.is_staff or 
            (hasattr(request.user, 'profile') and 
             request.user.profile.role == 'vendeur' and 
             request.user.profile.is_vendeur_confirmed)):
        messages.error(request, "Accès réservé aux administrateurs et vendeurs confirmés")
        return redirect('home')

    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES)
        if form.is_valid():
            produit = form.save(commit=False)
            produit.vendeur = request.user
            produit.save()
            messages.success(request, "Produit ajouté avec succès!")
            return redirect('profile')
    else:
        form = ProduitForm()
    
    return render(request, 'ajouter_produit.html', {'form': form})

@login_required
def passer_commande(request, produit_id):
    produit = get_object_or_404(Produit, pk=produit_id)
    
    if request.method == 'POST':
        quantite = int(request.POST.get('quantite', 1))
        livraison = request.POST.get('livraison', 'domicile')
        
        # Calcul du prix avec frais de livraison
        frais_livraison = 1500 if livraison == 'domicile' else 0
        total = (produit.prix * quantite) + frais_livraison
        
        # Création de la comma
        commande = Commande.objects.create(
            acheteur=request.user,
            total=total
        )
        
        LigneDeCommande.objects.create(
            commande=commande,
            produit=produit,
            quantite=quantite,
            prix_unitaire=produit.prix
        )
        
        # Envoi d'email
        try:
            send_mail(
                f"Confirmation de commande #{commande.id}",
                f"Votre commande de {quantite} {produit.nom} a été enregistrée. Total: {total} FCFA",
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=False,
            )
            messages.success(request, "Commande confirmée! Un email de confirmation vous a été envoyé.")
        except Exception as e:
            messages.warning(request, "Commande confirmée mais l'email n'a pas pu être envoyé.")
        
        return redirect('liste_commandes')
    
    return render(request, 'passer_commande.html', {'produit': produit})

@login_required
def liste_commandes(request):
    commandes = Commande.objects.filter(acheteur=request.user)\
                               .order_by('-date_commande')\
                               .prefetch_related('lignedecommande_set__produit')
    context = {'commandes': commandes}
    return render(request, 'liste_commandes.html', context)

@login_required
def detail_commande(request, commande_id):
    commande = get_object_or_404(Commande, pk=commande_id, acheteur=request.user)
    lignes_de_commande = LigneDeCommande.objects.filter(commande=commande)
    context = {'commande': commande, 'lignes_de_commande': lignes_de_commande}
    return render(request, 'detail_commande.html', context)

@login_required
def ajouter_avis(request, produit_id):
    produit = get_object_or_404(Produit, pk=produit_id)
    
    if request.method == 'POST':
        form = AvisForm(request.POST)
        if form.is_valid():
            avis = form.save(commit=False)
            avis.produit = produit
            avis.auteur = request.user
            avis.save()
            messages.success(request, "Votre avis a été ajouté avec succès.")
            return redirect('detail_produit', produit_id=produit_id)
    else:
        form = AvisForm()  
    
    context = {'form': form, 'produit': produit}
    return render(request, 'ajouter_avis.html', context)

def carte_producteurs(request):
    producteurs = Profile.objects.exclude(latitude__isnull=True, longitude__isnull=True).filter(user__produit__est_actif=True, role='vendeur', is_vendeur_confirmed=True).distinct()
    producteurs_data = serializers.serialize('json', producteurs, fields=('latitude', 'longitude', 'user__username'))
    context = {'producteurs': producteurs_data}
    return render(request, 'carte_producteurs.html', context)

@login_required
def initier_paiement_mobile(request, commande_id):
    commande = get_object_or_404(Commande, pk=commande_id, acheteur=request.user)
    if request.method == 'POST':
        numero_telephone = request.POST.get('numero_telephone')
        montant = commande.lignedecommande_set.aggregate(total=Sum('prix_unitaire'))['total']
        # TCHAI PAS FINI HEIN 
        commande.transaction_id = f"TEMP_TRANS_{commande.id}"
        commande.save()
        return redirect('verifier_paiement_mobile', commande_id=commande_id)
    else:
        return render(request, 'formulaire_paiement_mobile.html', {'commande': commande})

@login_required
def verifier_paiement_mobile(request, commande_id):
    commande = get_object_or_404(Commande, pk=commande_id, acheteur=request.user)
    transaction_id = commande.transaction_id
    # BAIDAI
    commande.est_livree = True
    commande.save()
    return redirect('paiement_reussi', commande_id=commande_id)

def paiement_reussi(request, commande_id):
    commande = get_object_or_404(Commande, pk=commande_id, acheteur=request.user)
    return render(request, 'paiement_reussi.html', {'commande': commande})

def paiement_echoue(request, commande_id, erreur=""):
    commande = get_object_or_404(Commande, pk=commande_id, acheteur=request.user)
    return render(request, 'paiement_echoue.html', {'commande': commande, 'erreur': erreur})

def formulaire_paiement_mobile(request, commande):
    return render(request, 'formulaire_paiement_mobile.html', {'commande': commande})

# Vues spécifiques à l'administrateur
@login_required
@user_passes_test(is_admin)
def liste_vendeurs_a_confirmer(request):
    if not request.user.is_staff:
        messages.error(request, "Accès refusé. Vous n'avez pas les droits d'administration.")
        return redirect('home')
    
    vendeurs_a_confirmer = User.objects.filter(
        profile__role='vendeur',
        profile__is_vendeur_confirmed=False
    ).select_related('profile')
    
    nb_vendeurs = vendeurs_a_confirmer.count()
    
    return render(request, 'admin/vendeurs_a_confirmer.html', {
        'vendeurs_a_confirmer': vendeurs_a_confirmer,
        'nb_vendeurs': nb_vendeurs
    })

def formation(request):
    """Vue pour la page de formation"""
    return render(request, 'formation.html')

@login_required
def liste_conversations(request):
    conversations = request.user.conversations.all().order_by('-date_modification')
    
    # Ajouter le nombre de messages non lus pour chaque conversation
    conversations_avec_infos = []
    for conv in conversations:
        nb_non_lus = conv.messages.filter(destinataire=request.user, lu=False).count()
        autre_participant = conv.participants.exclude(id=request.user.id).first()
        conversations_avec_infos.append({
            'conversation': conv,
            'nb_non_lus': nb_non_lus,
            'autre_participant': autre_participant,
            'dernier_message': conv.messages.last()
        })
    
    return render(request, 'messagerie/liste_conversations.html', {
        'conversations_avec_infos': conversations_avec_infos
    })

@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    
    if request.method == 'POST':
        contenu = request.POST.get('contenu')
        if contenu:
            # Récupérer l'autre participant comme destinataire
            destinataire = conversation.participants.exclude(id=request.user.id).first()
            
            Message.objects.create(
                conversation=conversation,
                expediteur=request.user,
                destinataire=destinataire,
                contenu=contenu
            )
            # Mettre à jour la date de modification de la conversation
            conversation.save()
            return redirect('conversation_detail', conversation_id=conversation.id)
    
    messages = conversation.messages.all()
    # Marquer les messages non lus comme lus
    conversation.messages.filter(lu=False).exclude(expediteur=request.user).update(lu=True)
    
    # Récupérer l'autre participant
    autre_participant = conversation.participants.exclude(id=request.user.id).first()
    
    return render(request, 'messagerie/conversation.html', {
        'conversation': conversation,
        'messages': messages,
        'autre_participant': autre_participant
    })

@login_required
def demarrer_conversation(request, user_id):
    autre_utilisateur = get_object_or_404(User, id=user_id)
    
    # Vérifier si une conversation existe déjà entre ces utilisateurs
    conversation = Conversation.objects.filter(participants=request.user).filter(participants=autre_utilisateur).first()
    
    if not conversation:
        # Créer une nouvelle conversation
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, autre_utilisateur)
    
    return redirect('conversation_detail', conversation_id=conversation.id)

@login_required
def supprimer_conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    if request.method == 'POST':
        conversation.delete()
        return redirect('liste_conversations')
    return redirect('conversation_detail', conversation_id=conversation.id)

@login_required
@user_passes_test(is_admin)  
def confirmer_vendeur(request, user_id):
    try:
        profile = Profile.objects.get(user_id=user_id, role='vendeur')
        profile.is_vendeur_confirmed = True
        profile.save()
        messages.success(request, f"Le vendeur {profile.user.username} a été confirmé.")
    except Profile.DoesNotExist:
        messages.error(request, "Le profil de vendeur à confirmer n'existe pas.")
    return redirect('liste_vendeurs_a_confirmer')

@login_required
@user_passes_test(is_acheteur)
def contacter_vendeur(request, vendeur_id):
    vendeur = get_object_or_404(User, id=vendeur_id)
    
    produit_id = request.session.get('current_product_id')  
    produit = get_object_or_404(Produit, id=produit_id) if produit_id else None
    
    if not hasattr(vendeur, 'profile') or not vendeur.profile.accepte_contact:
        messages.error(request, "Ce vendeur ne souhaite pas être contacté directement.")
        return redirect('detail_produit', produit_id=produit_id)
    
    if request.method == 'POST':
        form = ContactVendeurForm(request.POST)
        if form.is_valid():
            # Préparer l'email
            sujet = f"Contact depuis AgriTech: {form.cleaned_data['sujet']}"
            message = f"""
            De: {request.user.email}
            Pour: {vendeur.email}
            Message:
            {form.cleaned_data['message']}
            """
            
            # Envoyer l'email (à configurer avec vos paramètres SMTP) PAS FINI
            send_mail(
                sujet,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [vendeur.email],
                fail_silently=False,
            )
            
            messages.success(request, "Votre message a été envoyé au vendeur.")
            return redirect('detail_produit', produit_id=produit_id)
    else:
        form = ContactVendeurForm()
    
    context = {
        'vendeur': vendeur,
        'form': form,
    }
    return render(request, 'contacter_vendeur.html', context)


@login_required
@user_passes_test(is_admin)
def liste_vendeurs_a_confirmer(request):
    vendeurs = Profile.objects.filter(
        role='vendeur', 
        is_vendeur_confirmed=False
    ).select_related('user').order_by('-user__date_joined')
    
    context = {
        'vendeurs': vendeurs,
        'now': timezone.now()  
    }
    return render(request, 'admin/liste_vendeurs_a_confirmer.html', context)