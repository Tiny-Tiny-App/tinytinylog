from django.urls import path, include
from .views import CollectionsView


urlpatterns = [
    path('', CollectionsView.as_view(), name='log_collections'),
]