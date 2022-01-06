from django.urls import path

from .views      import SignupView, SigninView, CreateClassView, BuyCreditView, BookView, LogView, BookListAdminView

urlpatterns = [
    path('signup', SignupView.as_view()),
    path('signin', SigninView.as_view()),
    path('class', CreateClassView.as_view()),
    path('credit', BuyCreditView.as_view()),
    path('log', LogView.as_view()),
    path('book/<int:class_id>', BookView.as_view()),
    path('bookings', BookListAdminView.as_view())
]