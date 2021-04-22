from django.conf.urls import url 
from django.contrib.auth import views as auth_views

from . import views, search, upload, login, logout, signup, export, buy_stocks, sell_stocks

app_name = "stocks"
urlpatterns = [ 
    url(r'^$', views.index, name='index'),
    url(r'^search/', search.search, name='search'),
    url(r'^upload-csv/', upload.profile_upload, name="profile_upload"),
    url(r'^login/', login.login, name="login"),
    url(r'^logout/',logout.logout,name='logout'),
    url(r'^signup/',signup.signup, name="signup"),
    url(r'^export_csv/',export.export_csv, name="export_csv"),    
    url(r'^buy_stocks/',buy_stocks.buy_stocks, name="buy_stocks"),
    url(r'^sell_stocks/',sell_stocks.sell_stocks, name="sell_stocks"),    
]