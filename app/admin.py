from datetime import datetime

from app import  db,app,dao
from app.models import Phong, LoaiPhong, NguoiDung, LoginRole
from flask_admin.contrib.sqla import ModelView
from flask_admin import  BaseView,expose, AdminIndexView,Admin
from flask_login import  logout_user,current_user
from flask import  redirect, request



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



class MyAdminView(AdminIndexView):
    @expose('/')
    def index(self):
        stats=dao.Revenue_Stats()
        count = 0
        tongdoanhthu=0
        daycount=0
        stats2 = dao.Usage_Stats()
        for c in stats:
            count += c['soluotthue']
            tongdoanhthu+=c['doanhthu']
        for c in stats2:
            if c['songay']==None:
                pass
            else:
                daycount+=c['songay']
        return self.render('admin/index.html',stats=stats, count=count,tongdoanhthu=tongdoanhthu,stats2=stats2,daycount=daycount)


admin = Admin(app=app, name='Quản trị bán hàng',
              template_mode='bootstrap4', index_view=MyAdminView())


class ForRent(AuthenticatedBaseView):
        @expose('/',methods=['post','get'])
        def __index__(self):
            if request.method =="POST":
                ngaynhan = request.form.get('ngaynhan')
                ngaytra = request.form.get('ngaytra')
                nhanvien = request.form.get('nhanvien')
                try:
                      dao.Thue_Phong(ngaynhan=ngaynhan, ngaytra=ngaytra, nhanvien=nhanvien)
                except:
                    pass
                PhieuThuePhong=dao.get_PhieuThuePhong()
                hoten = request.form.get('khachhang')
                cmnd = request.form.get('cmnd')
                diachi = request.form.get('diachi')
                quocgia = request.form.get('quocgia')
                dao.CapNhat_ThuePhong(PhieuThuePhong, hoten=hoten, cmnd=cmnd, diachi=diachi, quocgia=quocgia)
                phongid = request.form.get('phongid')
                dao.CapNhat_PhongThue(PhieuThuePhong=PhieuThuePhong, phongid=phongid)
            return self.render('admin/rent.html')
admin.add_view(RoomCategoryView(LoaiPhong,db.session, name='Loại Phòng'))
admin.add_view(RoomView(Phong,db.session,name = 'Phòng'))
admin.add_view((AuthenticatedModelView(NguoiDung,db.session,name='Người dùng')))
admin.add_view(StatsView(name='Thong ke'))
admin.add_view(ForRent(name='Cho Thue'))
admin.add_view(LogoutView(name='dang xuat'))