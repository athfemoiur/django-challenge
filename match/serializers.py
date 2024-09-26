from rest_framework import serializers

from match.models import Stadium, Match, Team


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
