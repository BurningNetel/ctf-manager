from braces.views import LoginRequiredMixin
from django.views.generic import TemplateView

from accounts.models import CTFUser


class ProfileView(LoginRequiredMixin, TemplateView):

    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['p_user'] = user = CTFUser.objects.get(pk=self.args[0])
        context['events'] = user.event_set.all()
        return context
