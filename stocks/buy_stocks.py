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
    # Lấy ra thông tin user từ DB
    user = User.objects.filter(user_name=username)
    capital_company = ""
    if len(user) != 0:
        for user in user:
            capital_company = user.capital
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
    list_current_price = []
    template = loader.get_template('stocks/buy_stock.html')
    for company in company_list_db:
        list_stocks.append(company.stocks)
        list_current_price.append(company.current_price)
    context = {
        'list_current_price': list_current_price,
        'list_stocks': list_stocks,
        'capital_company': capital_company,
    }
    return HttpResponse(template.render(context, request))