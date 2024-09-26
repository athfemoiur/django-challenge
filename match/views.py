from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from match.models import Stadium
from match.serializers import StadiumSerializer, MatchSerializer, SeatSerializer


class StadiumCreateView(APIView):
    def post(self, request):
        serializer = StadiumSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MatchCreateView(APIView):
    def post(self, request):
        serializer = MatchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AddSeatsToStadiumView(APIView):
    def post(self, request, stadium_id: int):
        stadium = get_object_or_404(Stadium, pk=stadium_id)
        request_data = [{'stadium_id': stadium.id, **_data} for _data in request.data]
        serializer = SeatSerializer(data=request_data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)