from typing import TYPE_CHECKING

from allauth.account.decorators import verified_email_required
from django import forms
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

if TYPE_CHECKING:
    from django.db.models import QuerySet

from event_management.events.models import UserEvents


class EventForm(forms.ModelForm):
    class Meta:
        model = UserEvents
        fields = ["title", "description", "date", "location"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Event Title"},
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Event Description",
                    "rows": 3,
                },
            ),
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "location": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Event Location"},
            ),
        }


def all_events(request: HttpRequest) -> HttpResponse:
    events: QuerySet[UserEvents] = UserEvents.objects.all()

    search_query: str | None = request.GET.get("search")
    if search_query:
        events = events.filter(title__icontains=search_query)

    context = {"events": events}
    return render(request, "events/all_events.html", context)


@verified_email_required
def create_event(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form: EventForm = EventForm(request.POST)
        if form.is_valid():
            event: UserEvents = form.save(commit=False)
            event.owner = request.user
            event.save()
            return redirect("/events/all-events/")
    else:
        form: EventForm = EventForm()

    context = {"form": form}
    return render(request, "events/create_event.html", context)


@verified_email_required
def update_event(request: HttpRequest, event_id: int) -> HttpResponse:
    event: UserEvents = get_object_or_404(UserEvents, id=event_id)

    if request.user != event.owner:
        return redirect("/403/")

    if request.method == "POST":
        form: EventForm = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect("/events/all-events")

    else:
        form: EventForm = EventForm(instance=event)

    context = {"form": form}
    return render(request, "events/update_event.html", context)


@verified_email_required
def delete_event(request: HttpRequest, event_id: int) -> HttpResponse:
    event: UserEvents = get_object_or_404(UserEvents, id=event_id)

    if request.user != event.owner:
        return redirect("/403/")

    event.delete()
    return redirect("/events/all-events/")
