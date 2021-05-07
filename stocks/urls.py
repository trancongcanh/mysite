from django.conf.urls import url 
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views, search, upload, login, logout, signup, export, buy_stocks, sell_stocks, image_view, stock_information_owned
# Đặt app name
app_name = "stocks"
# Cấu hình các đường link trong app
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
    url(r'^image_upload/', image_view.image_view, name = 'image_upload'),
    url(r'^stock_information_owned/', stock_information_owned.stock_information_owned, name = 'stock_information_owned'),
]
# Thiết định cho chức năng upload avatar
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)