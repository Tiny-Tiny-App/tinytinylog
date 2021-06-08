from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import BaseFormView
from .forms import CreateCollectionForm
from core.mixins import HtmxTemplateResponseMixin


class HtmxFormView(HtmxTemplateResponseMixin, BaseFormView):
    """A view for displaying a form and rendering a htmx or regular template response."""


class CollectionsView(HtmxFormView):
    form_class = CreateCollectionForm
    template_name = 'collections.html'
    htmx_template_name = template_name

    def get_initial(self):
        initial = super().get_initial()  
        initial['user'] = self.request.user
        return initial

    def get_success_url(self):
        return reverse_lazy('log_collections')