from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from designerhub.permissions import IsOwnerOrReadOnly
from .models import Event
from .serializers import EventSerializer

class EventList(generics.ListCreateAPIView):
    """
    List events or create an event if logged in.
    """
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Event.objects.all().order_by("-created_at")
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = {
        "owner__followed__owner__profile": ["exact"],
        "owner__profile": ["exact"],
        'event_date': ['lte'],
    }
    search_fields = [
        "owner__username",
        "title",
        "event_date",
        "tags__name",
    ]
    ordering_fields = []

    def perform_create(self, serializer):
        """
        Ensure the event date is not in the past before saving.
        """
        from datetime import date
        from rest_framework.exceptions import ValidationError

        event_date = serializer.validated_data.get("event_date")
        if event_date and event_date < date.today():
            raise ValidationError({"event_date": "Event date cannot be in the past!"})

        serializer.save(owner=self.request.user)

class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve an event and edit or delete it if you own it.
    """
    serializer_class = EventSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Event.objects.all().order_by("-created_at")

