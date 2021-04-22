from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.urls import reverse
from datetime import datetime
from .models import Company, User
from django.shortcuts import redirect

def buy_stocks(request):
    # Get dữ liệu từ session
    username=request.session.get('member_id', '')
    # Get stocks từ request
    stock = request.POST.get('stock', '')
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
    template = loader.get_template('stocks/buy_stock.html')
    current_price = ""
    for company in company_list_db:
        if company.stocks == stock:
            current_price = company.current_price
        else:
            list_stocks.append(company.stocks)  
    context = {
        'current_price': current_price,
        'list_stocks': list_stocks,
        'stock': stock
    }
    return HttpResponse(template.render(context, request))