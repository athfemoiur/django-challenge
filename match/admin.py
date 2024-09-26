from django.contrib import admin

from match.models import Stadium, Match, Team, Seat


class SeatInline(admin.TabularInline):
    model = Seat
    extra = 0


class StadiumAdmin(admin.ModelAdmin):
    _fields = ['name']
    list_display = _fields
    fields = _fields
    inlines = [SeatInline]


class TeamAdmin(admin.ModelAdmin):
    _fields = ['name']
    list_display = _fields
    fields = _fields


class MatchAdmin(admin.ModelAdmin):
    _fields = ['home_team', 'away_team', 'datetime', 'stadium']
    list_display = _fields
    fields = _fields


admin.site.register(Stadium, StadiumAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Match, MatchAdmin)
