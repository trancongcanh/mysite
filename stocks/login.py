from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.urls import reverse
from datetime import datetime
from .models import Company, User
from django.shortcuts import redirect


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
        # Nếu user có tồn tại trong CSDL thì qua trở về MH danh sách lưu trạng thái đã đăng nhập lên session
        else:
            username = ""
            context ={}
            for user in user:
                username = user.user_name
                request.session['member_id'] = user.user_name
            try:
                company_list_db = Company.objects.order_by('-efficiency_level')
                template = loader.get_template('stocks/index.html')
                # Tạo danh sách đối tượng company mới có thuộc tính index để hiển thị STT table
                company_list_view = []
                for company in company_list_db:
                    company_view = CompanyView(0, company.stocks, company.company_name, company.company_cap, company.current_price, company.r_o_a, company.p_e, company.efficiency_level, company.date_update)
                    company_list_view.append(company_view)
                for index in range(len(company_list_view)):
                    company_list_view[index].id=index+1
                if username != "" :
                    log = 1
                else: 
                    log = 0               
                context = {
                    'log': log,
                    'username': username,
                    'company_list_view': company_list_view,
                }  
            except Company.DoesNotExist:
                raise Http404('Company does not exist')
            return HttpResponse(template.render(context, request))        
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