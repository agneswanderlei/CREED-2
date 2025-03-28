from django.contrib import admin
from .models import Oficios
# Register your models here.


class OficiosAdmin(admin.ModelAdmin):
    list_display = ('n_oficios',)
    search_fields = ('n_oficios', )


admin.site.register(Oficios, OficiosAdmin)
