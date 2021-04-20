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

# Xử lí hiển thị trường hợp search
def search(request):
    try:
        # Get dữ liệu từ session
        username=request.session.get('member_id', '')
        log = 0
        # Get dữ liệu từ request
        company_capital = request.POST['company_cap']
        count_company = request.POST['count_company']
        date_update = request.POST['date_update']
        request.session['company_cap'] = company_capital
        request.session['count_company'] = count_company
        request.session['date_update'] = date_update
        # Khởi tạo danh sách công ty
        company_list_db = []
        company_list = []
        company_list_view= []
        # Thay đổi format date lấy từ form để thực hiện get data từ Db
        date_update_change_format = change_format_date_update(date_update)
        # Xử lí các trường hợp với các điều kiện tìm kiếm tương ứng có hoặc không có ngày tìm kiếm, số record
        if (date_update != "" and count_company !=""):
            date_update_view = datetime.strptime(date_update_change_format, "%Y-%m-%d")
            count_record = int(count_company)
            company_list_db = Company.objects.filter(date_update=date_update_view).order_by('-efficiency_level')[:count_record]
        elif (date_update != "" and count_company ==""):
            date_update_view = datetime.strptime(date_update_change_format, "%Y-%m-%d")
            company_list_db = Company.objects.filter(date_update=date_update_view).order_by('-efficiency_level')
        elif (date_update == "" and count_company !=""):
            count_record = int(count_company)
            company_list_db = Company.objects.all().order_by('-efficiency_level')[:count_record]
        elif (date_update == "" and count_company ==""):
            company_list_db = Company.objects.all().order_by('-efficiency_level')

        # Tìm kiếm với công ty có số vốn lớn hơn vốn công ty(nếu có) lấy được từ request 
        if (company_capital != ""):

            company_capital_validate = int(company_capital) 
            for company in company_list_db :
                if (int(company.company_cap) >= company_capital_validate):
                    company_list.append(company)
        else:
            company_list = company_list_db
        # Tạo danh sách đối tượng company mới có thuộc tính index để hiển thị STT table
        for company in company_list:
            company_view = CompanyView(0, company.stocks, company.company_name, company.company_cap, company.current_price, company.r_o_a, company.p_e, company.efficiency_level, company.date_update)
            company_list_view.append(company_view)
        # Duyệt các chỉ số hiển thị của mỗi record
        for index in range(len(company_list_view)):
            company_list_view[index].id=index+1
        # Lấy ra số lượng thực tế các công ty thỏa mãn điều kiện tìm kiếm
        len_company = len(company_list_view)
        # Get ra template theo đường dẫn tương ứng để set hiển thị
        template = loader.get_template('stocks/index.html')
        # Tạo 1 Dictionary đưa lên template hiển thị 
        if username != "" :
            log = 1
        else: 
            log = 0
        context = {
            'log': log,
            'username': username,
            'date_update_view': date_update,
            'len_company': len_company,
            'count_record_view': count_company,
            'company_capital_view': company_capital,
            'company_list_view': company_list_view,
        }
    except (KeyError, Company.DoesNotExist):
        raise Http404('Company does not exist')
    # Xử lí thông báo lỗi khi dữ liệu tìm kiếm từ form sai format
    except ValueError:
        message = ''
        message2 = ''
        message3 = ''
        # Validate khi nhập điều kiện tìm kiếm theo vốn công ty
        if (company_capital != ""):
            try:
                int(company_capital)
            except ValueError:
                message = "Vốn công ty chỉ chứa số half size."
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
        # Tạo 1 Dictionary đưa lên template hiển thị 
        disable_buy_sell = false
        context = {
                    'date_update_view': date_update,                    
                    'count_record_view': count_company,
                    'company_capital_view': company_capital,
                    'message': message,
                    'message2': message2,
                    'message3': message3,
                    'company_list_view': company_list_view,
                    'disable_buy_sell' : disable_buy_sell 
                }

    # Trả về dữ liệu hiển thị trên tempalte
    return HttpResponse(template.render(context, request))

