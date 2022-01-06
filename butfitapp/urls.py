from django.urls import path

from .views      import SignupView, SigninView, CreateClassView, BuyCreditView, BookView, BookListView

urlpatterns = [
    path('signup', SignupView.as_view()),
    path('signin', SigninView.as_view()),
    path('class', CreateClassView.as_view()),
    path('credit', BuyCreditView.as_view()),
    path('book', BookListView.as_view()),
    path('book/<int:class_id>', BookView.as_view()),
]