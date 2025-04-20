from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import CustomUser, AuditLog

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('codigo_usuario',)}),  # Tupla válida com vírgula
    )
    list_display = ('username', 'email', 'codigo_usuario', 'is_staff', 'is_active')  # Exibe os campos na tabela

class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'description', 'timestamp')  # Campos exibidos na tabela
    list_filter = ('action', 'timestamp')  # Filtros laterais
    search_fields = ('user__username', 'action', 'description')  # Campos pesquisáveis
    ordering = ('-timestamp',)  # Ordenação padrão (mais recente primeiro)



# Registrar o modelo no admin
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(AuditLog, AuditLogAdmin)
