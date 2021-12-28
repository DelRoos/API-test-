from django.urls import path
from . import views

urlpatterns = [
    # path("", views.HelloAuthView.as_view(), name='hello_auth'),
    path("", views.UserCreatedView.as_view(), name="sign_up"),
    path("current_user/", views.CurrentUserView.as_view(), name="current_user")
]