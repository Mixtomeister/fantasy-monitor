from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet

from .models import Team, Player, PlayerUpdate, PlayerPoints

class PlayerTeamListFilter(admin.SimpleListFilter):
    title = "Team"
    parameter_name = 'team'
    def lookups(self, request, model_admin):
        for team in Team.objects.all().order_by('name'):
            yield (team.id, team.name)

    def queryset(self, request, queryset):
        print(self.value())

class TeamAdmin(admin.ModelAdmin):
    search_fields = ('name', 'shortName', 'teamId')

class PlayerAdmin(admin.ModelAdmin):
    list_filter = [PlayerTeamListFilter]
    search_fields = ('name', 'shortName', 'playerId')

class PlayerUpdateAdmin(admin.ModelAdmin):
    list_display = ('player_name_field', 'team', 'position', 'date', 'market_value', 'status')
    list_filter = ('team__name', 'position', 'date', 'status')
    search_fields = ('player__name', 'player__shortName', 'player__playerId')

    def player_name_field(self, obj):
        return f'{obj.player.name} ({obj.player.shortName})'
    player_name_field.allow_tags = True
    player_name_field.short_description = "Player Name"

class PlayerPointsAdmin(admin.ModelAdmin):
    list_display = ('player', 'round', 'points', 'idealXI')
    list_filter = ['round', 'idealXI']

# Register your models here.
admin.site.register(Team, TeamAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(PlayerUpdate, PlayerUpdateAdmin)
admin.site.register(PlayerPoints, PlayerPointsAdmin)