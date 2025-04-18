from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.views import *

from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('articles/<slug:slug>/', DetailPageView.as_view(), name='detail-page'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
