from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint

User = get_user_model()


class Team(models.Model):
    name = models.CharField(unique=True, max_length=80)

    def __str__(self):
        return self.name


class Stadium(models.Model):
    name = models.CharField(unique=True, max_length=80)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Match(models.Model):
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')
    datetime = models.DateTimeField()
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.home_team} vs {self.away_team}'


class Seat(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='seats')
    number = models.PositiveIntegerField()
    is_reserved = models.BooleanField(default=False)
    reserver_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['match', 'number'], name='unique_match_number')
        ]

    def __str__(self):
        return f'{self.match}: NO.{self.number} reserved: {self.is_reserved}'
