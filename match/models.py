from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models, transaction
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
        return f'{self.row}-{self.number}'


class SeatAssignment(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='seat_assignments')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    is_reserved = models.BooleanField(default=False)
    reserved_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                                    related_name='reserved_seats')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['match', 'seat'], name='unique_match_seat')
        ]

    def __str__(self):
        return f'{self.match}-{self.seat}'

    def clean(self):
        if self.seat.stadium != self.match.stadium:
            raise ValidationError("The seat's stadium does not match the match's stadium.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    @classmethod
    def reserve(cls, seat_assignment_id: int, user: User) -> bool:
        with transaction.atomic(): # for handling race-conditions on the db level
            seat_assignment = SeatAssignment.objects.select_for_update().get(id=seat_assignment_id)
            if seat_assignment.is_reserved:
                return False
            seat_assignment.is_reserved = True
            seat_assignment.reserved_by = user
            seat_assignment.save(update_fields=['is_reserved', 'reserved_by'])
            return True
