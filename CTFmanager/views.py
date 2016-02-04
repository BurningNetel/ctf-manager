from braces.views import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import TemplateView, FormView

from .forms import EventForm, ChallengeForm, SolveForm
from .models import Event, Challenge


class HomePageView(LoginRequiredMixin, TemplateView):

    template_name = 'home.html'


class EventPageView(LoginRequiredMixin, TemplateView):

    template_name = 'event/events.html'

    def get_context_data(self, **kwargs):
        context = super(EventPageView, self).get_context_data(**kwargs)
        context['events'] = Event.objects.filter(date__gt=timezone.now())
        context['archive'] = Event.objects.filter(date__lte=timezone.now())
        return context


class EventFormView(LoginRequiredMixin, FormView):
    template_name = 'event/add_event.html'
    form_class = EventForm
    success_url = reverse_lazy('events')

    def form_valid(self, form):
        form.save()
        return super(EventFormView, self).form_valid(form)


@login_required
def view_event(request, event_id):
    _event = Event.objects.get(pk=event_id)
    solve_form = SolveForm()
    return render(request, 'event/event_detail.html', {'event': _event,
                                                       'solve_form': solve_form})


@login_required
def new_challenge(request, event_id):
    _event = Event.objects.get(pk=event_id)
    form = ChallengeForm(data=request.POST)
    if request.method == 'POST':
        form.set_event(_event)
        if form.is_valid():
            form.save()
            return redirect(_event.get_absolute_url())
        else:
            return render(request, 'event/add_challenge.html', {'form': form, 'event': _event})
    return render(request, 'event/add_challenge.html', {'form': ChallengeForm(), 'event': _event})


@login_required
def challenge_pad(request, event_id, challenge_name):
    _event = Event.objects.get(pk=event_id)
    _challenge = Challenge.objects.get(name__iexact=challenge_name,
                                       event=_event)
    if not _challenge.get_pad_created:
        result, json = _challenge.create_pad()
        if result:
            _challenge.save()

    solve_form = SolveForm()
    return render(request, 'event/challenge_pad.html', {'challenge': _challenge,
                                                        'solve_form': solve_form})
