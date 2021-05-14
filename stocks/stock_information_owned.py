from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from datetime import datetime, timedelta
from .models import Company, User, Deal
from django.shortcuts import redirect
from django.conf import settings
from .common import fomat_number

# Xử lí hiển thị kết quả các giao dịch mua bán
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
    profit_user = 0
    capital_original_user = 0
    e = 0
    if len(user) != 0:
        capital_user = user[0].capital
        capital_original_user = user[0].capital_original
        if user[0].profit != None:
            profit_user = user[0].profit
            e = round((profit_user/capital_original_user) *100, 2)
    # Thực hiện xóa các điều kiện tìm kiếm (nếu có) ở MH danh sách hiện tại trên session
    if request.session.get('company_value','') != "":
        del request.session['company_value'] 
    if request.session.get('count_company','') != "":
        del request.session['count_company'] 
    if request.session.get('date_update','') != "":        
        del request.session['date_update'] 
    # Lấy ra tất cả cố phiếu mà user nắm giữ trong db
    company_list_db = Deal.objects.order_by('capital_buy_stock').filter(user_owned=username, count_stock_owned__gt=0)
    # Lấy ra danh sách cổ phiếu cập nhật của ngày hiện tại
    company_list_current = Company.objects.order_by('magic_formula').filter(date_update=datetime.now())
    # Cập nhật giá mới nhất của cổ phiếu trước khi bán,khởi tạo danh sách cổ phiếu và số lượng cổ phiếu user nắm giữ
    id = 1
    for company in company_list_db:
        company.id = id
        for i in range(len(company_list_current)):
            if company_list_current[i].stocks == company.stock_code and company.count_stock_owned != 0:
                company.transaction_prices = fomat_number(company_list_current[i].current_price)
                company.e = round(((float(company_list_current[i].current_price)-(company.capital_buy_stock/company.count_stock_owned))/(company.capital_buy_stock/company.count_stock_owned)) *100, 2)
        id+=1
    # Tạo template hiển thị
    template = loader.get_template('stocks/stock_information_owned.html')
    # Tạo 1 context set các giá trị hiển thị ban đầu khi tới MH Bán cổ phiếu
    context = {}
    if profit_user != 0 and e != 0:
        context = {
            'company_list_view': company_list_db,
            'capital_user': fomat_number(capital_user),
            'profit_user': fomat_number(profit_user),
            'profit_user_number': profit_user,
            'e': e
        }
    else:
        context = {
            'company_list_view': company_list_db,
            'capital_user': fomat_number(capital_user),
        }
    
    return HttpResponse(template.render(context, request))