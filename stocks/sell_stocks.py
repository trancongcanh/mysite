from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from datetime import datetime, timedelta
from .models import Company, User, History
from django.shortcuts import redirect
from django.conf import settings
import math

# Xử lí bán cổ phiếu
def sell_stocks(request):
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
    list_stocks = []
    list_current_price = []
    list_count_stocks = []
    # Tạo template hiển thị ban đầu
    template = loader.get_template('stocks/sell_stock.html')
    # Cập nhật giá mới nhất của cổ phiếu trước khi bán,khởi tạo danh sách cổ phiếu và số lượng cổ phiếu user nắm giữ
    for company in company_list_db:
        list_stocks.append(company.stock)
        list_count_stocks.append(company.count_stocks)
        for i in range(len(company_list_current)):
            if company_list_current[i].stocks == company.stock:
                company.capital_end = company_list_current[i].current_price
                list_current_price.append(company_list_current[i].current_price)
    # Tạo 1 context set các giá trị hiển thị ban đầu khi tới MH Bán cổ phiếu
    context = {
        'capital': 0,
        'count_stocks': 0,
        'list_count_stocks': list_count_stocks,
        'list_current_price': list_current_price,
        'list_stocks': list_stocks,
        'capital_user': capital_user,
    }
    # Xử lí khi thực hiện giao dịch
    if request.method =='POST':
        # Get stocks từ request
        stock_view = request.POST.get('stock', '')
        capital_hidden = float(request.POST.get('capital_hidden', 0))
        count_stocks = int(request.POST.get('count_stocks', 0))
        count_stocks_db = 0
        transaction_status = 1
        capital_start = 0
        # Lấy ra tất cả số lượng của cổ phiếu muốn bán trong DB
        for i in range(len(company_list_db)):
            if company_list_db[i].stock == stock_view:
                count_stocks_db = company_list_db[i].count_stocks
                capital_start = company_list_db[i].capital_start
                break;
        if count_stocks == count_stocks_db:
            transaction_status = 0
        if int(count_stocks) <= count_stocks_db and count_stocks > 0:
            e = (capital_hidden/float(capital_start))*100
            update_history_buy = History.objects.filter(stock=stock_view, managed_by=username, transaction_status=1).update(end_date=datetime.now(), count_stocks=count_stocks_db-count_stocks, capital_end=capital_hidden, transaction_status= transaction_status, e=e)
            update_capital_user = User.objects.filter(user_name=username).update(capital=int(capital_user+math.ceil(count_stocks*capital_hidden)))
            capital_user = int(capital_user+math.ceil(count_stocks*capital_hidden))
            message = "Giao dịch thành công"
        else:
            message = "Bán quá số lượng sở hữu"
        # Lấy ra tất cả cố phiếu mà user nắm giữ trong db
        company_list_db = History.objects.order_by('capital_start').filter(managed_by=username, transaction_status=1)
        # Lấy ra danh sách cổ phiếu cập nhật của ngày hiện tại
        company_list_current = Company.objects.order_by('magic_formula').filter(date_update=datetime.now())
        # Khởi tạo lại ds cổ phiếu, số lượng cổ phiếu và giá tương ứng của user nắm giữ để hiển thị
        list_stocks = []
        list_current_price = []
        list_count_stocks = []
        # Cập nhật giá mới nhất của cổ phiếu trước khi bán,khởi tạo danh sách cổ phiếu và số lượng cổ phiếu user nắm giữ
        for company in company_list_db:
            list_stocks.append(company.stock)
            list_count_stocks.append(company.count_stocks)
            for i in range(len(company_list_current)):
                if company_list_current[i].stocks == company.stock:
                    company.capital_end = company_list_current[i].current_price
                    list_current_price.append(company_list_current[i].current_price)
        # Tạo 1 context set các giá trị hiển thị khi click button thực hiện giao dịch ở MH bán cổ phiếu
        context = {
            'list_count_stocks': list_count_stocks,
            'list_current_price': list_current_price,
            'list_stocks': list_stocks,
            'capital_user': capital_user,
            'message': message,
            'capital': 0,
            'count_stocks': 0,
        }
    # Thực hiện hiển thị MH
    return HttpResponse(template.render(context, request))