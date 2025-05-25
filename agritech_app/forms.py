

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Produit, Profile, Avis

class CustomUserCreationForm(UserCreationForm):
    """
    Formulaire d'inscription personnalisé qui inclut le choix du rôle.
    """
    role = forms.ChoiceField(
        choices=Profile.USER_ROLES, 
        widget=forms.RadioSelect,
        label="Rôle",
        help_text="Choisissez votre rôle sur la plateforme"
    )
    email = forms.EmailField(
        max_length=254, 
        required=True, 
        help_text="Obligatoire. Entrez une adresse email valide."
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UserProfileForm(forms.ModelForm):
    """
    Formulaire pour modifier les informations du profil utilisateur.
    """
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

class ProfileForm(forms.ModelForm):
    """
    Formulaire pour modifier les détails du profil.
    """
    class Meta:
        model = Profile
        fields = ['photo', 'description', 'localisation', 'latitude', 'longitude', 'certifications']
        widgets = {
            'latitude': forms.NumberInput(attrs={'step': '0.000001'}),
            'longitude': forms.NumberInput(attrs={'step': '0.000001'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'telephone': forms.TextInput(attrs={'placeholder': '+225 XX XX XX XX'}),
            'whatsapp': forms.TextInput(attrs={'placeholder': '+225 XX XX XX XX'}),
        }

class ProduitForm(forms.ModelForm):
    """
    Formulaire pour ajouter ou modifier un produit.
    """
    class Meta:
        model = Produit
        fields = ['categorie', 'nom', 'prix', 'quantite', 'photo', 'description', 'saisonnalite']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'saisonnalite': forms.TextInput(
                attrs={'placeholder': 'Ex: disponible de juin à septembre'}
            ),
        }

class AvisForm(forms.ModelForm):
    """
    Formulaire pour ajouter des avis sur les produits.
    """
    class Meta:
        model = Avis
        fields = ['note', 'commentaire']
        widgets = {
            'note': forms.RadioSelect(choices=Avis.NOTE_CHOICES),
            'commentaire': forms.Textarea(attrs={'rows': 3}),
        }


class ContactVendeurForm(forms.Form):
    sujet = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Objet de votre message'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 5,
            'placeholder': 'Votre message au vendeur...'
        })
    )
