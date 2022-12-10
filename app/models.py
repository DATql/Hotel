from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, Text, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from app import db, app
from enum import Enum as CountryEnum
from enum import Enum as Role
from flask_login import UserMixin
from datetime import datetime


class QuocGia(CountryEnum):
    TrongNuoc = 1
    NuocNgoai = 2


class LoginRole(Role):
    Admin = 1
    Staff = 2
    User = 3


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class NguoiDung(BaseModel, UserMixin):
    hoten = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    quocgia = Column(Enum(QuocGia), default=QuocGia.TrongNuoc)
    cmnd = Column(String(10))
    diachi = Column(String(100))
    role = Column(Enum(LoginRole, default=LoginRole.User))
    avatar = Column(String(100))

    def __str__(self):
        return self.hoten


class LoaiPhong(BaseModel):
    loaiphong = Column(String(30), unique=True)
    mota = Column(String(100), nullable=False)
    soluong = Column(Integer, nullable=False)
    hinhanh = Column(String(100))
    dongia = Column(Float, nullable=False)
    sokhachtoida = Column(Integer, default=3, nullable=False)
    tilephuthu = Column(Float, default=3 / 10, nullable=False)
    heso = Column(Float, default=1.5, nullable=False)
    Phong = relationship('Phong', backref='LoaiPhong', lazy=True)


class Phong(BaseModel):
    tenphong = Column(String(10), nullable=False)
    tinhtrang = Column(Boolean)
    hinhanh = Column(String(100))
    LoaiPhong_id = Column(Integer, ForeignKey(LoaiPhong.id), nullable=False)
    ChiTietHoaDon = relationship('ChiTietHoaDon', backref='Phong', lazy=True)
    PhieuDatPhong = relationship('PhieuDatPhong', secondary='Phong_PhieuDatPhong', lazy='subquery',
                                 backref=backref('Phong', lazy=True))
    PhieuThuePhong = relationship('PhieuThuePhong', secondary='Phong_PhieuThuePhong', lazy='subquery',
                                  backref=backref('Phong', lazy=True))

    def __str__(self):
        return self.tenphong


class DanhSachKhachHang(BaseModel):
    __abstract__ = True
    hoten = Column(String(50), nullable=False)
    quocgia = Column(Enum(QuocGia), default=QuocGia.TrongNuoc)
    cmnd = Column(String(10))
    diachi = Column(String(100))


Phong_PhieuDatPhong = db.Table('Phong_PhieuDatPhong',
                               Column('Phong_id', Integer, ForeignKey('phong.id'), primary_key=True),
                               Column('PhieuDatPhong_id', Integer, ForeignKey('phieu_dat_phong.id'), primary_key=True))

Phong_PhieuThuePhong = db.Table('Phong_PhieuThuePhong',
                                Column('Phong_id', Integer, ForeignKey('phong.id'), primary_key=True),
                                Column('PhieuThuePhong_id', Integer, ForeignKey('phieu_thue_phong.id'),
                                       primary_key=True))
9

class PhieuDatPhong(BaseModel):
    ngaydat = Column(DateTime)
    ngaynhan = Column(DateTime)
    ngaytra = Column(DateTime)
    nguoidat = Column(Integer, ForeignKey(NguoiDung.id), nullable=False)
    DSDatPhong = relationship('DSDatPhong', backref='PhieuDatPhong', lazy=True)


class DSDatPhong(DanhSachKhachHang):
    PhieuDatPhong_id = Column(Integer, ForeignKey(PhieuDatPhong.id), nullable=False)


class PhieuThuePhong(BaseModel):
    ngaydat = Column(DateTime)
    ngaynhan = Column(DateTime)
    ngaytra = Column(DateTime)
    nguoithue_id = Column(Integer, ForeignKey(NguoiDung.id), nullable=False)
    nhanvien_id = Column(Integer, ForeignKey(NguoiDung.id), nullable=False)
    DSThuePhong = relationship('DSThuePhong', backref='PhieuThuePhong', lazy=True)


class DSThuePhong(DanhSachKhachHang):
    PhieuThuePhong_id = Column(Integer, ForeignKey(PhieuThuePhong.id), nullable=False)


class HoaDonThanhToan(BaseModel):
    ngaylap = Column(DateTime, default=datetime.now())
    tongtien = Column(Float)
    ngaynhan = Column(DateTime)
    ngaytra = Column(DateTime)
    thang = Column(Integer)
    ChiTietHoaDon_id = relationship('ChiTietHoaDon', backref='HoaDonThanhToan', lazy=True)


class ChiTietHoaDon(BaseModel):
    dongia = Column(Float, nullable=False)
    phong_id = Column(Integer, ForeignKey(Phong.id))
    HoaDonThanhToan_id = Column(Integer, ForeignKey(HoaDonThanhToan.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        r2 = LoaiPhong(loaiphong='Phòng đôi', soluong=10, mota='a', hinhanh='a', dongia=100000, sokhachtoida=3,
                       tilephuthu=3 / 10, heso=1.5)
        r3 = LoaiPhong(loaiphong='Phòng lớn', soluong=10, mota='a', hinhanh='a', dongia=100000, sokhachtoida=3,
                       tilephuthu=3 / 10, heso=1.5)
        r1 = LoaiPhong(loaiphong='Phòng đơn', soluong=10, mota='a', hinhanh='a', dongia=100000, sokhachtoida=3,
                       tilephuthu=3 / 10, heso=1.5)

        import hashlib

        password = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        a1 = NguoiDung(hoten='admin', username='admin', password=password, role='Admin', cmnd='123', diachi='123',
                       quocgia='TrongNuoc', avatar='a')
        a2 = NguoiDung(hoten='dat1', username='dat1', password=password, role='User', cmnd='123', diachi='123',
                       quocgia='TrongNuoc', avatar='a')


        p1 = Phong (tenphong ='P01',tinhtrang=1,hinhanh='a',LoaiPhong_id=1)
        p2 = Phong (tenphong ='P02',tinhtrang=1,hinhanh='a',LoaiPhong_id=1)
        p3 = Phong (tenphong ='P03',tinhtrang=1,hinhanh='a',LoaiPhong_id=1)
        p4 = Phong (tenphong ='P04',tinhtrang=1,hinhanh='a',LoaiPhong_id=2)
        p5 = Phong (tenphong ='P05',tinhtrang=1,hinhanh='a',LoaiPhong_id=2)
        p6 = Phong (tenphong ='P06',tinhtrang=1,hinhanh='a',LoaiPhong_id=2)
        p7 = Phong (tenphong ='P07',tinhtrang=1,hinhanh='a',LoaiPhong_id=3)
        p8 = Phong (tenphong ='P08',tinhtrang=1,hinhanh='a',LoaiPhong_id=3)
        p9 = Phong (tenphong ='P09',tinhtrang=1,hinhanh='a',LoaiPhong_id=3)

        db.session.add_all([r1,r2,r3,a1,a2,p1,p2,p3,p4,p5,p6,p7,p8,p8])
        db.session.commit()