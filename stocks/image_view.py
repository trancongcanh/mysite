from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
from django.template import loader
from .models import Company, User
from .company_view import CompanyView

  
# Create your views here.
def image_view(request):
    try:
        # Kiểm tra login
        username=request.session.get('member_id', '')
        log = 0
        # Lấy ra data từ CSDL để hiển thị ở MH danh sách
        company_list_db = Company.objects.order_by('-magic_formula')
        # Lấy template hiển thị
        template = loader.get_template('stocks/index.html')
        # Tạo danh sách đối tượng company mới có thuộc tính index để hiển thị STT table
        company_list_view = []
        for company in company_list_db:
            company_view = CompanyView(0, company.stocks, company.current_price, company.p_or_e, company.company_value, company.r_o_a, company.magic_formula, company.date_update)
            company_list_view.append(company_view)
        for index in range(len(company_list_view)):
            company_list_view[index].id=index+1
        context = {}
        if username != "" :
            update = User.objects.filter(user_name=username).update(avatar=request.FILES.get('avatar', "1"))
        # Lấy ra thông tin user từ DB
        user = User.objects.filter(user_name=username)
        avatar = "1"
        if len(user) != 0:
            for user in user:
                avatar = user.avatar
        context = {
            'username':username,
            'company_list_view': company_list_view,
            'avatar': avatar
        }   
        if request.method == 'POST':
            form = ImageForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
        else:
            form = ImageForm()
            return render(request, 'stocks/image_form.html', {'form' : form})
    except Company.DoesNotExist:
        raise Http404('Company does not exist')
    except Exception:
        return HttpResponse(template.render(context, request))   
    return HttpResponse(template.render(context, request))   
