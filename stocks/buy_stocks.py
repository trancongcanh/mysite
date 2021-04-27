from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.urls import reverse
from datetime import datetime, timedelta
from .models import Company, User
from django.shortcuts import redirect
from django.conf import settings


def buy_stocks(request):
    # Kiểm tra session time out        
    if datetime.now() - request.session['last_touch'] > timedelta( 0, settings.AUTO_LOGOUT_DELAY * 60, 0):
        member_id = request.session.get('member_id',"")
        last_touch = request.session.get('last_touch',"")
        if member_id != "" and last_touch != "":
            del request.session['member_id']
            del request.session['last_touch']
        return render(request, 'stocks/login_user.html', {})
    else:
        request.session['last_touch'] = datetime.now()
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