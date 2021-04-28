from django.db import models
#Tạo bảng các công ty và các thuộc tính tương ứng
class Company(models.Model):
    # Mã cổ phiếu	
    stocks = models.TextField()
    # Giá trị sổ sách
    book_value = models.DecimalField(decimal_places=2, max_digits=15)
    # Giá hiện tại
    current_price = models.DecimalField(decimal_places=2, max_digits=15)
    # ROA (%)
    r_o_a =  models.DecimalField(decimal_places=2, max_digits=15)
    # P/E
    p_or_e =  models.DecimalField(decimal_places=2, max_digits=15)
    # Giá thấp nhất trong 52 tuần
    lowest_price_in_52w =  models.DecimalField(decimal_places=2, max_digits=15)
    # Khoảng cách
    difference =  models.DecimalField(decimal_places=2, max_digits=15)
    # Khối lượng lưu thông
    masses_in_circulation =  models.BigIntegerField()
    # Giá trị công ty
    company_value =  models.BigIntegerField()
    # ESP
    e_s_p =  models.DecimalField(decimal_places=2, max_digits=15)
    # ROE
    r_o_e =  models.DecimalField(decimal_places=2, max_digits=15)
    # P/B
    p_or_b =  models.DecimalField(decimal_places=2, max_digits=15)
    # Công thức kì diệu
    magic_formula =  models.DecimalField(decimal_places=1, max_digits=15)
    # Đủ lớn
    is_big_enough = models.NullBooleanField()
    # Thấp nhất
    is_lowest = models.NullBooleanField()
    # Ngày cập nhật
    date_update = models.DateField(null=True, blank=True)

#Tạo bảng các công ty và các thuộc tính tương ứng
class User(models.Model):
    # User name	
    user_name = models.CharField(max_length=50, primary_key=True)
    # pass word
    password = models.CharField(max_length=16)
    # Vốn cá nhân
    capital = models.CharField(max_length=50)
    # Avatar
    avatar = models.ImageField(upload_to='')

