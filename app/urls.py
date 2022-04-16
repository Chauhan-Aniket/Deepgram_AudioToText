from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import HomePageView, audio_upload

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("form/", audio_upload, name="audio_upload"),
]
