from django.http import HttpResponse, Http404
from django.template import loader
from datetime import datetime, timedelta
from .models import Company, User
from django.conf import settings

# Xử lí hiển thị MH danh sách công ty
def index(request):
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
        # Kiểm tra login
        username=request.session.get('member_id', '')
        log = 0
        # Lấy ra data từ CSDL để hiển thị ở MH danh sách
        company_list_db = Company.objects.order_by('magic_formula')
        # Lấy template hiển thị
        template = loader.get_template('stocks/index.html')
        # Thay đổi lại thuộc tính id dùng hiển thị STT
        for index in range(len(company_list_db)):
            company_list_db[index].id=index+1
        context = {}
        avatar = "1"
        # Lấy ra thông tin user từ DB
        user = User.objects.filter(user_name=username)    
        if len(user) != 0:
            avatar = user[0].avatar            
        context = {
            'username':username,
            'company_list_view': company_list_db,
            'user': user,
            'avatar': avatar
        }  
    except Company.DoesNotExist:
        raise Http404('Company does not exist')
    return HttpResponse(template.render(context, request))   
