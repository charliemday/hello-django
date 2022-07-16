from django.urls import path

from .views import SignupView, LoginView, UserDetailsView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("signup/", SignupView.as_view(), name="signup"),
    path('user/', UserDetailsView.as_view(), name='user-details'),
]