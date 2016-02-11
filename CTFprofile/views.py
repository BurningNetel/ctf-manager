from braces.views import LoginRequiredMixin
from chartjs.views.lines import BaseLineChartView
from django.views.generic import TemplateView

from accounts.models import CTFUser


class ProfileView(LoginRequiredMixin, TemplateView):

    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['p_user'] = user = CTFUser.objects.get(pk=self.args[0])
        context['events'] = user.event_set.all()
        return context


class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels."""
        return ["January", "February", "March", "April", "May", "June", "July"]

    def get_data(self):
        """Return 1 dataset to plot."""
        return [[75, 44, 92, 11, 44, 95, 35, 12, 1, 20, 40, 60]]

