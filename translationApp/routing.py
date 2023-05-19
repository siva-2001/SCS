from django.urls import re_path

from translationApp import consumers

websocket_urlpatterns = [
    re_path(r"ws/volleyballTranslation/(?P<match_id>\w+)/$", consumers.VolleyballConsumer.as_asgi()),
]