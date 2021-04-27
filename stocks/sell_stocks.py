from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.urls import reverse
from datetime import datetime, timedelta
from .models import Company, User
from django.shortcuts import redirect
from django.conf import settings

def sell_stocks(request):
    # Kiểm tra session time out        
    if datetime.now() - request.session['last_touch'] > timedelta( 0, settings.AUTO_LOGOUT_DELAY * 60, 0):
        member_id = request.session.get('member_id',"")
        last_touch = request.session.get('last_touch',"")
        if member_id != "" and last_touch != "":
            del request.session['member_id']
            del request.session['last_touch']
        return redirect("http://127.0.0.1:8000/stocks/login/")
    else:
        request.session['last_touch'] = datetime.now()
    # Get dữ liệu từ session
    username=request.session.get('member_id', '')
    # Thực hiện xóa các điều kiện tìm kiếm (nếu có) ở MH danh sách hiện tại trên session
    if request.session.get('company_cap','') != "":
        del request.session['company_cap'] 
    if request.session.get('count_company','') != "":
        del request.session['count_company'] 
    if request.session.get('date_update','') != "":        
        del request.session['date_update'] 
    # Lấy ra data từ CSDL để hiển thị ở MH danh sách
    company_list_db = Company.objects.order_by('-efficiency_level')  
    list_stocks = []
    for company in company_list_db:
        list_stocks.append(company.stocks)  
    template = loader.get_template('stocks/sell_stock.html')
    context = {
        'list_stocks': list_stocks,
    }
    return HttpResponse(template.render(context, request))