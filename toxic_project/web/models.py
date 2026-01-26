from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# --- 1. PERFIL DEL JUGADOR ---
class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuario")
    discord_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="ID Discord")
    avatar_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="Link Avatar")
    
    # Datos del Juego
    rango = models.CharField(max_length=50, default="Miembro", verbose_name="Rango del Clan")
    dkp_actuales = models.IntegerField(default=0, verbose_name="Puntos DKP")
    
    # Estadísticas
    asistencia_porcentaje = models.IntegerField(default=0, verbose_name="% Asistencia")
    eventos_participados = models.IntegerField(default=0, verbose_name="Raids Totales")

    class Meta:
        verbose_name = "Perfil de Jugador"
        verbose_name_plural = "Perfiles de Jugadores"

    def __str__(self):
        return f"{self.usuario.username} [{self.dkp_actuales} DKP]"

# --- 2. HISTORIAL DE PUNTOS ---
class HistorialDKP(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, verbose_name="Jugador")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y Hora")
    evento = models.CharField(max_length=200, verbose_name="Motivo / Evento") 
    cantidad = models.IntegerField(verbose_name="Cantidad de Puntos") 
    
    class Meta:
        verbose_name = "Registro de Historial"
        verbose_name_plural = "Historial de Puntos"
        ordering = ['-fecha'] # Ordena siempre del más reciente al más antiguo

    def __str__(self):
        signo = "+" if self.cantidad > 0 else ""
        return f"{self.perfil.usuario.username}: {self.evento} ({signo}{self.cantidad})"

# --- ZONA DE AUTOMATIZACIÓN (SIGNALS) ---

@receiver(post_save, sender=HistorialDKP)
def sumar_puntos(sender, instance, created, **kwargs):
    """Actualiza el saldo del perfil al crear un registro nuevo."""
    if created:
        perfil = instance.perfil
        perfil.dkp_actuales += instance.cantidad
        perfil.save()

@receiver(post_delete, sender=HistorialDKP)
def restar_puntos_al_borrar(sender, instance, **kwargs):
    """Revierte la operación si borras un registro del historial."""
    perfil = instance.perfil
    perfil.dkp_actuales -= instance.cantidad
    perfil.save()