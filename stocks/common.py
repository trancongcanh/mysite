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