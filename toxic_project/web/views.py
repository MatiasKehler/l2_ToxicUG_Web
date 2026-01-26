from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Perfil, HistorialDKP

def index(request):
    """Vista de la portada pública."""
    return render(request, 'web/index.html')

@login_required
def panel(request):
    """
    Panel principal.
    Si el usuario no tiene perfil (porque el Admin no lo creó),
    muestra un mensaje de error en lugar de fallar o auto-crearlo.
    """
    try:
        # 1. Buscamos el perfil del usuario conectado
        perfil_usuario = Perfil.objects.get(usuario=request.user)
        
        # 2. Buscamos historial (Optimizado: Trae los últimos 10)
        historial = HistorialDKP.objects.filter(perfil=perfil_usuario).order_by('-fecha')[:10]

        context = {
            'perfil': perfil_usuario,
            'historial': historial
        }
    except Perfil.DoesNotExist:
        # CASO DE ERROR CONTROLADO:
        # Si el usuario existe en Django pero no tiene ficha de jugador.
        context = {
            'error': 'Tu cuenta no tiene un Perfil de Jugador activo. Contacta a un Administrador.'
        }
    
    return render(request, 'web/panel.html', context)

def salir(request):
    """Cierra sesión y redirige a la portada."""
    logout(request)
    return redirect('index')