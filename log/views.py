from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from core.mixins import HtmxTemplateResponseMixin
from .forms import CreateCollectionForm
from .models import Collection



class HtmxFormView(HtmxTemplateResponseMixin, FormView):
    """A view for displaying a form and rendering a htmx or regular template response."""

class CollectionsView(LoginRequiredMixin, HtmxFormView):
    form_class = CreateCollectionForm
    template_name = 'collections.html'
    htmx_template_name = template_name

    def get_initial(self):
        initial = super().get_initial()  
        initial['user'] = self.request.user
        return initial

    def get_success_url(self):
        # note that this may only be called when javascript is turned off
        return reverse_lazy('log_collections')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['collections'] = Collection.objects.filter(user=self.request.user, archived=False).order_by('name')
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class CollectionDetailView(LoginRequiredMixin, DetailView):
    model = Collection
    template_name = 'collection_detail.html'
