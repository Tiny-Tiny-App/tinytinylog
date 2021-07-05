import logging
from django.views.generic import TemplateView

logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = 'index.html'
