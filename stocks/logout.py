from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.urls import reverse
from datetime import datetime
from .models import Company, User
import io,csv
from django.shortcuts import redirect

from .company_view import CompanyView

# Xử lí log out
def logout(request):
    try:
        # Xóa thông tin user khỏi session
        if request.session.get('member_id','') != "":
            del request.session['member_id']
        # Lấy ra data từ CSDL để hiển thị ở MH danh sách
        company_list_db = Company.objects.order_by('-efficiency_level')
        # Lấy template để hiển thị sau khi logout
        template = loader.get_template('stocks/index.html')
        # Tạo danh sách đối tượng company mới có thuộc tính index để hiển thị STT table
        company_list_view = []
        for company in company_list_db:
            company_view = CompanyView(0, company.stocks, company.company_name, company.company_cap, company.current_price, company.r_o_a, company.p_e, company.efficiency_level, company.date_update)
            company_list_view.append(company_view)
        for index in range(len(company_list_view)):
            company_list_view[index].id=index+1
        context = {}
        log = 0
        context = {
            'log': log,
            'company_list_view': company_list_view,
        }  
    except Company.DoesNotExist:
        raise Http404('Company does not exist')

    except KeyError:
        pass
    return HttpResponse(template.render(context, request))  