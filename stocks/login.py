from django.http import HttpResponse, Http404
from django.template import loader
from .models import Company, User
from datetime import datetime
from django.shortcuts import redirect

from .company_view import CompanyView

# Xử lí login
def login(request):
    # Thực hiện xóa các điều kiện tìm kiếm (nếu có) ở MH danh sách hiện tại trên session
    if request.session.get('company_cap','') != "":
        del request.session['company_cap'] 
    if request.session.get('count_company','') != "":
        del request.session['count_company'] 
    if request.session.get('date_update','') != "":        
        del request.session['date_update']     
    if request.method == 'POST':
        # Get dữ liệu từ request
        user_name_views = request.POST.get('user_name', "")
        password_views = request.POST.get('password', "")
        user = User.objects.filter(user_name=user_name_views, password=password_views)
        # Get ra template theo đường dẫn tương ứng để set hiển thị
        template = loader.get_template('stocks/login_user.html')
        # Kiểm tra tồn tại của user login
        # Nếu user không tồn tại trong CSDL thì gửi thông báo lỗi và yêu cầu login lại
        if len(user) == 0:
            message = "Login không thành công, vui lòng thử lại"
            context = {
                'message': message
            }
            return HttpResponse(template.render(context, request))
        # Nếu user có tồn tại trong CSDL thì quay trở về MH danh sách lưu trạng thái đã đăng nhập lên session
        else:
            request.session['last_touch'] = datetime.now()
            for user in user:
                request.session['member_id'] = user.user_name
            return redirect("stocks:index")     
    else:
        # Get dữ liệu từ request
        user_name_views = request.POST.get('user_name', "")
        password_views = request.POST.get('password', "")
        user = User.objects.filter(user_name=user_name_views, password=password_views)
        # Get ra template theo đường dẫn tương ứng để set hiển thị
        template = loader.get_template('stocks/login_user.html')
        if len(user) == 0:
            context = {}
            return HttpResponse(template.render(context, request))     