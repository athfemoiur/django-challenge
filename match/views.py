from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from match.models import Stadium, Match, SeatAssignment, Seat
from match.serializers import StadiumSerializer, MatchSerializer, SeatSerializer, \
    SeatAssignmentSerializer


class StadiumCreateView(APIView):

    @swagger_auto_schema(
        request_body=StadiumSerializer,
        responses={201: StadiumSerializer, 400: 'Validation Error'}
    )
    def post(self, request):
        serializer = StadiumSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MatchCreateView(APIView):

    @swagger_auto_schema(
        request_body=MatchSerializer,
        responses={201: MatchSerializer, 400: 'Validation Error'}
    )
    def post(self, request):
        serializer = MatchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StadiumSeatsView(APIView):

    @swagger_auto_schema(
        responses={200: SeatSerializer(many=True), 404: 'Not Found'}
    )
    def get(self, request, stadium_id: int):
        stadium = get_object_or_404(Stadium, pk=stadium_id)
        seats = Seat.objects.filter(stadium=stadium)
        serializer = SeatSerializer(seats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'row': openapi.Schema(type=openapi.TYPE_STRING),
                'number': openapi.Schema(type=openapi.TYPE_STRING),
            })
        ),
        responses={201: SeatSerializer(many=True), 400: 'Validation Error', 404: 'Not Found'}
    )
    def post(self, request, stadium_id: int):
        stadium = get_object_or_404(Stadium, pk=stadium_id)
        request_data = [{'stadium_id': stadium.id, **_data} for _data in request.data]
        serializer = SeatSerializer(data=request_data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MatchSeatsView(APIView):

    @swagger_auto_schema(
        responses={200: SeatAssignmentSerializer(many=True), 404: 'Not Found'}
    )
    def get(self, request, match_id: int):
        match = get_object_or_404(Match, pk=match_id)
        seats = SeatAssignment.objects.filter(match=match)
        serializer = SeatAssignmentSerializer(seats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'seat_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'is_reserved': openapi.Schema(type=openapi.TYPE_BOOLEAN),
            })
        ),
        responses={201: SeatAssignmentSerializer(many=True), 400: 'Validation Error',
                   404: 'Not Found'}
    )
    def post(self, request, match_id: int):
        match = get_object_or_404(Match, pk=match_id)
        request_data = [{'match_id': match.id, **_data} for _data in request.data]
        serializer = SeatAssignmentSerializer(data=request_data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReserveSeatView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'seat_id': openapi.Schema(type=openapi.TYPE_INTEGER,
                                          description='ID of the seat to reserve')
            }
        ),
        responses={
            200: 'Seat successfully reserved',
            409: 'Seat already reserved',
            404: 'Not Found'
        }
    )
    def post(self, request, match_id: int):
        seat_id = request.data.get('seat_id')
        seat_assignment = get_object_or_404(SeatAssignment, match_id=match_id, seat_id=seat_id)
        success = SeatAssignment.reserve(seat_assignment.id, request.user)
        if success:
            return Response({}, status=status.HTTP_200_OK)

        return Response({'code': 'already-reserved'}, status=status.HTTP_409_CONFLICT)
