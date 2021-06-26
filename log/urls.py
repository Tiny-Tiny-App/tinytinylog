from django.urls import path, include
from .views import (
    CollectionsView,
    CollectionDetailView,
    CollectionUpdateView,
    CollectionDeleteView,
    ItemCreateView,
    ItemUpdateView,
    ItemDeleteView,
    EventCreateView,
)


urlpatterns = [
    path('collections/item/<int:pk>/event/create/', EventCreateView.as_view(), name='log_collection_item_event_create'),
    path('collections/item/delete/<int:pk>/', ItemDeleteView.as_view(), name='log_collection_item_delete'),
    path('collections/item/update/<int:pk>/', ItemUpdateView.as_view(), name='log_collection_item_update'),
    path('collections/item/create/<int:pk>/', ItemCreateView.as_view(), name='log_collection_item_create'),
    path('collections/update/<slug:slug>/<int:pk>/', CollectionUpdateView.as_view(), name='log_collection_update'),
    path('collections/delete/<slug:slug>/<int:pk>/', CollectionDeleteView.as_view(), name='log_collection_delete'),
    path('collections/<slug:slug>/<int:pk>/', CollectionDetailView.as_view(), name='log_collection_detail'),
    path('collections/', CollectionsView.as_view(), name='log_collections'),
]