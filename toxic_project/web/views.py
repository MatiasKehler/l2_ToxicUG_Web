from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from .models import Perfil, HistorialDKP

# ========================================================
# 1. VISTAS DE AUTENTICACIÓN (CLASES)
# ========================================================

class CustomLoginView(LoginView):
    """
    Vista de Login personalizada con seguridad anti-bruteforce.
    - Máximo 3 intentos.
    - Bloqueo de 5 minutos.
    - Mensajes de advertencia dinámicos.
    """
    template_name = 'web/login.html'

    def dispatch(self, request, *args, **kwargs):
        # A. VERIFICAR SI ESTÁ BLOQUEADO POR TIEMPO
        blocked_time_str = request.session.get('login_blocked_until')
        
        if blocked_time_str:
            blocked_until = timezone.datetime.fromisoformat(blocked_time_str)
            # Si la fecha actual es MENOR a la de desbloqueo, sigue bloqueado
            if timezone.now() < blocked_until:
                remaining_minutes = int((blocked_until - timezone.now()).total_seconds() / 60) + 1
                messages.error(request, f"🔒 Sistema bloqueado por seguridad. Espera {remaining_minutes} minutos.")
                return render(request, self.template_name, {'form': self.get_form()})
            else:
                # Si ya pasó el tiempo, desbloqueamos silenciosamente
                self._reset_login_attempts(request)

        return super().dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        # B. GESTIÓN DE INTENTOS FALLIDOS
        attempts = self.request.session.get('login_attempts', 0) + 1
        self.request.session['login_attempts'] = attempts
        
        limit = 3
        remaining = limit - attempts

        if attempts >= limit:
            # CASO: BLOQUEO
            block_time = timezone.now() + timedelta(minutes=5)
            self.request.session['login_blocked_until'] = block_time.isoformat()
            messages.error(self.request, "🚫 Has excedido los 3 intentos. Acceso bloqueado por 5 minutos.")
        else:
            # CASO: ADVERTENCIA (CONTADOR REGRESIVO)
            msg_text = f"Te queda 1 intento." if remaining == 1 else f"Te quedan {remaining} intentos."
            messages.warning(self.request, f"Credenciales incorrectas. ⚠️ {msg_text}")

        return super().form_invalid(form)

    def form_valid(self, form):
        # C. ÉXITO: RESETEAR CONTADORES
        # Si entra correctamente, borramos su historial de fallos
        self._reset_login_attempts(self.request)
        return super().form_valid(form)

    def _reset_login_attempts(self, request):
        """Método auxiliar para limpiar la sesión."""
        if 'login_attempts' in request.session:
            del request.session['login_attempts']
        if 'login_blocked_until' in request.session:
            del request.session['login_blocked_until']


# ========================================================
# 2. VISTAS FUNCIONALES (PÁGINAS)
# ========================================================

def index(request):
    """Vista de la portada pública."""
    return render(request, 'web/index.html')

@login_required
def panel(request):
    """
    Panel principal de usuario.
    Muestra estadísticas y movimientos DKP.
    """
    context = {}
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
        # Error controlado: Usuario sin perfil de juego
        context['error'] = 'Tu cuenta no tiene un Perfil de Jugador activo. Contacta a un Administrador.'
    
    return render(request, 'web/panel.html', context)

def salir(request):
    """Cierra sesión y redirige a la portada."""
    logout(request)
    return redirect('index')