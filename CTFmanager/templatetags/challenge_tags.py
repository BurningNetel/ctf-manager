from django import template
from django.utils.formats import date_format

from CTFmanager.models import Solver

register = template.Library()


@register.simple_tag
def solve_time(user, challenge):
    try:
        solve_dt = challenge.get_solve_time(user)
        if solve_dt:
            return "You solved this challenge at %s" % date_format(solve_dt, 'SHORT_DATETIME_FORMAT', True)
        return ''
    except Solver.DoesNotExist:
        return ''


@register.simple_tag
def join_time(user, challenge):
    try:
        join_dt = challenge.get_join_time(user)
        if join_dt:
            return "You started solving this challenge on %s." % date_format(join_dt, 'SHORT_DATETIME_FORMAT', True)
        return ''
    except Solver.DoesNotExist:
        return ''

@register.filter
def solved(user, challenge):
    if challenge.get_solve_time(user):
        return True
    return False

@register.filter
def is_solving(user, challenge):
    if challenge.get_join_time(user):
        return True
    return False

@register.filter
def is_solved(challenge):
    return challenge.is_solved()
