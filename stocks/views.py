from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.urls import reverse
from datetime import datetime, timedelta
from .models import Company, User
import io,csv
from django.shortcuts import redirect
from django.conf import settings


from .company_view import CompanyView

# Xử lí hiển thị MH danh sách công ty
def index(request):
    try:
        # Kiểm tra session time out 
        if request.session.get('last_touch',"") != "" :
            if datetime.now() - request.session['last_touch']> timedelta( 0, settings.AUTO_LOGOUT_DELAY * 60, 0):
                member_id = request.session.get('member_id',"")
                del request.session['last_touch']
                if member_id != "":
                    del request.session['member_id']
            else:
                request.session['last_touch'] = datetime.now()
        else:
            member_id = request.session.get('member_id',"")
            if member_id != "":
                del request.session['member_id']
        # Kiểm tra login
        username=request.session.get('member_id', '')
        log = 0
        # Lấy ra data từ CSDL để hiển thị ở MH danh sách
        company_list_db = Company.objects.order_by('-magic_formula')
        # Lấy template hiển thị
        template = loader.get_template('stocks/index.html')
        # Tạo danh sách đối tượng company mới có thuộc tính index để hiển thị STT table
        company_list_view = []
        for company in company_list_db:
            company_view = CompanyView(0, company.stocks, company.current_price, company.p_or_e, company.company_value, company.r_o_a, company.magic_formula, company.date_update)
            company_list_view.append(company_view)
        for index in range(len(company_list_view)):
            company_list_view[index].id=index+1
        context = {}
        avatar = "1"
        # Lấy ra thông tin user từ DB
        user = User.objects.filter(user_name=username)    
        if len(user) != 0:
            for user in user:
                avatar = user.avatar            
        context = {
            'username':username,
            'company_list_view': company_list_view,
            'user': user,
            'avatar': avatar
        }  
    except Company.DoesNotExist:
        raise Http404('Company does not exist')
    return HttpResponse(template.render(context, request))   
