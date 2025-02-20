from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.timezone import now
from datetime import date  # ✅ Import globally
from rest_framework.exceptions import ValidationError
from designerhub.permissions import IsOwnerOrReadOnly
from .models import Event
from .serializers import EventSerializer

class EventList(generics.ListCreateAPIView):
    """
    List events or create an event if logged in.
    """
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # ✅ Only allow events that are in the present or future
    queryset = Event.objects.filter(event_date__gte=now().date()).order_by("-event_date")

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = {
        "owner__followed__owner__profile": ["exact"],
        "owner__profile": ["exact"],
        "event_date": ["gte"],  # ✅ Only allow future or present events
    }
    search_fields = [
        "owner__username",
        "title",
        "description",  # ✅ Allow searching in description
        "tags__name",
    ]
    ordering_fields = ["event_date", "created_at"]  # ✅ Define proper ordering

    def perform_create(self, serializer):
        """
        Ensure the event date is not in the past before saving.
        """
        event_date = serializer.validated_data.get("event_date")
        if event_date and event_date < date.today():
            raise ValidationError({"event_date": "❌ ERROR: Event date cannot be in the past!"})

        serializer.save(owner=self.request.user)

class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve an event and edit or delete it if you own it.
    """
    serializer_class = EventSerializer
    permission_classes = [IsOwnerOrReadOnly]

    # ✅ Ensure that only future or present events can be accessed
    queryset = Event.objects.filter(event_date__gte=now().date()).order_by("-event_date")


