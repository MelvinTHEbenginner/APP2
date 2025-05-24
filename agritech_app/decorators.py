"""
# Décorateur personnalisé pour les permissions

Pour mieux gérer les autorisations dans votre application, voici un ensemble de décorateurs personnalisés à ajouter dans un nouveau fichier `decorators.py` dans votre application:
"""

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from functools import wraps

def admin_required(view_func):
    """
    Décorateur pour vérifier si l'utilisateur est un administrateur Django (is_staff)
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Vous devez être connecté pour accéder à cette page.")
            return redirect('login')
        
        if not request.user.is_staff:
            messages.error(request, "Vous n'avez pas les droits administrateur nécessaires.")
            return redirect('home')
            
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def vendeur_confirme_required(view_func):
    """
    Décorateur pour vérifier si l'utilisateur est un vendeur confirmé
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Vous devez être connecté pour accéder à cette page.")
            return redirect('login')
        
        try:
            profile = request.user.profile
            if profile.role != 'vendeur' or not profile.is_vendeur_confirmed:
                messages.error(request, "Vous devez être un vendeur confirmé pour accéder à cette page.")
                return redirect('home')
        except:
            messages.error(request, "Profil utilisateur introuvable.")
            return redirect('home')
            
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def acheteur_required(view_func):
    """
    Décorateur pour vérifier si l'utilisateur est un acheteur
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Vous devez être connecté pour accéder à cette page.")
            return redirect('login')
        
        try:
            profile = request.user.profile
            if profile.role != 'acheteur':
                messages.error(request, "Cette page est réservée aux acheteurs.")
                return redirect('home')
        except:
            messages.error(request, "Profil utilisateur introuvable.")
            return redirect('home')
            
        return view_func(request, *args, **kwargs)
    return _wrapped_view