# Thay đổi format date từ dd/mm/yyyy --> yyyy-mm-dd
def change_format_date_update(date_update):
    date_update_view = ""
    date_update_view_list = date_update.split("/")
    if (date_update != ""):
        for index in range(len(date_update_view_list)):
            if (index == 0) :
                date_update_view = str(date_update_view_list[index])
            else:
                date_update_view = str(date_update_view_list[index]) + "-" + date_update_view
    return date_update_view

# Xử lí upload file
def profile_upload(request):
    # Lấy mẫu template
    template = 'stocks/profile_upload.html'
    data = Company.objects.all()
    # Tạo 1 Dictionary đưa lên template hiển thị 
    prompt = {
        'profiles': data    
    }
    # Xử lí hiển thị ban đầu khi vào trang upload file
    if request.method == "GET":
        return render(request, template, prompt)
    csv_file = request.FILES['profile_upload']
    # Kiểm tra xem tệp đầu vào phải là tệp csv không
    if not csv_file.name.endswith('.csv'):
        context = {
            'messages': "File upload không phải tệp csv"
        }
        # Trả về template hiển thị sau khi upload file thất bại
        return render(request, template, context)
    data_set = csv_file.read().decode('UTF-8')
    # setup a stream which is when we loop through each line we are able to handle a data in a stream
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = Company.objects.update_or_create(
            stocks=column[0],
            company_name=column[1],
            company_cap=column[2],
            current_price=column[3],
            r_o_a=column[4],
            p_e=column[5],
            efficiency_level=column[6],
            date_update=datetime.now(),
        )
    # Tạo 1 Dictionary đưa lên template hiển thị 
    context = {
       'messages': "Upload file thành công"
    }
    # Trả về template hiển thị sau khi upload file thành công
    return render(request, template, context)

# Xử lí login
def login(request):
    # Thực hiện xóa các điều kiện tìm kiếm (nếu có) ở MH danh sách hiện tại trên session
    if request.session.get('company_cap','') != "":
        del request.session['company_cap'] 
    if request.session.get('count_company','') != "":
        del request.session['count_company'] 
    if request.session.get('date_update','') != "":        
        del request.session['date_update']     
    if request.method == 'POST':
        # Get dữ liệu từ request
        user_name_views = request.POST.get('user_name', "")
        password_views = request.POST.get('password', "")
        user = User.objects.filter(user_name=user_name_views, password=password_views)
        # Get ra template theo đường dẫn tương ứng để set hiển thị
        template = loader.get_template('stocks/login_user.html')
        # Kiểm tra tồn tại của user login
        # Nếu user không tồn tại trong CSDL thì gửi thông báo lỗi và yêu cầu login lại
        if len(user) == 0:
            message = "Login không thành công, vui lòng thử lại"
            context = {
                'message': message
            }
            return HttpResponse(template.render(context, request))
        # Nếu user có tồn tại trong CSDL thì qua trở về MH danh sách lưu trạng thái đã đăng nhập lên session
        else:
            username = ""
            context ={}
            for user in user:
                username = user.user_name
                request.session['member_id'] = user.user_name
            try:
                company_list_db = Company.objects.order_by('-efficiency_level')
                template = loader.get_template('stocks/index.html')
                # Tạo danh sách đối tượng company mới có thuộc tính index để hiển thị STT table
                company_list_view = []
                for company in company_list_db:
                    company_view = CompanyView(0, company.stocks, company.company_name, company.company_cap, company.current_price, company.r_o_a, company.p_e, company.efficiency_level, company.date_update)
                    company_list_view.append(company_view)
                for index in range(len(company_list_view)):
                    company_list_view[index].id=index+1
                if username != "" :
                    log = 1
                else: 
                    log = 0               
                context = {
                    'log': log,
                    'username': username,
                    'company_list_view': company_list_view,
                }  
            except Company.DoesNotExist:
                raise Http404('Company does not exist')
            return HttpResponse(template.render(context, request))        
    else:
        # Get dữ liệu từ request
        user_name_views = request.POST.get('user_name', "")
        password_views = request.POST.get('password', "")
        user = User.objects.filter(user_name=user_name_views, password=password_views)
        # Get ra template theo đường dẫn tương ứng để set hiển thị
        template = loader.get_template('stocks/login_user.html')
        if len(user) == 0:
            context = {
            }
            return HttpResponse(template.render(context, request))        
   
