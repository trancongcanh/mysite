from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from datetime import datetime, timedelta
from .models import Company, User, History, Deal
from django.shortcuts import redirect
from django.conf import settings
import math
from .common import fomat_number


# XỬ lí mua cổ phiếu
def buy_stocks(request):
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
    # Lấy ra data từ CSDL để hiển thị ở MH danh sách
    company_list_db = Company.objects.order_by('magic_formula').filter(date_update=datetime.now())
    list_stocks = []
    list_current_price = []
    template = loader.get_template('stocks/buy_stock.html')
    for company in company_list_db:
        list_stocks.append(company.stocks)
        list_current_price.append(company.current_price)
    context = {
        'capital': 0,
        'count_stocks': 0,
        'list_current_price': list_current_price,
        'list_stocks': list_stocks,
        'capital_user': capital_user,
        'capital_user_format': fomat_number(capital_user),
    }
    # Xử lí khi thực hiện giao dịch
    if request.method =='POST':
        # Get stocks từ request
        stock_view = request.POST.get('stock', '')
        capital_hidden = float(request.POST.get('capital_hidden', 0))
        count_stocks = int(request.POST.get('count_stocks', 0))
        if count_stocks*capital_hidden <= capital_user and count_stocks > 0:
            History.objects.create(managed_by=username, stock=stock_view, deal_date=datetime.now(), count_stocks=count_stocks, capital_deal=capital_hidden, transaction_status= 1, )
            User.objects.filter(user_name=username).update(capital=int(capital_user-math.ceil(count_stocks*capital_hidden)))
            capital_user = int(capital_user-math.ceil(count_stocks*capital_hidden))
            list_stock_user_owned = Deal.objects.filter(user_owned=username)
            list_stock_code_user_owned = []
            for stock in list_stock_user_owned:
                list_stock_code_user_owned.append(stock.stock_code)
            if stock_view in list_stock_code_user_owned:
                capital_buy_stock = 0
                count_stock_owned = 0
                for stock in list_stock_user_owned:
                    if stock.stock_code == stock_view:
                        capital_buy_stock = stock.capital_buy_stock
                        count_stock_owned = stock.count_stock_owned
                Deal.objects.filter(stock_code=stock_view).update(capital_buy_stock=capital_buy_stock+(capital_hidden*count_stocks), count_stock_owned=count_stock_owned+count_stocks)
            else:
                Deal.objects.filter(stock_code=stock_view).create(stock_code=stock_view, capital_buy_stock=capital_hidden*count_stocks, count_stock_owned=count_stocks, user_owned= username)
            message = "Giao dịch thành công"
        else:
            message = "Giao dịch không thành công"
        context = {
            'list_current_price': list_current_price,
            'list_stocks': list_stocks,
            'capital_user': capital_user,
            'capital_user_format': fomat_number(capital_user),
            'message': message,
            'capital': 0,
            'count_stocks': 0,
        }

    return HttpResponse(template.render(context, request))