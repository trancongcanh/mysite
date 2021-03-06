from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
#Điều hướng tới các app con trong chương trình
urlpatterns = [
    url(r'^stocks/', include('stocks.urls')),
    url(r'^$', include('stocks.urls')),
    url(r'^admin/', admin.site.urls),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, 
    document_root=settings.MEDIA_ROOT)