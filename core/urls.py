from django.urls import path
from .views import IndexView, UserProfileView


urlpatterns = [
    path('accounts/user/profile/', UserProfileView.as_view(), name='user_profile'),
    path('', IndexView.as_view(), name='index'),
]
