from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from match.serializers import StadiumSerializer, MatchSerializer


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
