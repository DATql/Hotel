from app import admin, db,app
from app.models import Phong, LoaiPhong, NguoiDung, LoginRole
from flask_admin.contrib.sqla import ModelView
from flask_admin import  BaseView,expose, AdminIndexView,Admin
from flask_login import  logout_user,current_user
from flask import  redirect



# class MyAdminIndex(AdminIndexView):
#     def index(self):
#         return  self.render('/admin/index.html', msg="Hello")

class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role==LoginRole.Admin

class AuthenticatedBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and  (current_user.role==LoginRole.Admin or current_user.role==LoginRole.Staff)
class LogoutView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        logout_user()

        return redirect('/admin')


class StatsView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')


class RoomView(AuthenticatedModelView):
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    column_export_list = ['']
    column_filters = ['tenphong']
    column_searchable_list = ['tenphong']
    column_labels = { 'tenphong':'Tên Phòng',
                      'tinhtrang':'Tình Trạng',
                      'Loaiphong':'Loại Phòng'}
    form_excluded_columns = ['ThuePhong','DatPhong','ChiTietHoaDon']

class RoomCategoryView(AuthenticatedModelView):
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    column_exclude_list = ['image']
    column_filters = ['loaiphong']
    column_searchable_list = ['loaiphong']
    column_labels = {
                     'soluong': 'Số Lượng',
                     'sotiencancoc':'Số Tiền Cần Cọc',
                     'image': 'Hình Ảnh',
                     'dongia': 'Đơn Giá',
                     'sokhachtoida': ' Số Khách Tối Đa',
                     'loaiphong':'Loại Phòng'
                     }
    form_excluded_columns = ['Phong', 'ChiTietDoanhThu']

admin = Admin(app=app,name='Quản trị hotel',template_mode='bootstrap4')


admin.add_view(RoomCategoryView(LoaiPhong,db.session, name='Loại Phòng'))
admin.add_view(RoomView(Phong,db.session,name = 'Phòng'))
admin.add_view((AuthenticatedModelView(NguoiDung,db.session,name='Người dùng')))
admin.add_view(StatsView(name='Thong ke'))
admin.add_view(LogoutView(name='dang xuat'))