from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.urls import reverse
from datetime import datetime
from .models import Company, User
import io,csv
from django.shortcuts import redirect


# Tạo đối tượng Company để hiển thị lên view
class CompanyView:
    id=0;
    stocks="";
    company_name="";
    company_cap=0;
    current_price=0;
    r_o_a=0;
    p_e=0;
    efficiency_level=0;
    date_update=datetime.now()
    # Constructor
    def __init__(self, id, stocks, company_name, company_cap, current_price, r_o_a, p_e, efficiency_level, date_update):
        self.stocks = stocks;
        self.company_name = company_name;
        self.company_cap = company_cap;
        self.current_price = current_price;
        self.r_o_a = r_o_a;
        self.p_e = p_e;
        self.efficiency_level = efficiency_level;
        self.date_update = date_update;
        self.id = id;

# Xử lí hiển thị MH danh sách công ty
def index(request):
    try:
        # Kiểm tra login
        username=request.session.get('member_id', '')
        log = 0
        # Lấy ra data từ CSDL để hiển thị ở MH danh sách
        company_list_db = Company.objects.order_by('-efficiency_level')
        # Lấy template hiển thị
        template = loader.get_template('stocks/index.html')
        # Tạo danh sách đối tượng company mới có thuộc tính index để hiển thị STT table
        company_list_view = []
        for company in company_list_db:
            company_view = CompanyView(0, company.stocks, company.company_name, company.company_cap, company.current_price, company.r_o_a, company.p_e, company.efficiency_level, company.date_update)
            company_list_view.append(company_view)
        for index in range(len(company_list_view)):
            company_list_view[index].id=index+1
        context = {}
        if username != "" :
            log = 1
        else: 
            log = 0
        context = {
            'log': log,
            'username':username,
            'company_list_view': company_list_view,
        }  
    except Company.DoesNotExist:
        raise Http404('Company does not exist')
    return HttpResponse(template.render(context, request))   
