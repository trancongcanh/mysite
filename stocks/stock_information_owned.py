from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.urls import reverse
from datetime import datetime, timedelta
from .models import Company, User, History
from django.shortcuts import redirect
from django.conf import settings
import math
from .common import fomat_number, reverse_string


def stock_information_owned(request):
    # Kiểm tra session time out        
    if request.session.get('last_touch',"") != "" :
        # Logout và Quay lại MH login nếu quá session
        if datetime.now() - request.session['last_touch']> timedelta( 0, settings.AUTO_LOGOUT_DELAY * 60, 0):
            member_id = request.session.get('member_id',"")
            del request.session['last_touch']
            if member_id != "":
                del request.session['member_id']
                return redirect("stocks:login")
        # Nếu chưa quá session thì thực hiện reset lại session
        else:
            request.session['last_touch'] = datetime.now()
    # Logout và Quay lại MH login nếu quá session
    else:
        member_id = request.session.get('member_id',"")
        if member_id != "":
            del request.session['member_id']
            return redirect("stocks:login")  
    # Get dữ liệu từ session
    username=request.session.get('member_id', '')
    # Lấy ra thông tin user từ DB
    user = User.objects.filter(user_name=username)
    capital_user = 0
    if len(user) != 0:
        capital_user = user[0].capital
    # Thực hiện xóa các điều kiện tìm kiếm (nếu có) ở MH danh sách hiện tại trên session
    if request.session.get('company_value','') != "":
        del request.session['company_value'] 
    if request.session.get('count_company','') != "":
        del request.session['count_company'] 
    if request.session.get('date_update','') != "":        
        del request.session['date_update'] 
    # Lấy ra tất cả cố phiếu mà user nắm giữ trong db
    company_list_db = History.objects.order_by('capital_start').filter(managed_by=username, transaction_status=1)
    # Lấy ra danh sách cổ phiếu cập nhật của ngày hiện tại
    company_list_current = Company.objects.order_by('magic_formula').filter(date_update=datetime.now())
    # Cập nhật giá mới nhất của cổ phiếu trước khi bán,khởi tạo danh sách cổ phiếu và số lượng cổ phiếu user nắm giữ
    id = 1
    for company in company_list_db:
        company.id = id
        for i in range(len(company_list_current)):
            if company_list_current[i].stocks == company.stock:
                company.stock = company_list_current[i].stocks
                company.capital_end = company_list_current[i].current_price
                company.e = round(((company.capital_end-company.capital_start)/company.capital_start) *100, 2)
        id+=1
    # Tạo template hiển thị
    template = loader.get_template('stocks/stock_information_owned.html')
    # Tạo 1 context set các giá trị hiển thị ban đầu khi tới MH Bán cổ phiếu
    context = {
        'company_list_view': company_list_db,
        'capital_user': capital_user,
    }
    
    return HttpResponse(template.render(context, request))