from django.db import models
from django.contrib.auth.models import User


class VenueManager(models.Manager):
    def get_queryset(self):
        return super(VenueManager, self).get_queryset().filter(zip_code='00000')


class Venue(models.Model):
    name = models.CharField('Venue Name', max_length=120)
    address = models.CharField(max_length=300)
    zip_code = models.CharField('Zip/Post Code', max_length=12)
    phone = models.CharField('Contact Phone', max_length=20, blank=True)
    web = models.URLField('Web Address', blank=True)
    email_address = models.EmailField('Email Address', blank=True)

    venues = models.Manager()
    local_venues = VenueManager()

    def __str__(self):
       return self.name


class MyClubUser(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField('User Email')

    def __str__(self):
        return self.first_name + " " + self.last_name


# Illustrative examples for multi-table inheritance
# and Abstract base classes.
# You're fine to try this in your code, 
# but you might get some errors later in the book.
# This is easy fixed by resetting your database,
# which I show you how to do in Chapter 16

# class UserBase(models.Model):
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     email = models.EmailField('User Email')
    
#     class Meta:
#         abstract = True
#         ordering = ['last_name']
    
    
# class MyclubUser(UserBase):
#     def __str__(self):
#         return self.first_name + " " + self.last_name
    
    
# class Subscriber(UserBase):
#     date_joined = models.DateTimeField()


class EventManager(models.Manager):
    def event_type_count(self, event_type):
        return self.filter(name__icontains=event_type).count()


class Event(models.Model):
    name = models.CharField('Event Name', max_length=120)
    event_date = models.DateTimeField('Event Date')
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    attendees = models.ManyToManyField(MyClubUser, blank=True)
    description = models.TextField(blank=True)
    events = EventManager()

    def save(self, *args, **kwargs):
        self.manager = User.objects.get(username='admin')
        super(Event, self).save(*args, **kwargs)

    def event_timing(self, date):
        if self.event_date > date:
            return "Event is after this date"
        elif self.event_date == date:
            return "Event is on the same day"
        else:
            return "Event is before this date"

    @property
    def name_slug(self):
        return self.name.lower().replace(' ','-')

    def __str__(self):
        return self.name