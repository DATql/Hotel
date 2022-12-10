from app.models import NguoiDung, Phong, LoaiPhong, HoaDonThanhToan, ChiTietHoaDon
from app import db
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


def add_repceipt(cart):
    receipt = HoaDonThanhToan(NhanVien_id=current_user.id)
    db.session.add(receipt)
    for c in cart.values():
        d = ChiTietHoaDon(HoaDonThanhToan=receipt,
                          dongia=d['price'],
                          Phong_id=d['id'])
        db.session.add(d)
        db.session.commit()

def Revenue_Stats(thang):
    query = db.session.query(LoaiPhong.id,LoaiPhong.loaiphong,func.sum(ChiTietHoaDon.dongia))\
                      .join(ChiTietHoaDon,ChiTietHoaDon.phong_id.__eq__(Phong.id))\
                      .join(Phong,Phong.LoaiPhong_id.__eq__(LoaiPhong.id))\
                      .join(HoaDonThanhToan,HoaDonThanhToan.ChiTietHoaDon_id.__eq__(ChiTietHoaDon.id))
    if thang:
        query.filter(HoaDonThanhToan.thang==thang)

    return query.group_by(LoaiPhong.id).all()

def pay():
    pass
