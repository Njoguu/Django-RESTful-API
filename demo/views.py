from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import developers
from .serializers import developersSerializer

# Create your views here.
class developerList(APIView):
    def get(self, request):
        devs = developers.objects.all()
        serializer = developersSerializer(devs, many=True)

        return Response(serializer.data)

    def post(self):
        pass
