import logging
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import View
from django.shortcuts import get_object_or_404, redirect
from django.core.paginator import Paginator
from core.htmx_views import HtmxTemplateView, HtmxFormView, HtmxUpdateView
from .forms import CreateCollectionForm, UpdateCollectionForm, CreateItemForm, UpdateItemForm
from .models import Collection, Item, Event

logger = logging.getLogger(__name__)


class CollectionsView(LoginRequiredMixin, HtmxFormView):
    form_class = CreateCollectionForm
    template_name = 'collections.html'
    htmx_template_name = 'partials/collections/collection_results.html'
    success_url = reverse_lazy('log_collections')

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['collections'] = Collection.objects.filter(user=self.request.user).order_by('name')
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class CollectionView(LoginRequiredMixin, HtmxTemplateView):
    template_name = 'collection_detail.html'
    htmx_template_name = 'partials/collections/collection_items_events.html'

    def get_collection(self):
        return get_object_or_404(Collection, pk=self.kwargs.get('collection_pk'), user=self.request.user)

    def paginator(self):
        self.items = self.get_collection().item_set.all()
        events = Event.objects.filter(item__in=self.items).order_by('-created')
        paginator = Paginator(events, 25)
        page_number = self.request.GET.get('page', 1)
        return paginator.get_page(page_number)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['collection'] = self.get_collection()
        context['page'] = self.paginator()
        context['items'] = self.items
        return context

    def post(self, request, *args, **kwargs):
        '''Used for htmx requests only '''
        item = get_object_or_404(
            Item,
            pk=self.kwargs.get('item_pk'),
            collection__user=self.request.user
        )
        Event.objects.create(
            item=item,
            comment=self.request.POST.get('comment'),
        )
        return self.render_to_response(self.get_context_data())


class CollectionUpdateView(LoginRequiredMixin, HtmxUpdateView):
    model = Collection
    form_class = UpdateCollectionForm
    template_name = 'collection_update.html'
    htmx_template_name = 'partials/collections/update_collection.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.collection = get_object_or_404(Collection, pk=self.kwargs.get('pk'), user=self.request.user)

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user
        initial['collection'] = self.collection
        return initial

    def get_success_url(self):
        return reverse_lazy(
            'log_collection_update',
            kwargs={
                'pk': self.collection.id,
                'slug': self.collection.slug
            }
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['collection'] = self.collection
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class CollectionDeleteView(LoginRequiredMixin, View):
    def delete_collection(self):
        collection = get_object_or_404(
            Collection,
            pk=self.kwargs.get('pk'),
            slug=self.kwargs.get('slug'),
            user=self.request.user
        )
        collection.delete()
        return True

    def get(self, request, *args, **kwargs):
        self.delete_collection()
        return redirect(reverse_lazy('log_collections'))


class ItemCreateView(LoginRequiredMixin, HtmxFormView):
    form_class = CreateItemForm
    template_name = 'item_create.html'
    htmx_template_name = 'partials/items/item_form.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.collection = get_object_or_404(
            Collection,
            pk=self.kwargs.get('pk'),
            user=self.request.user
        )

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user
        initial['collection'] = self.collection
        return initial

    def get_success_url(self):
        return reverse_lazy('log_collection_item_create', kwargs={'pk': self.collection.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['collection'] = self.collection
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Item created!')
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class ItemUpdateView(LoginRequiredMixin, HtmxUpdateView):
    model = Item
    form_class = UpdateItemForm
    template_name = 'item_update.html'
    htmx_template_name = 'partials/items/item_update_form.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.item = get_object_or_404(Item, pk=self.kwargs.get('pk'))

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user
        initial['item'] = self.item
        return initial

    def get_success_url(self):
        return reverse_lazy('log_collection_item_update', kwargs={'pk': self.item.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # added to pass context to navigation partials
        context['collection'] = self.item.collection
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Item updated!')
        return super().form_valid(form)


class ItemDeleteView(LoginRequiredMixin, View):
    def delete_item(self):
        item = get_object_or_404(
            Item,
            pk=self.kwargs.get('pk'),
            collection__user=self.request.user
        )
        collection = item.collection
        item.delete()
        return collection

    def get(self, request, *args, **kwargs):
        collection = self.delete_item()
        return redirect(collection.get_absolute_url())


class EventDeleteView(LoginRequiredMixin, View):
    def delete_event(self):
        event = get_object_or_404(
            Event,
            pk=self.kwargs.get('pk'),
            item__collection__user=self.request.user
        )
        collection = event.item.collection
        event.delete()
        return collection

    def get(self, request, *args, **kwargs):
        collection = self.delete_event()
        return redirect(collection.get_absolute_url())


class SearchEventsView(LoginRequiredMixin, HtmxTemplateView):
    template_name = 'search.html'
    htmx_template_name = 'search_results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('search')
        if search:
            context['events'] = Event.objects.filter(
                item__name__icontains=search,
                item__collection__user=self.request.user
            ).order_by('-created')
        return context
