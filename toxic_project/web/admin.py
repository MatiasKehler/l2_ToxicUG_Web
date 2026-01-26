from django.contrib import admin
from .models import Perfil, HistorialDKP

# --- ACCIONES MASIVAS (ACTIONS) ---

@admin.action(description='🎁 Dar 100 DKP (Bonus Raid)')
def dar_bonus_raid(modeladmin, request, queryset):
    count = 0
    for perfil in queryset:
        HistorialDKP.objects.create(
            perfil=perfil,
            evento="Bonus Raid (Masivo)",
            cantidad=100
        )
        count += 1
    modeladmin.message_user(request, f"¡Éxito! Se entregaron 100 DKP a {count} jugadores.")

@admin.action(description='⚠️ Multa por Toxicidad (-50 DKP)')
def aplicar_multa(modeladmin, request, queryset):
    count = 0
    for perfil in queryset:
        HistorialDKP.objects.create(
            perfil=perfil,
            evento="Sanción disciplinaria",
            cantidad=-50
        )
        count += 1
    modeladmin.message_user(request, f"Se aplicó la multa a {count} jugadores.")

# --- CONFIGURACIÓN DE TABLAS ---

class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rango', 'dkp_actuales', 'asistencia_porcentaje')
    search_fields = ('usuario__username', 'discord_id')
    list_filter = ('rango', 'asistencia_porcentaje')
    actions = [dar_bonus_raid, aplicar_multa]
    list_per_page = 20 # Paginación para que no sea una lista infinita

class HistorialAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'perfil', 'evento', 'cantidad')
    list_filter = ('fecha', 'evento')
    search_fields = ('perfil__usuario__username', 'evento')
    date_hierarchy = 'fecha' # Agrega una barra de navegación por fechas arriba

# --- REGISTRO ---
admin.site.register(Perfil, PerfilAdmin)
admin.site.register(HistorialDKP, HistorialAdmin)