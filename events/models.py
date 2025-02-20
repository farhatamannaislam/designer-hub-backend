from django.db import models
from django.contrib.auth.models import User
from datetime import date
from taggit.managers import TaggableManager
from django.utils.timezone import now  # ✅ Import now correctly
from django.core.exceptions import ValidationError  # ✅ Import ValidationError

class Event(models.Model):
    """
    Event model, related to 'owner', i.e. a User instance.
    """

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=False)
    event_date = models.DateField(blank=False)
    tags = TaggableManager(blank=True)
    image = models.ImageField(
        upload_to="images/", default="../eventsdefault_n2yze8", blank=False
    )

    class Meta:
        ordering = ["-created_at"]

    def clean(self):
        """Prevent past dates for events."""
        if self.event_date < now().date():  # ✅ Ensure now() is correctly imported
            raise ValidationError("❌ ERROR: Event date cannot be in the past!")

    def save(self, *args, **kwargs):
        """Run validation before saving."""
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} {self.title}"

