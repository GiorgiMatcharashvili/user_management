from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('login/', UserAuthenticationAPIView.as_view(), name='user-authentication'),
    path('user/<int:pk>/', UserDetailsAPIView.as_view(), name='user-details'),
    path('user/<int:pk>/permissions/', UserPermissionsAPIView.as_view(), name='user-permissions'),
]