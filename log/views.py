from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, UpdateView
from django.shortcuts import get_object_or_404, redirect
from core.mixins import HtmxTemplateResponseMixin
from .forms import CreateCollectionForm, UpdateCollectionForm, CreateItemForm, UpdateItemForm, CreateEventForm
from .models import Collection, Item, Event



class HtmxFormView(HtmxTemplateResponseMixin, FormView):
    '''A view for displaying a form and rendering a htmx or regular template response.'''

class HtmxUpdateView(HtmxTemplateResponseMixin, UpdateView):
    '''A view for displaying a form and rendering a htmx or regular template response to update models'''


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
        context['collections'] = Collection.objects.filter(user=self.request.user).order_by('name')
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class CollectionDetailView(LoginRequiredMixin, DetailView):
    model = Collection
    template_name = 'collection_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = self.object.item_set.all()
        context['events'] = Event.objects.filter(item__in=context['items']).order_by('-created')[:25] # 25 most recent
        return context
    

class CollectionUpdateView(LoginRequiredMixin, HtmxUpdateView):
    model = Collection
    form_class = UpdateCollectionForm
    template_name = 'collection_update.html'
    htmx_template_name = template_name
    
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.collection = get_object_or_404(Collection, pk=self.kwargs.get('pk'), user=self.request.user)

    def get_initial(self):
        initial = super().get_initial()  
        initial['user'] = self.request.user
        initial['collection'] = self.collection
        return initial

    def get_success_url(self):
        # note that this may only be called when javascript is turned off
        return reverse_lazy('log_collection_update', kwargs={'pk': self.collection.id, 'slug': self.collection.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['collection'] = self.collection
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class CollectionDeleteView(LoginRequiredMixin, View):
    '''
    Requires HTMX to function correctly.
    Means Javascript is required for deleting records.
    '''
    def delete_collection(self):
        collection = get_object_or_404(
            Collection,
            pk=self.kwargs.get('pk'),
            slug=self.kwargs.get('slug'),
            user=self.request.user
        )
        collection.delete()
        return True

    def delete(self, request, *args, **kwargs):
        self.delete_collection()
        # the HX-Redirect response header is used by htmx to fire a redirect to the value of the header
        return HttpResponse(headers={'HX-Redirect': reverse_lazy('log_collections')})


class ItemCreateView(LoginRequiredMixin, HtmxFormView):
    form_class = CreateItemForm
    template_name = 'item_create.html'
    htmx_template_name = template_name

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.collection = get_object_or_404(Collection, pk=self.kwargs.get('pk'), user=self.request.user)
        self.failure = False

    def get_initial(self):
        initial = super().get_initial()  
        initial['user'] = self.request.user
        initial['collection'] = self.collection
        return initial

    def get_success_url(self):
        # note that this may only be called when javascript is turned off
        return reverse_lazy('log_collection_item_create', kwargs={'pk': self.collection.id})
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['collection'] = self.collection
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        self.failure = True
        return super().form_invalid(form)

    def dispatch(self, *args, **kwargs):
        response = super(ItemCreateView, self).dispatch(*args, **kwargs)
        # this allows us to trigger an event on the client
        # to show a success message
        # honestly, using the django messages framework is a better solution
        if self.request.htmx and not self.failure:
            response['HX-Trigger-After-Swap'] = 'success'
        return response

class ItemUpdateView(LoginRequiredMixin, HtmxUpdateView):
    model = Item
    form_class = UpdateItemForm
    template_name = 'item_update.html'
    htmx_template_name = template_name
    
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.item = get_object_or_404(Item, pk=self.kwargs.get('pk'))
        self.collection = get_object_or_404(Collection, pk=self.item.collection.pk)


    def get_initial(self):
        initial = super().get_initial()  
        initial['user'] = self.request.user
        initial['collection'] = self.collection
        initial['item'] = self.item
        return initial

    def get_success_url(self):
        return self.collection.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ItemDeleteView(LoginRequiredMixin, View):
    '''
    Requires HTMX to function correctly.
    Means Javascript is required for deleting records.
    '''
    def delete_item(self):
        item = get_object_or_404(
            Item,
            pk=self.kwargs.get('pk'),
            collection__user=self.request.user
        )
        redirect_url = reverse_lazy(
            'log_collection_detail',
            kwargs={'pk': item.collection.id, 'slug': item.collection.slug})
        
        item.delete()
        return redirect_url

    def delete(self, request, *args, **kwargs):
        redirect_url = self.delete_item()
        # the HX-Redirect response header is used by htmx to fire a redirect to the value of the header
        return HttpResponse(headers={'HX-Redirect': redirect_url})


class EventCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        item = get_object_or_404(
            Item,
            pk=self.kwargs.get('pk'),
            collection__user=self.request.user
        )
        form = CreateEventForm(self.request.POST, initial={'item': item})
        if form.is_valid():
            form.save()
        # refreshing at this point
        # but might make more sense to simply just append the new event to the body
        return HttpResponse(headers={'HX-Refresh': 'true'})
    
