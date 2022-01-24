from django.test import TestCase
from datetime import datetime, timedelta
from .models import Event

class EventsTest(TestCase):

    def test_str_rep(self):
        event = Event(name="Test Event", event_date=datetime.now())
        self.assertEqual(str(event), event.name)

    def test_event_timing(self):
        now = datetime.now()
        past = now - timedelta(days=2)
        future = now + timedelta(days=2)
        event = Event(name="Test Event", event_date=now)
        self.assertEqual(event.event_timing(now), "Event is on the same day")
        self.assertEqual(event.event_timing(past), "Event is after this date")
        self.assertEqual(event.event_timing(future), "Event is before this date")


class EventViewTests(TestCase):

    def test_all_events(self):
        response = self.client.get('/allevents/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('formset', response.context)


# class BandTest(TestCase):

#     def test_not_even_close(self):
#         self.assertEqual('Nickelback', 'Metallica')
