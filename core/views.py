import logging
from django.views.generic import View, TemplateView

logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = 'index.html'


class UserProfileView(TemplateView):
    template_name = 'user/profile.html'


class UserDeleteView(View):
    pass