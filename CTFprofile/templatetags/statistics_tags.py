from django import template

register = template.Library()


@register.filter
def can_show_graph(user):
    for solve in user.solver_set.all():
        if solve.solve_time:
            return True

    return False
