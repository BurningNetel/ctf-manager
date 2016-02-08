from django.http import JsonResponse
from django.views.generic import FormView

from CTFmanager.forms import SolveForm
from CTFmanager.models import Challenge, Event


class AjaxTemplateMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self, 'ajax_template_name'):
            split = self.template_name.split('.html')
            split[-1] = '_inner'
            split.append('.html')
            self.ajax_template_name = ''.join(split)
        if request.is_ajax():
            self.template_name = self.ajax_template_name
        return super(AjaxTemplateMixin, self).dispatch(request, *args, **kwargs)


class SolveFormView(AjaxTemplateMixin, FormView):
    template_name = 'event/solve_form.html'
    form_class = SolveForm

    def get_context_data(self, **kwargs):
        context = super(SolveFormView, self).get_context_data(**kwargs)
        context['pk'] = self.args[0]
        return context

    def get_form(self, form_class=SolveForm):
        challenge = Challenge.objects.get(pk=self.args[0])
        return form_class(instance=challenge, **self.get_form_kwargs())

    def form_valid(self, form):
        challenge = form.save(commit=False)
        user = self.request.user
        result = challenge.solve(user)
        challenge.save()
        if result:
            return JsonResponse(data={'success': True})
        return JsonResponse(data={'success': False})


def join_challenge(request, challenge_pk):
    if request.method == 'POST':
        if request.user.is_authenticated():
            chal = Challenge.objects.get(pk=challenge_pk)
            chal.join(request.user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})

    if request.method == 'DELETE':
        if request.user.is_authenticated():
            chal = Challenge.objects.get(pk=challenge_pk)
            success = chal.leave(request.user)
            chal.save()
            return JsonResponse({'success': success})
        else:
            return JsonResponse({'success': False})


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
