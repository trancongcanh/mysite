from django.conf.urls import url 
from django.contrib.auth import views as auth_views

from . import views, search, upload, login, logout, signup, export

app_name = "stocks"
urlpatterns = [ 
    url(r'^$', views.index, name='index'),
    url(r'^search/', search.search, name='search'),
    url(r'^upload-csv/', upload.profile_upload, name="profile_upload"),
    url(r'^login/', login.login, name="login"),
    url(r'^logout/',logout.logout,name='logout'),
    url(r'^signup/',signup.signup, name="signup"),
    url(r'^export_csv/',export.export_csv, name="export_csv"),    
]