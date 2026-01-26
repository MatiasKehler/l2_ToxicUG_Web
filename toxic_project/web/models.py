from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# 1. PERFIL DEL JUGADOR
class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    discord_id = models.CharField(max_length=100, blank=True, null=True)
    avatar_url = models.URLField(max_length=500, blank=True, null=True)
    
    # Datos del Juego
    rango = models.CharField(max_length=50, default="Miembro")
    dkp_actuales = models.IntegerField(default=0)
    
    # Estadísticas
    asistencia_porcentaje = models.IntegerField(default=0)
    eventos_participados = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.usuario.username} | DKP: {self.dkp_actuales}"

# 2. HISTORIAL DE PUNTOS
class HistorialDKP(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    evento = models.CharField(max_length=200) 
    cantidad = models.IntegerField() 
    
    def __str__(self):
        signo = "+" if self.cantidad > 0 else ""
        return f"{self.perfil.usuario.username}: {self.evento} ({signo}{self.cantidad})"

# --- ZONA DE AUTOMATIZACIÓN ---

@receiver(post_save, sender=HistorialDKP)
def sumar_puntos(sender, instance, created, **kwargs):
    """
    Se activa automáticamente cuando CREAS un nuevo historial.
    Suma (o resta) la cantidad al perfil del usuario.
    """
    if created: # Solo si es un registro nuevo
        perfil = instance.perfil
        perfil.dkp_actuales += instance.cantidad
        perfil.save()

@receiver(post_delete, sender=HistorialDKP)
def restar_puntos_al_borrar(sender, instance, **kwargs):
    """
    Si borras un historial por error, esto deshace la operación
    para que los puntos vuelvan a estar bien.
    """
    perfil = instance.perfil
    perfil.dkp_actuales -= instance.cantidad
    perfil.save()