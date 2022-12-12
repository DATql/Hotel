from app.models import NguoiDung,PhieuThuePhong, Phong, LoaiPhong, HoaDonThanhToan, ChiTietHoaDon, DSDatPhong, PhieuDatPhong,Phong_PhieuDatPhong,PhieuThuePhong_Phong,DSThuePhong
from app import db, utils
import hashlib
from sqlalchemy import func
from flask_login import current_user


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return NguoiDung.query.filter(NguoiDung.username.__eq__(username.strip()),
                                  NguoiDung.password.__eq__(password)).first()


def register(name, username, password, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = NguoiDung(hoten=name.strip(),
 username=username.strip(),
                  password=password,
                  cmnd=kwargs.get('cmnd'),
                  diachi=kwargs.get('diachi'),
                  avatar=kwargs.get('avatar'),
                  quocgia=kwargs.get('quocgia'),
                  role='User')
    db.session.add(u)
    db.session.commit()


def load_roomcategories(loaiphong=None):

    query = LoaiPhong.query

    if loaiphong:
        query = query.filter(LoaiPhong.loaiphong.contains(loaiphong))

    return query.all()


def load_fullroomcategories():
    return LoaiPhong.query.all()

def load_room():
    return Phong.query.all()


def get_user_by_id(user_id):
    return NguoiDung.query.get(user_id)

def get_phieu_dat_phong(user_id):
    return PhieuDatPhong.query.filter(PhieuDatPhong.nguoidat.__eq__(user_id)).all()

def get_danh_sach_dat_phong(user_id):
    query= db.session.query(DSDatPhong.id,DSDatPhong.hoten,DSDatPhong.cmnd,DSDatPhong.diachi)\
                     .join(PhieuDatPhong,PhieuDatPhong.id.__eq__(DSDatPhong.PhieuDatPhong_id).isouter)\
                     .join(NguoiDung,NguoiDung.id.__eq__(PhieuDatPhong.id).isouter())


    return query.filter(NguoiDung.id.__eq__(user_id)).all()
def dat_phong(cart,hoten,cmnd,diachi,quocgia,ngaynhan,ngaytra,user_id):
    phieudatphong = PhieuDatPhong(nguoidat=user_id,
                              ngaynhan=ngaynhan,
                              ngaytra=ngaytra)
    db.session.add(phieudatphong)
    for c in cart.values():
        d = Phong_PhieuDatPhong(PhieuDatPhong=phieudatphong,
                          Phong_id=c['id'])
    for i in range(1,hoten.__len__):
        e = DSDatPhong(PhieuDatPhong=phieudatphong,
                       hoten=hoten[1],
                       cmnd=cmnd[1],
                       diachi=diachi[1],
                       quocgia=quocgia[1])
        db.session.add_all([d,e])
        db.session.commit()

def Revenue_Stats(**kwargs):
    query = db.session.query(LoaiPhong.id,LoaiPhong.loaiphong,func.sum(ChiTietHoaDon.dongia).label('doanhthu'),func.count(ChiTietHoaDon.id).label("soluotthue")) \
                      .join(Phong,Phong.LoaiPhong_id.__eq__(LoaiPhong.id),isouter=True)\
                       .join(ChiTietHoaDon, ChiTietHoaDon.phong_id.__eq__(Phong.id),isouter=True)\


    return query.group_by(LoaiPhong.loaiphong).all()

def get_PhieuThuePhong():
    descending = PhieuThuePhong.query.order_by(PhieuThuePhong.id.desc())
    return descending.first()
def CapNhat_ThuePhong(PhieuThuePhong,**kwargs):
    if PhieuThuePhong:
        pass
    else:
       PhieuThuePhong
    dsthuephong = DSThuePhong(PhieuThuePhong=PhieuThuePhong,
                              hoten=kwargs.get('hoten'),
                              diachi =kwargs.get('diachi'),
                              cmnd = kwargs.get('cmnd'),
                              quocgia=kwargs.get('quocgia'))
    db.session.add(dsthuephong)
    db.session.commit()
def CapNhat_PhongThue(PhieuThuePhong,**kwargs):
    dsPhong = PhieuThuePhong_Phong(PhieuThuePhong=PhieuThuePhong,
                                   Phong_id=kwargs.get('phongid'))

    db.session.add(dsPhong)
    db.session.commit()
    pass
def Thue_Phong(ngaynhan,ngaytra,nhanvien,**kwargs):
    ngaynhan=ngaynhan
    ngaytra=ngaytra
    phieuthue=PhieuThuePhong(ngaynhan=ngaynhan,ngaytra=ngaytra,nhanvien_id=nhanvien,ngaydat=kwargs.get('ngaydat'),nguoithue_id=kwargs.get('nguoithue'))
    db.session.add(phieuthue)
    db.session.commit()
    return phieuthue

# def Dat_Phong(ngaynhan,ngaytra)
def Usage_Stats(**kwargs):
    thang = kwargs.get('thang')
    tungay= kwargs.get('tungay')
    denngay= kwargs.get('denngay')

    query = db.session.query(Phong.id,Phong.tenphong,PhieuThuePhong.songay)\
                       .join(PhieuThuePhong_Phong,PhieuThuePhong_Phong.Phong_id.__eq__(Phong.id),isouter=True)\
                       .join(PhieuThuePhong,PhieuThuePhong.id.__eq__(PhieuThuePhong_Phong.PhieuThuePhong_id),isouter=True)
    return query.group_by(Phong.id)


# session.query(ObjectRes).filter(ObjectRes.id == session.query(func.max(ObjectRes.id)))
def pay():
    pass
