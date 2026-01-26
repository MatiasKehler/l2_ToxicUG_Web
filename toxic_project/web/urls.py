from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Portada
    path('', views.index, name='index'),
    
    # Área Privada (Cambiamos 'panel.html' por 'panel/' para que sea más elegante)
    path('panel/', views.panel, name='panel'),
    
    # Autenticación
    path('login/', auth_views.LoginView.as_view(template_name='web/login.html'), name='login'),
    path('logout/', views.salir, name='logout'),
]