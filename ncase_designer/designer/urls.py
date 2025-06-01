from django.urls import path
from . import views

urlpatterns = [
    path("auth-test/", views.test_adobe_auth),
]
