from django.urls import path
from .views import CheckIngredientsView, UserRegistrationView, UserLoginView

urlpatterns = [
    path('check-ingredients/', CheckIngredientsView.as_view(), name='check-ingredients'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
]
