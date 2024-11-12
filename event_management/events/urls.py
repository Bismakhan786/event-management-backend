from django.urls import path

from event_management.events.views import all_events
from event_management.events.views import create_event
from event_management.events.views import delete_event
from event_management.events.views import update_event

app_name = "events"
urlpatterns = [
    path("all-events/", view=all_events, name="all_events"),
    path("create-event/", view=create_event, name="create_event"),
    path("delete-event/<id>/", view=delete_event, name="delete_event"),
    path("update-event/<id>/", view=update_event, name="update_event"),
]
