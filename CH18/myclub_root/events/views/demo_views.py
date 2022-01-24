from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import FileResponse
from django.core import serializers
from django.template import RequestContext, Template
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.dates import ArchiveIndexView, MonthArchiveView
from django.contrib.auth.mixins import LoginRequiredMixin
from formtools.wizard.views import SessionWizardView
from django.core.mail import send_mail, get_connection
from django.contrib import messages
from django.urls import reverse_lazy
# from django.template.response import TemplateResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from datetime import date
# import calendar
from datetime import datetime
import csv
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
# from calendar import HTMLCalendar
from events.models import Venue, MyClubUser, Event
# from .forms import VenueForm
from events.forms import EventForm, CommitteeForm
from django.forms import formset_factory, modelformset_factory


def gen_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="bart.txt"'
    lines = [
        "I will not expose the ignorance of the faculty.\n",
        "I will not conduct my own fire drills.\n",
        "I will not prescribe medication.\n",
    ]
    response.writelines(lines)
    return response


def gen_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="venues.csv"'
    writer = csv.writer(response)
    venues = Venue.venues.all()
    writer.writerow(['Venue Name', 'Address', 'Phone', 'Email'])
    for venue in venues:
        writer.writerow([venue.name, venue.address, venue.phone, venue.email_address])    
    return response


def gen_pdf(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica-Oblique", 14)
    lines = [
        "I will not expose the ignorance of the faculty.",
        "I will not conduct my own fire drills.",
        "I will not prescribe medication.",
    ]
    for line in lines:
        textob.textLine(line)
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='bart.pdf')


def template_demo(request):
    empty_list = []
    color_list = ['red', 'green', 'blue', 'yellow']
    somevar = 5
    anothervar = 21
    today = datetime.now()
    past = datetime(1985, 11, 5)
    future = datetime(2035, 11, 5)
    best_bands = [
        {'name': 'The Angels', 'country': 'Australia'},
        {'name': 'AC/DC', 'country': 'Australia'},
        {'name': 'Nirvana', 'country': 'USA'},
        {'name': 'The Offspring', 'country': 'USA'},
        {'name': 'Iron Maiden', 'country': 'UK'},
        {'name': 'Rammstein', 'country': 'Germany'},
    ]
    aussie_bands = ['Australia', ['The Angels', 'AC/DC', 'The Living End']]
    venues_js = serializers.serialize('json', Venue.venues.all())
    return render(request,
        'events/template_demo.html',
        {
            'somevar': somevar,
            'anothervar': anothervar,
            'empty_list': empty_list,
            'color_list': color_list,
            'best_bands': best_bands,
            'today': today,
            'past': past,
            'future': future,
            'aussie_bands': aussie_bands,
            'venues': venues_js,
        }
    )


def my_processor(request):
    return {
        'foo': 'foo',
        'bar': 'bar',
        'baz': 'baz',
    }


def context_demo(request):
    # template = Template('{{ user }}<br>{{ perms }}<br>{{ request }}<br>{{ messages }}')
    # template = Template('{{ LANGUAGE_CODE }}<br>{{ LANGUAGE_BIDI }}')
    template = Template('{{ foo }}<br>{{ bar }}<br>{{ baz }}')
    con = RequestContext(request, processors=[my_processor])
    return HttpResponse(template.render(con))


class TemplateViewDemo(TemplateView):

    template_name = "events/cbv_demo.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Testing The TemplateView CBV"
        return context


class ListViewDemo(ListView):
    model = Event
    context_object_name = 'all_events'


class DetailViewDemo(DetailView):
    model = Event
    context_object_name = 'event'


class CreateViewDemo(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Event
    # fields = ['name', 'event_date', 'description']
    success_url = reverse_lazy('show-events')
    form_class = EventForm


class UpdateViewDemo(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Event
    # fields = ['name', 'event_date', 'description']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('show-events')
    form_class = EventForm


class DeleteViewDemo(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Event
    context_object_name = 'event'
    success_url = reverse_lazy('show-events')


class ArchiveIndexViewDemo(ArchiveIndexView):
    model=Event 
    date_field="event_date"
    allow_future = True


class MonthArchiveViewDemo(MonthArchiveView):
    queryset = Event.events.all()
    date_field="event_date"
    context_object_name = 'event_list'
    allow_future = True
    month_format = '%m'


def committee_formset(request):
    committee_formset = formset_factory(CommitteeForm, extra=3)
    if request.method == 'POST':
        formset = committee_formset(request.POST)
        if formset.is_valid():
            # process the form
            pass
    else:
        formset = committee_formset()
        return render(request, 'events/committee.html', {'formset': formset})


def all_events(request):
    EventsFormSet = modelformset_factory(
        Event, 
        fields=('name', 'event_date'),
        extra=0
    )
    qry = Event.events.all().order_by('event_date')
    pg = Paginator(qry, 4)
    page = request.GET.get('page')
    try:
        event_records = pg.page(page)
    except PageNotAnInteger:
        event_records = pg.page(1)
    except EmptyPage:
        event_records = pg.page(pg.num_pages)
    if request.method == 'POST':
        formset = EventsFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return_url = '/allevents/'
            if 'page' in request.GET:
                return_url += '?page=' + request.GET['page']
            return HttpResponseRedirect(return_url)
    else:
        page_qry = qry.filter(id__in=[event.id for event in event_records])
        formset = EventsFormSet(queryset=page_qry)

    context = {'event_records': event_records, 'formset': formset}
    messages.debug(request, qry)
    return render(request, 'events/all_events.html', context)


class SurveyWizard(SessionWizardView):
    template_name = 'events/survey.html'
    def done(self, form_list, **kwargs):
        responses = [form.cleaned_data for form in form_list]
        mail_body = ''
        for response in responses:
            for k,v in response.items():
                mail_body += "%s: %s\n" % (k, v)
        con = get_connection('django.core.mail.backends.console.EmailBackend')
        send_mail(
            'Survey Submission',
            mail_body,
            'noreply@example.com',
            ['siteowner@example.com'],
            connection=con
        )
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Your survey was submitted successfully. Thank you for your feedback'
        )
        return HttpResponseRedirect('/survey')


class ModelFormWizard(SessionWizardView):
    template_name = 'events/modelwiz_demo.html'
    def done(self, form_list, **kwargs):
        for form in form_list:
            form.save()
        return HttpResponseRedirect('/')