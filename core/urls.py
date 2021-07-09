from django.urls import path
from .views import IndexView, UserProfileView, UserDeleteView, UserAccountDeletedView


urlpatterns = [
    path('accounts/user/profile/', UserProfileView.as_view(), name='user_profile'),
    path('accounts/user/d/', UserDeleteView.as_view(), name='user_delete'),
    path('goodbye/', UserAccountDeletedView.as_view(), name='goodbye'),
    path('', IndexView.as_view(), name='index'),
]
