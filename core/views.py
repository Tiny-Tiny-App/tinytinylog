import logging
from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy


logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = 'index.html'


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'user/profile.html'


class UserDeleteView(LoginRequiredMixin, View):
    def delete_user(self):
        self.request.user.delete()

    def post(self, *args, **kwargs):
        self.delete_user()
        return redirect(reverse_lazy('goodbye'))


class UserAccountDeletedView(TemplateView):
    template_name = 'user/deleted.html'
