from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.urls import reverse
from datetime import datetime
from .models import Company, User
import io,csv
from django.shortcuts import redirect

# Xử lí sign up
def signup(request):
    # Thực hiện xóa các điều kiện tìm kiếm (nếu có) ở MH danh sách hiện tại trên session
    if request.session.get('company_cap','') != "":
        del request.session['company_cap'] 
    if request.session.get('count_company','') != "":
        del request.session['count_company'] 
    if request.session.get('date_update','') != "":        
        del request.session['date_update'] 
    # Lấy dữ liệu từ request và thực hiện sign up 
    if request.method == 'POST':
        # Get dữ liệu từ request để thực hiện sign up
        user_name_views = request.POST.get('user_name', "")
        password_views = request.POST.get('password', "")
        message = ""
        # Thực hiện sign up thông tin user và CSDL, kiểm tra có sign up thành công hay không và gửi câu thông báo tương ứng
        if (user_name_views != "" and password_views != ""):
            user = User.objects.update_or_create(user_name=user_name_views, password=password_views)
            message = "Đăng kí thành công, vui lòng quay về trang chủ để login"
        else:
            message = "Đăng kí không thành công, vui lòng nhập đầy đủ username và password"
        context = {
            'message': message
        }
    # Xử lí hiển thị ban đầu MH sign up 
    else:
        context = {}
    return render(request, 'stocks/signup_user.html', context)   