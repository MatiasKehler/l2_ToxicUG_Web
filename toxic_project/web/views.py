from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Perfil, HistorialDKP

def index(request):
    return render(request, 'web/index.html')

# --- EL PORTERO DE SEGURIDAD ---
# Esta línea dice: "Si no está logueado, mándalo a /admin/"
@login_required
def panel(request):
    try:
        # 1. Buscamos el perfil del usuario conectado
        perfil_usuario = Perfil.objects.get(usuario=request.user)
        
        # 2. Buscamos sus últimos 5 movimientos
        historial = HistorialDKP.objects.filter(perfil=perfil_usuario).order_by('-fecha')[:5]

        # 3. Empaquetamos los datos
        context = {
            'perfil': perfil_usuario,
            'historial': historial
        }
        return render(request, 'web/panel.html', context)
    
    except Perfil.DoesNotExist:
        # Si el usuario existe pero no tiene perfil creado en la base de datos
        return render(request, 'web/panel.html', {'error': 'Perfil no encontrado.'})

def salir(request):
    logout(request) # Cierra la sesión
    return redirect('index') # Te manda a la portada