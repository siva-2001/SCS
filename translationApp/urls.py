from django.urls import include, path, re_path
from translationApp.views import translationView, roomView

translation_urlpatterns = [
    path('<str:match_id>/', translationView, name="liveStream"),
    path('test/<str:match_id>/', roomView, name="match"),
]