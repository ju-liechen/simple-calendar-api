from datetime import datetime
from django.db.models import Q
from django.shortcuts import get_object_or_404
from ninja import Schema, FilterSchema as NinjaFilterSchema, Query
from typing import Optional, List
from uuid import UUID

from apps.schedule.models import Event
from project.api import api

PATH = '/user/schedule/events'
NAME = 'user-events'


class UserEventsOut(Schema):
    id: UUID
    title: str
    start_date_time: datetime
    end_date_time: datetime
    description: Optional[str]
    location: Optional[str]
    url: Optional[str]


class UserEventsDeleteOut(Schema):
    pass


class UserEventsIn(Schema):
    title: str
    start_date_time: datetime
    end_date_time: datetime
    description: Optional[str] = ''
    location: Optional[str] = ''
    url: Optional[str] = ''


class UserEventsDetailIn(Schema):
    title: Optional[str] = ''
    start_date_time: Optional[datetime] = ''
    end_date_time: Optional[datetime] = ''
    description: Optional[str] = ''
    location: Optional[str] = ''
    url: Optional[str] = ''


class FilterSchema(NinjaFilterSchema):
    date: Optional[str] = None
    month: Optional[int] = None
    year: Optional[int] = None

    def filter_date(self, value: str) -> Q:
        q = Q()
        if value:
            try:
                parsed_date = datetime.strptime(value, '%Y-%m-%d').date()
                q &= (Q(start_date_time__date=parsed_date) | Q(end_date_time__date=parsed_date))
            except ValueError:
                raise ValueError(f"Invalid date format: {value}. Expected format: 'YYYY-MM-DD'")
        return q

    def filter_month(self, value: str) -> Q:
        q = Q()
        if value:
            q &= (Q(start_date_time__month=value) | Q(end_date_time__month=value))
        return q

    def filter_year(self, value: str) -> Q:
        q = Q()
        if value:
            q &= (Q(start_date_time__year=value) | Q(end_date_time__year=value))
        return q


@api.get(PATH, url_name=NAME, response=List[UserEventsOut])
def user_events_get(request, filters: FilterSchema = Query()):
    events = Event.objects.filter(user=request.user).order_by('-start_date_time')
    return filters.filter(events)


@api.post(PATH, url_name=NAME, response=UserEventsOut)
def user_events_post(request, data: UserEventsIn):
    data_dict = data.dict(exclude_unset=True)
    event = Event.objects.create(user=request.user, **data_dict)
    return event


@api.get(PATH + "/{event_id}", url_name=f"{NAME}-detail", response=UserEventsOut)
def user_events_get_detail(request, event_id):
    return get_object_or_404(Event, id=event_id)


@api.patch(PATH + "/{event_id}", url_name=f"{NAME}-detail", response=UserEventsOut)
def user_events_patch_detail(request, event_id, data: UserEventsDetailIn):
    event = get_object_or_404(Event, id=event_id)
    for (key, value) in data.dict(exclude_unset=True).items():
        setattr(event, key, value)
    event.save()
    return event


@api.delete(PATH + "/{event_id}", url_name=f"{NAME}-detail", response=UserEventsDeleteOut)
def user_events_delete_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    return {}
