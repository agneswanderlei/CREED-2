from django.contrib import admin
from .models import (
    States,
    Tipo_documento,
    Presos,
    Institution,
    PostGrad,
)


class StatesAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class TipoAdmin(admin.ModelAdmin):
    list_display = ('tipos',)
    search_fields = ('tipos',)


class PresosAdmin(admin.ModelAdmin):
    list_display = (
        'number_doc',
        'type_doc',
        'name_full',
        'state_origin',
        'institutions'
    )
    search_fields = ('institutions__name', 'name_full')


class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class PostGradAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )


admin.site.register(States, StatesAdmin)
admin.site.register(Tipo_documento, TipoAdmin)
admin.site.register(Presos, PresosAdmin)
admin.site.register(Institution, InstitutionAdmin)
admin.site.register(PostGrad, PostGradAdmin)
