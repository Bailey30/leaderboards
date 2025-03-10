from django.urls import path

from . import views

app_name = "boards"  # Namespace of the app
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:board_id>/", views.BoardDetailView.as_view(), name="board_detail"),
    path("register", views.RegistrationView.as_view(), name="register"),
    path("login", views.Login.as_view(), name="login"),
    path("logout", views.Logout.as_view(), name="logout"),
]
