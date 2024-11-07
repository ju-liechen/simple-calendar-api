from datetime import date, timedelta
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from mixer.backend.django import mixer

from apps.schedule.models import Event
from common.utils.tests import APIClient


class TestUserEvents(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(email=mixer.faker.email())
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.event_today = mixer.blend(
            'schedule.Event',
            title='My Event Today',
            start_date_time=timezone.now(),
            end_date_time=timezone.now() + timedelta(hours=1),
            user=self.user,
        )
        self.event_last_year_month = mixer.blend(
            'schedule.Event',
            title='My Event Last Year, Last Month',
            start_date_time=timezone.now() - timedelta(days=396, hours=1),
            end_date_time=timezone.now() - timedelta(days=396),
            user=self.user,
        )
        self.url = reverse("api:user-events")
        self.detail_url = reverse("api:user-events-detail",
                                  kwargs={'event_id': self.event_today.id})

    def test_get_events(self):
        resp = self.client.get(self.url)
        data = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(2, data['count'])
        self.assertEqual(data['results'][0]['id'], str(self.event_today.id))

    def test_filter_events_by_date(self):
        resp_no_filter = self.client.get(self.url)
        data_no_filter = resp_no_filter.json()
        resp = self.client.get(
            f'{self.url}?date={date.today().strftime("%Y-%m-%d")}')
        data = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertNotEqual(data_no_filter['count'], data['count'])
        self.assertTrue(data['results'][0]['id'], str(self.event_today.id))

    def test_filter_events_by_month(self):
        resp_no_filter = self.client.get(self.url)
        data_no_filter = resp_no_filter.json()
        resp = self.client.get(f'{self.url}?month={date.today().month}')
        data = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertNotEqual(data_no_filter['count'], data['count'])
        self.assertEqual(data['results'][0]['id'], str(self.event_today.id))

    def test_filter_events_by_year(self):
        resp_no_filter = self.client.get(self.url)
        data_no_filter = resp_no_filter.json()
        resp = self.client.get(f'{self.url}?year={date.today().strftime("%Y")}')
        data = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertNotEqual(data_no_filter['count'], data['count'])
        self.assertEqual(data['results'][0]['id'], str(self.event_today.id))

    def test_add_event(self):
        input_data = {
            'title': 'New Event',
            'startDateTime': (timezone.now() + timedelta(days=1)).isoformat(),
            'endDateTime': (timezone.now() + timedelta(days=1, hours=1)).isoformat(),
        }
        resp = self.client.post(self.url, input_data, format='json')
        data = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['title'], input_data['title'])

    def test_update_event_date(self):
        add_one_day_start = (self.event_today.start_date_time + timedelta(days=1)
                             ).strftime('%Y-%m-%d')
        add_one_day_end = (self.event_today.end_date_time + timedelta(days=1)
                           ).strftime('%Y-%m-%d')
        input_data = {'startDateTime': add_one_day_start, 'endDateTime': add_one_day_end}
        resp = self.client.patch(self.detail_url, input_data, format='json')
        self.assertEqual(resp.status_code, 200)
        self.event_today.refresh_from_db()
        self.assertEqual(self.event_today.start_date_time.strftime('%Y-%m-%d'), add_one_day_start)
        self.assertEqual(self.event_today.end_date_time.strftime('%Y-%m-%d'), add_one_day_end)

    def test_delete_event(self):
        initial_event_count = Event.objects.count()
        resp = self.client.delete(self.detail_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(initial_event_count - 1, Event.objects.count())
