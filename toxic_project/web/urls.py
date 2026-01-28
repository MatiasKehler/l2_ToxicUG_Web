from django.urls import path
from . import views
from .views import CustomLoginView

urlpatterns = [
    # Portada
    path('', views.index, name='index'),
    
    # Área Privada
    path('panel/', views.panel, name='panel'),
    
    # Autenticación (Usamos nuestra vista personalizada con seguridad)
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', views.salir, name='logout'),
]