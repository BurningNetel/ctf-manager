from django import template
from django.utils.formats import date_format

from CTFmanager.models import Solver

register = template.Library()


@register.simple_tag
def solve_time(user, challenge):
    try:
        solve_dt = Solver.objects.get(user=user, challenge=challenge).solve_time
        return "You solved this challenge at %s" % date_format(solve_dt, 'SHORT_DATETIME_FORMAT', True)
    except Solver.DoesNotExist:
        return ''
