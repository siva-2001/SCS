from django.conf import settings
from authorizationApp.views import JudgeObtainAuthToken
from authorizationApp.urls import auth_urlpatterns
from translationApp.urls import translation_urlpatterns
from SCSapp.urls import scs_urlpatterns
from django.urls import include, path, re_path
from django.contrib import admin
from django.conf.urls.static import static


urlpatterns = [
    path('auth/', include(auth_urlpatterns)),
    path('liveStream/', include(translation_urlpatterns)),
    path('', include(scs_urlpatterns)),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)