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
        if self.value():
            player_ids = Player.objects.filter(
                playerupdate__team_id=self.value()
            ).distinct().values_list('id', flat=True)

            return queryset.filter(id__in=player_ids)

class TeamAdmin(admin.ModelAdmin):
    search_fields = ('name', 'short_name', 'team_api_id')

class PlayerAdmin(admin.ModelAdmin):
    list_filter = [PlayerTeamListFilter]
    search_fields = ('name', 'short_name', 'player_api_id')

class PlayerUpdateAdmin(admin.ModelAdmin):
    list_display = ('player_name_field', 'team', 'position', 'date', 'market_value', 'status')
    list_filter = ('team__name', 'position', 'date', 'status')
    search_fields = ('player__name', 'player__short_name', 'player__player_api_id')

    def player_name_field(self, obj):
        return f'{obj.player.name} ({obj.player.short_name})'
    player_name_field.allow_tags = True
    player_name_field.short_description = "Player Name"

class PlayerPointsAdmin(admin.ModelAdmin):
    list_display = ('player', 'round', 'points', 'ideal_xi')
    list_filter = ['round', 'ideal_xi']
    search_fields = ["player__name"]

# Register your models here.
admin.site.register(Team, TeamAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(PlayerUpdate, PlayerUpdateAdmin)
admin.site.register(PlayerPoints, PlayerPointsAdmin)