from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('agritech_app.urls')),
    path('accounts/', include('django.contrib.auth.urls')),   # Pour les vues d'authentification par défaut
    path('accounts/profile/', include('agritech_app.urls')),  # Redirige vers votre vue profile# URLs pour la connexion, déconnexion, etc.
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)