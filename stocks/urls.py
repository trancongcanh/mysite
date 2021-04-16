from django.conf.urls import url 
from django.contrib.auth import views as auth_views

from . import views 

app_name = "stocks"
urlpatterns = [ 
    url(r'^$', views.index, name='index'),
    url(r'^search/', views.search, name='search'),
    url(r'^upload-csv/', views.profile_upload, name="profile_upload"),
    url(r'^login/',auth_views.LoginView.as_view(template_name="stocks/login.html"), name="login"),
    url(r'^logout/',auth_views.LogoutView.as_view(next_page='/stocks/'),name='logout'),
]