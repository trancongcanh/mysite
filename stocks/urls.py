from django.conf.urls import url 
from django.contrib.auth import views as auth_views

from . import views 

app_name = "stocks"
urlpatterns = [ 
    url(r'^$', views.index, name='index'),
    url(r'^search/', views.search, name='search'),
    url(r'^upload-csv/', views.profile_upload, name="profile_upload"),
    url(r'^login/', views.login, name="login"),
    url(r'^logout/',auth_views.LogoutView.as_view(next_page='/admin/logout'),name='logout'),
    url(r'^signup/',views.signup, name="signup"),
    url(r'^export_csv/',views.export_csv, name="export_csv"),    
]