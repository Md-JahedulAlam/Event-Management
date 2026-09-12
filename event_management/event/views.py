from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import viewsets
# from rest_framework.permissions import AllowAny
from .permissions import IsAdminOrReadOnly

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [IsAdminOrReadOnly]


class EventsViewsets(viewsets.ModelViewSet):
    queryset = Events.objects.all()
    serializer_class = EventSerializers
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['title']
    ordering_fields=['price', 'event_date']