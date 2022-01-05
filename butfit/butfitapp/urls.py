from django.urls import path

from .views      import SignupView, SigninView, ClassView

urlpatterns = [
    path('signup', SignupView.as_view()),
    path('signin', SigninView.as_view()),
    path('class', ClassView.as_view()),
]