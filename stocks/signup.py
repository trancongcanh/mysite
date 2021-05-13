from django.shortcuts import render
from .models import User

# Xử lí sign up
def signup(request):
    # Thực hiện xóa các điều kiện tìm kiếm (nếu có) ở MH danh sách hiện tại trên session
    if request.session.get('company_value','') != "":
        del request.session['company_value'] 
    if request.session.get('count_company','') != "":
        del request.session['count_company'] 
    if request.session.get('date_update','') != "":        
        del request.session['date_update'] 
    # Lấy dữ liệu từ request và thực hiện sign up 
    if request.method == 'POST':
        # Get dữ liệu từ request để thực hiện sign up
        user_name_views = request.POST.get('user_name', "")
        password_views = request.POST.get('password', "")
        email_view = request.POST.get('email', "")
        phone_view = request.POST.get('phone', "")
        capital_view = request.POST.get('capital', "")
        message = ""
        # Thực hiện sign up thông tin user và CSDL, kiểm tra có sign up thành công hay không và gửi câu thông báo tương ứng
        if (user_name_views != "" and password_views != "" and capital_view != ""):
            user = User.objects.update_or_create(user_name=user_name_views, password=password_views, capital=capital_view, email=email_view, phone=password_views)
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