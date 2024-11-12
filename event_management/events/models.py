from django.db import models

from event_management.users.models import User

# Create your models here.


class UserEvents(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=100)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    attendees = models.ManyToManyField(
        User,
        related_name="events_attending",
        blank=True,
    )

    def __str__(self):
        return self.title
