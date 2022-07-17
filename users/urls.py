from django.urls import path

from .views import SignupView, LoginView, UserDetailsView, UserFeedbackView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("signup/", SignupView.as_view(), name="signup"),
    path('user/', UserDetailsView.as_view(), name='user-details'),
    path('feedback/', UserFeedbackView.as_view(), name='user-feedback'),
]