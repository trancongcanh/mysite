from django.http import HttpResponse, Http404
from django.template import loader
from datetime import datetime, timedelta
from .models import Company, User
from django.conf import settings
from .common import change_format_date_update, fomat_number

# Xử lí hiển thị trường hợp search
def search(request):
    try:
        # Kiểm tra session time out        
        if request.session.get('last_touch',"") != "" :
            # Logout nếu quá session
            if datetime.now() - request.session['last_touch']> timedelta( 0, settings.AUTO_LOGOUT_DELAY * 60, 0):
                member_id = request.session.get('member_id',"")
                del request.session['last_touch']
                if member_id != "":
                    del request.session['member_id']
            # Nếu chưa quá session thì thực hiện reset lại session
            else:
                request.session['last_touch'] = datetime.now()
        # Logout nếu quá session
        else:
            member_id = request.session.get('member_id',"")
            if member_id != "":
                del request.session['member_id']
        # Get dữ liệu từ session
        username=request.session.get('member_id', '')
        log = 0
        # Get dữ liệu từ request
        company_value = request.POST.get('company_value', '')
        count_company = request.POST.get('count_company', '')
        date_update = request.POST.get('date_update', '')
        request.session['company_value'] = company_value
        request.session['count_company'] = count_company
        request.session['date_update'] = date_update
        # Khởi tạo danh sách công ty
        company_list_db = []
        company_list_view= []
        # Thay đổi format date lấy từ form để thực hiện get data từ Db
        date_update_change_format = change_format_date_update(date_update)
        # Xử lí các trường hợp với các điều kiện tìm kiếm tương ứng có hoặc không có ngày tìm kiếm
        if (date_update != ""):
            date_update_view = datetime.strptime(date_update_change_format, "%Y-%m-%d")
            company_list_db = Company.objects.filter(date_update=date_update_view).order_by('magic_formula')
        else:
            company_list_db = Company.objects.all().order_by('magic_formula')
        # Tìm kiếm với công ty có số vốn lớn hơn vốn công ty(nếu có) lấy được từ request 
        if company_value != "":
            company_value_validate = int(company_value)
        else:
            company_value_validate = 0
        # Lấy ra số lượng record mong muốn hiển thị
        if count_company != "":
            count_record = int(count_company)
        else:
            count_record = len(company_list_db)
        # Duyệt danh sách lấy từ DB theo ngày tìm kiếm (nếu có) và lọc ra theo giá trị công ty và số record muốn hiển thị
        for i in range(len(company_list_db)):
            if int(company_list_db[i].company_value) >= company_value_validate and len(company_list_view) < count_record:
                company_list_db[i].id = len(company_list_view)+1
                company_list_db[i].company_value=fomat_number(company_list_db[i].company_value)
                company_list_db[i].current_price=fomat_number(company_list_db[i].current_price)
                company_list_view.append(company_list_db[i])
        # Lấy ra số lượng thực tế các công ty thỏa mãn điều kiện tìm kiếm
        len_company = len(company_list_view)
        # Get ra template theo đường dẫn tương ứng để set hiển thị
        template = loader.get_template('stocks/index.html')
        if username != "" :
            user = User.objects.filter(user_name=username)    
            if len(user) != 0:
                avatar = user[0].avatar
        else: 
            avatar="1"
        # Tạo 1 Dictionary đưa lên template hiển thị 
        context = {
            'username': username,
            'date_update_view': date_update,
            'len_company': len_company,
            'count_record_view': count_company,
            'company_value_view': company_value,
            'company_list_view': company_list_view,
            'avatar': avatar
        }
    except (KeyError, Company.DoesNotExist):
        raise Http404('Company does not exist')
    # Xử lí thông báo lỗi khi dữ liệu tìm kiếm từ form sai format
    except ValueError:
        message = ''
        message2 = ''
        message3 = ''
        # Validate khi nhập điều kiện tìm kiếm theo vốn công ty
        if (company_value != ""):
            try:
                int(company_value)
            except ValueError:
                message = "Giá trị của công ty chỉ chứa số half size."
        # Validate khi nhập điều kiện tìm kiếm số công ty muốn hiển thị
        if (count_company !=""):
            try:
                int(count_company)
            except ValueError:
                message2 = "Số record chỉ chứa số half size."
        # Validate khi nhập điều kiện tìm kiếm ngày cập nhật công ty
        if (date_update !=""):
            try:
                date_update_view = datetime.strptime(change_format_date_update(date_update), "%Y-%m-%d")
            except ValueError:
                message3 = "Ngày tìm kiếm sai định dạng." 
        # Do điều kiện tìm kiếm sai format nên khởi tạo 1 danh sách rỗng để hiển thị    
        company_list_view=[]
        # Get ra template theo đường dẫn tương ứng để set hiển thị
        template = loader.get_template('stocks/index.html')
        if username != "" :
            user = User.objects.filter(user_name=username)    
            if len(user) != 0:
                for user in user:
                    avatar = user.avatar
        else: 
            avatar="1"
        # Tạo 1 Dictionary đưa lên template hiển thị 
        context = {
            'date_update_view': date_update,                    
            'count_record_view': count_company,
            'company_value_view': company_value,
            'message': message,
            'message2': message2,
            'message3': message3,
            'company_list_view': company_list_view,
            'avatar':avatar,
            'username': username,
        }

    # Trả về dữ liệu hiển thị trên tempalte
    return HttpResponse(template.render(context, request))