# Xử lí sign up
def signup(request):
    # Thực hiện xóa các điều kiện tìm kiếm (nếu có) ở MH danh sách hiện tại trên session
    if request.session.get('company_cap','') != "":
        del request.session['company_cap'] 
    if request.session.get('count_company','') != "":
        del request.session['count_company'] 
    if request.session.get('date_update','') != "":        
        del request.session['date_update'] 
    # Lấy dữ liệu từ request và thực hiện sign up 
    if request.method == 'POST':
        # Get dữ liệu từ request để thực hiện sign up
        user_name_views = request.POST.get('user_name', "")
        password_views = request.POST.get('password', "")
        message = ""
        # Thực hiện sign up thông tin user và CSDL, kiểm tra có sign up thành công hay không và gửi câu thông báo tương ứng
        if (user_name_views != "" and password_views != ""):
            user = User.objects.update_or_create(user_name=user_name_views, password=password_views)
            message = "Đăng kí thành công, vui lòng quay về trang chủ để login"
        else:
            message = "Đăng kí không thành công, vui lòng nhập đầy đủ username và password"
        context = {
            'message': message
        }
    # Xử lí hiển thị ban đầu MH sign up 
    else:
        context = {}
    return render(request, 'stocks/signup_user.html', context)

# Xử lí export file csv
def export_csv(request):
    # Get điều kiện tìm kiếm từ session nếu có để thực hiện export data tương ứng
    company_capital = request.session.get("company_cap", "")
    count_company = request.session.get('count_company', "")
    date_update = request.session.get('date_update', "")
    # Khởi tạo danh sách công ty
    company_list_db = []
    company_list = []
    company_list_view= []
    # Thay đổi format date lấy từ form để thực hiện get data từ Db
    date_update_change_format = change_format_date_update(date_update)
    # Xử lí các trường hợp với các điều kiện tìm kiếm tương ứng có hoặc không có ngày tìm kiếm, số record
    if (date_update != "" and count_company !=""):
        date_update_view = datetime.strptime(date_update_change_format, "%Y-%m-%d")
        count_record = int(count_company)
        company_list_db = Company.objects.filter(date_update=date_update_view).order_by('-efficiency_level')[:count_record]
    elif (date_update != "" and count_company ==""):
        date_update_view = datetime.strptime(date_update_change_format, "%Y-%m-%d")
        company_list_db = Company.objects.filter(date_update=date_update_view).order_by('-efficiency_level')
    elif (date_update == "" and count_company !=""):
        count_record = int(count_company)
        company_list_db = Company.objects.all().order_by('-efficiency_level')[:count_record]
    elif (date_update == "" and count_company ==""):
        company_list_db = Company.objects.all().order_by('-efficiency_level')

    # Tìm kiếm với công ty có số vốn lớn hơn vốn công ty(nếu có) lấy được từ request 
    if (company_capital != ""):
        company_capital_validate = int(company_capital) 
        for company in company_list_db :
            if (int(company.company_cap) >= company_capital_validate):
                company_list.append(company)
    else:
        company_list = company_list_db

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="stocks.csv"'

    writer = csv.writer(response)
    writer.writerow(['company_name', 'company_cap'])

    for company in company_list:
        writer.writerow([company.company_name, company.company_cap])

    return response

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
