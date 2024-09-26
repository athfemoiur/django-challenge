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

    def __str__(self):
        return self.name


class Match(models.Model):
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')
    datetime = models.DateTimeField()
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Matches'

    def __str__(self):
        return f'{self.home_team} vs {self.away_team}'


class Seat(models.Model):
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE, related_name='seats')
    row = models.PositiveIntegerField()
    number = models.PositiveIntegerField()

    class Meta:
        constraints = [
            UniqueConstraint(fields=['stadium', 'row', 'number'], name='unique_stadium_row_number')
        ]

    def __str__(self):
        return f'{self.number}-{self.number}'

class SeatAssignment(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='seat_assignments')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    is_reserved = models.BooleanField(default=False)
    reserver_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reserved_seats')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['match', 'seat'], name='unique_match_seat')
        ]

    def __str__(self):
        return f'{self.match}-{self.seat}'