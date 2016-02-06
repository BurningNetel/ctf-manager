from braces.views import LoginRequiredMixin

from django.views.generic import TemplateView


class ProfileView(LoginRequiredMixin, TemplateView):

    template_name = 'profile.html'