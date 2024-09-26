from django.contrib import admin

from match.models import Stadium


class StadiumAdmin(admin.ModelAdmin):
    _fields = ['name', 'capacity']
    list_display = _fields
    fields = _fields


admin.site.register(Stadium, StadiumAdmin)
