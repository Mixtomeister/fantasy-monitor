from django.db import models

# Create your models here.
class Team(models.Model):
    teamId = models.IntegerField()
    name = models.CharField(max_length=32)
    shortName = models.CharField(max_length=3)
    slug = models.SlugField(max_length=32)

    def __str__(self):
        return self.name


class Player(models.Model):
    playerId = models.IntegerField()
    name = models.CharField(max_length=64)
    shortName = models.CharField(max_length=32)
    slug = models.SlugField(max_length=32)
    lastSeasonPoints = models.IntegerField()

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
        current = PlayerUpdate.objects.filter(player=self).latest().market_value
        prev = PlayerUpdate.objects.filter(player=self).latest().get_next_in_order().market_value

        return current - prev

    @property
    def status(self):
        return PlayerUpdate.objects.filter(player=self).latest().status

    @property
    def total_points(self):
        return PlayerPoints.objects.filter(player=self).aggregate(total=models.Sum('points')).total

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
    date = models.DateField(auto_now_add=True)
    market_value = models.IntegerField()
    status = models.CharField(max_length=12, choices=PlayerStatus)

    def __str__(self):
        return f'[{self.date.strftime('%Y-%m-%d')}] [{self.team.name}] {self.player.name}'
    
    class Meta:
        get_latest_by = "-date"

class PlayerPoints(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    round = models.IntegerField()
    points = models.IntegerField()
    idealXI = models.BooleanField()

    def __str__(self):
        return f'[Week {self.round}] {self.player.name} ({self.points})'
