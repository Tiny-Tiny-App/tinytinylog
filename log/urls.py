from django.urls import path
from .views import (
    CollectionsView,
    CollectionView,
    CollectionUpdateView,
    CollectionDeleteView,
    ItemCreateView,
    ItemUpdateView,
    ItemDeleteView,
    EventDeleteView,
    SearchEventsView,
)


urlpatterns = [
    path('search/', SearchEventsView.as_view(), name='log_search'),
    path('collections/item/event/<int:pk>/delete/', EventDeleteView.as_view(), name='log_collection_item_event_delete'),
    path('collections/<int:collection_pk>/item/<int:item_pk>/event/create/', CollectionView.as_view(), name='log_collection_item_event_create'),
    path('collections/item/delete/<int:pk>/', ItemDeleteView.as_view(), name='log_collection_item_delete'),
    path('collections/item/update/<int:pk>/', ItemUpdateView.as_view(), name='log_collection_item_update'),
    path('collections/item/create/<int:pk>/', ItemCreateView.as_view(), name='log_collection_item_create'),
    path('collections/update/<slug:slug>/<int:pk>/', CollectionUpdateView.as_view(), name='log_collection_update'),
    path('collections/delete/<slug:slug>/<int:pk>/', CollectionDeleteView.as_view(), name='log_collection_delete'),
    path('collections/<slug:slug>/<int:collection_pk>/', CollectionView.as_view(), name='log_collection_detail'),
    path('collections/', CollectionsView.as_view(), name='log_collections'),
]
