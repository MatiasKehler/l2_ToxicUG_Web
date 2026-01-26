from django.contrib import admin
from .models import Perfil, HistorialDKP

# --- ACCIONES PERSONALIZADAS ---

@admin.action(description='🎁 Dar 100 DKP (Bonus Raid)')
def dar_bonus_raid(modeladmin, request, queryset):
    # 'queryset' es la lista de todos los jugadores que seleccionaste con el tilde
    for perfil_jugador in queryset:
        # Creamos una entrada en el historial para cada uno
        HistorialDKP.objects.create(
            perfil=perfil_jugador,
            evento="Bonus Raid (Masivo)",
            cantidad=100
        )
    # Mensaje de éxito en la pantalla (la barrita verde arriba)
    modeladmin.message_user(request, f"Se han entregado 100 DKP a {queryset.count()} jugadores.")

@admin.action(description='⚠️ Multa por Toxicidad (-50 DKP)')
def aplicar_multa(modeladmin, request, queryset):
    for perfil_jugador in queryset:
        HistorialDKP.objects.create(
            perfil=perfil_jugador,
            evento="Sanción disciplinaria",
            cantidad=-50
        )
    modeladmin.message_user(request, f"Se ha multado a {queryset.count()} jugadores.")

# --- CONFIGURACIÓN DEL ADMIN ---

class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rango', 'dkp_actuales', 'asistencia_porcentaje')
    search_fields = ('usuario__username',)
    list_filter = ('rango',) # Agregué filtro por Rango (útil para filtrar solo "Miembros")
    
    # AQUÍ REGISTRAMOS LAS ACCIONES NUEVAS
    actions = [dar_bonus_raid, aplicar_multa]

class HistorialAdmin(admin.ModelAdmin):
    list_display = ('perfil', 'evento', 'cantidad', 'fecha')
    list_filter = ('fecha', 'evento') # Agregué filtro por evento

# Registros
admin.site.register(Perfil, PerfilAdmin)
admin.site.register(HistorialDKP, HistorialAdmin)