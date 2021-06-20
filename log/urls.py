from django.urls import path, include
from .views import (
    CollectionsView,
    CollectionDetailView,
    CollectionUpdateView,
    CollectionDeleteView,
    ItemCreateView,
)


urlpatterns = [
    path('collections/item/create/<int:pk>/', ItemCreateView.as_view(), name='log_collection_item_create'),
    path('collections/update/<slug:slug>/<int:pk>/', CollectionUpdateView.as_view(), name='log_collection_update'),
    path('collections/delete/<slug:slug>/<int:pk>/', CollectionDeleteView.as_view(), name='log_collection_delete'),
    path('collections/<slug:slug>/<int:pk>/', CollectionDetailView.as_view(), name='log_collection_detail'),
    path('collections/', CollectionsView.as_view(), name='log_collections'),
]