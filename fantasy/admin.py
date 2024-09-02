from django.contrib import admin

from .models import Team, Player, PlayerUpdate, PlayerPoints


class PlayerUpdateAdmin(admin.ModelAdmin):
    list_display = ('player', 'team', 'position', 'date', 'market_value', 'status')
    list_filter = ('team__name', 'position', 'date', 'status')

class PlayerPointsAdmin(admin.ModelAdmin):
    list_display = ('player', 'round', 'points', 'idealXI')
    list_filter = ['round', 'idealXI']

# Register your models here.
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(PlayerUpdate, PlayerUpdateAdmin)
admin.site.register(PlayerPoints, PlayerPointsAdmin)