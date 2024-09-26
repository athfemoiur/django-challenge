from rest_framework import serializers

from match.models import Stadium, Match, Team, Seat, SeatAssignment


class StadiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stadium
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class MatchSerializer(serializers.ModelSerializer):
    stadium = StadiumSerializer(read_only=True)
    stadium_id = serializers.PrimaryKeyRelatedField(queryset=Stadium.objects.all(),
                                                    source='stadium', write_only=True)
    home_team = TeamSerializer(read_only=True)
    home_team_id = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(),
                                                      source='home_team', write_only=True)
    away_team = TeamSerializer(read_only=True)
    away_team_id = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(),
                                                      source='away_team', write_only=True)

    class Meta:
        model = Match
        fields = ['id', 'home_team', 'home_team_id', 'away_team', 'away_team_id', 'datetime',
                  'stadium', 'stadium_id']


class SeatSerializer(serializers.ModelSerializer):
    stadium_id = serializers.PrimaryKeyRelatedField(queryset=Stadium.objects.all(),
                                                    source='stadium')

    class Meta:
        model = Seat
        fields = ['id', 'row', 'number', 'stadium_id']


class SeatAssignmentSerializer(serializers.ModelSerializer):
    match_id = serializers.PrimaryKeyRelatedField(queryset=Match.objects.all(),
                                                  source='match')
    seat_id = serializers.PrimaryKeyRelatedField(queryset=Seat.objects.all(),
                                                 source='seat')
    seat = SeatSerializer(read_only=True)

    class Meta:
        model = SeatAssignment
        fields = ['match_id', 'seat_id', 'seat', 'is_reserved', 'reserved_by']

    def validate(self, data):
        if data['seat'].stadium != data['match'].stadium:
            raise serializers.ValidationError("The seat's stadium does not match the match's stadium.")
        return data
