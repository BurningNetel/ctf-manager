from django.http import JsonResponse

from CTFmanager.forms import SolveForm
from CTFmanager.models import Challenge, Event


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