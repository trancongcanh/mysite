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

# Thay đổi định dạng hiển thị mỗi 1000 lần sé ngăn bởi "."
def fomat_number(number):
    string_number = ""
    scout_zero = 0
    string_reverse = reverse_string(number)
    for i in range(len(string_reverse)):
        if string_reverse[i] == ".":
            scout_zero = 0
            string_number += ","
        else:
            if scout_zero == 3 :
                string_number += "."
                scout_zero = 0
            scout_zero += 1
            string_number += string_reverse[i]
    string_number = reverse_string(string_number)
    return string_number

# Hàm đảo ngược chuỗi
def reverse_string (string):
    string_handle = str(string)
    string_reverse = ""
    len_string=len(string_handle)-1
    while (len_string>=0):
        string_reverse+=string_handle[len_string]
        len_string-=1
    return string_reverse
