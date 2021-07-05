from core.mixins import HtmxTemplateResponseMixin
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, UpdateView


class HtmxTemplateView(HtmxTemplateResponseMixin, TemplateView):
    '''A view for rendering a htmx or regular template response'''


class HtmxFormView(HtmxTemplateResponseMixin, FormView):
    '''A view for displaying a form and rendering a htmx or regular template response.'''


class HtmxUpdateView(HtmxTemplateResponseMixin, UpdateView):
    '''A view for displaying a form and rendering a htmx or regular template response to update models'''
