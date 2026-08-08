from django.shortcuts import render
from rest_framework import generics

from .models import AccessRequest
from .serializers import AccessRequestSerializer

class AccessRequestListCreateView(generics.ListCreateAPIView):
    queryset = AccessRequest.objects.all()
    serializer_class = AccessRequestSerializer