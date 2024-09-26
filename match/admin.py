from django.contrib import admin

from match.models import Stadium, Match, Team, Seat, SeatAssignment


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


class SeatAssignmentInline(admin.TabularInline):
    model = SeatAssignment
    extra = 0

    def get_formset(self, request, obj=None,
                    **kwargs):  # showing only the seats of match's stadium
        formset = super().get_formset(request, obj, **kwargs)
        if obj:
            formset.form.base_fields['seat'].queryset = Seat.objects.filter(stadium=obj.stadium_id)
        return formset


class MatchAdmin(admin.ModelAdmin):
    _fields = ['home_team', 'away_team', 'datetime', 'stadium']
    list_display = _fields
    fields = _fields
    inlines = [SeatAssignmentInline]


admin.site.register(Stadium, StadiumAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Match, MatchAdmin)
