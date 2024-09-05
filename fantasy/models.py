from django.db import models

# Create your models here.
class Team(models.Model):
    team_api_id = models.IntegerField()
    name = models.CharField(max_length=32)
    short_name = models.CharField(max_length=3)
    slug = models.SlugField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Player(models.Model):
    player_api_id = models.IntegerField()
    name = models.CharField(max_length=64)
    short_name = models.CharField(max_length=32)
    slug = models.SlugField(max_length=32)
    last_season_points = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def team(self):
        return PlayerUpdate.objects.filter(player=self).latest().team

    @property
    def position(self):
        return PlayerUpdate.objects.filter(player=self).latest().position

    @property
    def market_value(self):
        return PlayerUpdate.objects.filter(player=self).latest().market_value

    @property
    def market_value_variation(self):
        updates = PlayerUpdate.objects.filter(player=self).order_by('-date')[0:2]
        if len(updates) == 2:
            current = updates[0].market_value
            prev = updates[1].market_value

            return current - prev
        else:
            return None

    @property
    def status(self):
        return PlayerUpdate.objects.filter(player=self).latest().status

    @property
    def total_points(self):
        return PlayerPoints.objects.filter(player=self).aggregate(total=models.Sum('points'))['total']

    def __str__(self):
        return self.name

class PlayerStatus(models.TextChoices):
    SUSPENDED = 'suspended', 'Suspended'
    INJURED = 'injured', 'Injured'
    AVAILABLE = 'ok', 'Available'
    DOUBTFUL = 'doubtful', 'Doubtful'
    UNKNOWN = 'unknown', 'Unknown'

class PlayerPosition(models.IntegerChoices):
    GOALKEEPER = 1, 'Goalkeeper'
    DEFENDER = 2, 'Defender'
    MIDFIELDER = 3, 'Midfielder'
    STRIKER = 4, 'Striker'
    MANAGER = 5, 'Manager'

class PlayerUpdate(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.RESTRICT, null=True)
    position = models.IntegerField(choices=PlayerPosition)
    date = models.DateField()
    market_value = models.IntegerField()
    status = models.CharField(max_length=12, choices=PlayerStatus)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'[{self.date.strftime('%Y-%m-%d')}] [{self.team.name}] {self.player.name}'
    
    class Meta:
        get_latest_by = "date"

class PlayerPoints(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.RESTRICT, null=True)
    position = models.IntegerField(choices=PlayerPosition)
    round = models.IntegerField()
    points = models.IntegerField()
    ideal_xi = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'[Week {self.round}] {self.player.name} ({self.points})'
