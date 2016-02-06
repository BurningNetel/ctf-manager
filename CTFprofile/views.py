from braces.views import LoginRequiredMixin
from django.contrib.auth.models import User

from django.views.generic import TemplateView


class ProfileView(LoginRequiredMixin, TemplateView):

    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        print("My pk is: %s"  % self.args[0])
        context['p_user'] = User.objects.get(pk=self.args[0])
        return context