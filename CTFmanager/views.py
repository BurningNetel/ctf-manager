from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import EventForm, ChallengeForm, SolveForm
from .models import Event, Challenge


@login_required
def home_page(request):
    return render(request, 'home.html')


@login_required
def events_page(request):
    _events = Event.objects.filter(date__gt=timezone.now())
    archive = Event.objects.filter(date__lte=timezone.now())
    return render(request, 'event/events.html', {'events': _events,
                                                 'archive': archive})


@login_required
def new_event_page(request):
    form = EventForm(data=request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('events')
        else:
            return render(request, 'event/add_event.html', {'form': form})
    return render(request, 'event/add_event.html', {'form': EventForm()})


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
    _challenge = Challenge.objects.get(name=challenge_name)
    if not _challenge.get_pad_created:
        result, json = _challenge.create_pad()
        if result:
            _challenge.save()

    return render(request, 'event/challenge_pad.html', {'challenge': _challenge})


def challenge_solve(request, event_pk, challenge_pk):
    form = SolveForm(data=request.POST)
    if request.user.is_authenticated():
        if form.is_valid():
            chal = Challenge.objects.get(pk=challenge_pk)
            _flag = request.POST['flag']
            if chal.solve(request.user, flag=_flag):
                chal.save()
                return JsonResponse(data={'status_code': 200,
                                          'result': True,
                                          })
            else:
                return JsonResponse(data={'status_code': 304,
                                          'result': False,
                                          })
        else:
            return JsonResponse(data={'status_code': 304,
                                      'result': False,
                                      })
    return JsonResponse(data={'status_code': 401,
                              'result': False,
                              })


def event_join(request, event_name):
    if request.user.is_authenticated():
        event = Event.objects.get(pk=event_name)
        user = request.user
        if request.method == 'POST':
            members = event.join(user)
            if members > 0:
                return JsonResponse({
                    'status_code': 200,
                    'members': members,
                })
            else:
                return JsonResponse({
                    'status_code': 304,
                    'members': -1,
                })
        elif request.method == 'DELETE':
            members = event.leave(user)
            if members > -1:
                return JsonResponse({
                    'status_code': 200,
                    'members': members,
                })
            else:
                return JsonResponse({
                    'status_code': 304,
                    'members': -1,
                })
    else:
        r = JsonResponse({
            'status_code': 401,
            'members': -1,
        })
        return r
