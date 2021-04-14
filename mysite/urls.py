from django.conf.urls import include, url
from django.contrib import admin
#Điều hướng tới các app con trong chương trình
urlpatterns = [
    url(r'^stocks/', include('stocks.urls')),
    url(r'^$', include('stocks.urls')),
    url(r'^admin/', admin.site.urls),
]