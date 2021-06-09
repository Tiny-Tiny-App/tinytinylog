from django.urls import path, include
from .views import CollectionsView, CollectionDetailView


urlpatterns = [
    path('', CollectionsView.as_view(), name='log_collections'),
    path('collection/<slug:slug>/<int:pk>/', CollectionDetailView.as_view(), name='log_collection_detail'),
]