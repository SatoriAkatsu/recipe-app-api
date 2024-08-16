"""
URL mappings for the user API.
"""

from django.urls import path

from user import views


app_name = 'user'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('api-token-auth/', views.AuthToken.as_view(), name='api_token_auth'),
    path('me/', views.RetrieveUpdateView.as_view(
        http_method_names=['get', 'patch']), name='me'),
]
