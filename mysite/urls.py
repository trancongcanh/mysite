from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^stocks/', include('stocks.urls')),
    url(r'^admin/', admin.site.urls),
]