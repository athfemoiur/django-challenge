from django.db import transaction
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from match.models import Stadium, Match, SeatAssignment, Seat
from match.serializers import StadiumSerializer, MatchSerializer, SeatSerializer, \
    SeatAssignmentSerializer


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


class StadiumSeatsView(APIView):
    def get(self, request, stadium_id: int):
        stadium = get_object_or_404(Stadium, pk=stadium_id)
        seats = Seat.objects.filter(stadium=stadium)
        serializer = SeatSerializer(seats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, stadium_id: int):
        stadium = get_object_or_404(Stadium, pk=stadium_id)
        request_data = [{'stadium_id': stadium.id, **_data} for _data in request.data]
        serializer = SeatSerializer(data=request_data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MatchSeatsView(APIView):
    def get(self, request, match_id: int):
        match = get_object_or_404(Match, pk=match_id)
        seats = SeatAssignment.objects.filter(match=match)
        serializer = SeatAssignmentSerializer(seats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, match_id: int):
        match = get_object_or_404(Match, pk=match_id)
        request_data = [{'match_id': match.id, **_data} for _data in request.data]
        serializer = SeatAssignmentSerializer(data=request_data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReserveSeatView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, match_id: int):
        seat_id = request.data.get('seat_id')
        seat_assignment = get_object_or_404(SeatAssignment, match_id=match_id, seat_id=seat_id)
        success = SeatAssignment.reserve(seat_assignment.id, request.user)
        if success:
            return Response({}, status=status.HTTP_200_OK)

        return Response({'code': 'already-reserved'}, status=status.HTTP_409_CONFLICT)
