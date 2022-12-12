from flask import render_template, request, redirect, session, jsonify, url_for
from app import app, dao, utils
from flask_login import login_user, logout_user, login_required
from datetime import datetime
import cloudinary.uploader
from app.admin import *
from app import login

@app.context_processor
def common_response():
    return  {
        'cart_stats': utils.cart_stats(session.get('cart')),
    }
@app.route("/")
def home():
    return render_template('index.html', des="Mường Thanh - Chuỗi khách sạn tư nhân lớn nhất Đông Dương",
                           title="Trang Chủ")


@app.route("/login", methods=['get', 'post'])
def login_my_user():
    err_msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user)

            return redirect(url_for('home'))
        else:
            err_msg = " Khong chinh xac"
    return render_template('login.html', err_msg=err_msg)


@app.route("/register", methods=['post', 'get'])
def register():
    err_msg = ''
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form['password']
        confirm = request.form['confirm']
        cmnd = request.form.get('password')
        diachi = request.form.get('diachi')
        quocgia = request.form.get('quocgia')
        avatar_path = None
        try:
            if password.__eq__(confirm):
                avatar = request.files.get('avatar')
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']
                dao.register(name=name, username=username, password=password, cmnd=cmnd, diachi=diachi,
                             avatar=avatar_path, quocgia=quocgia)

                return redirect(url_for('home'))

            else:
                err_msg = 'Mật khẩu KHÔNG khớp!'

        except Exception as ex:
            err_msg = 'Có lỗi xảy ra! Vui lòng quay lại sau!' + str(ex)

    return render_template('register.html', err_msg=err_msg)


@app.route('/booking', methods=['get'])
def room():
    kw = request.args.get('loaiphong')
    ngaynhan =request.args.get('ngaynhan')
    ngaytra = request.args.get('ngaytra')
    roomcategories = dao.load_roomcategories(loaiphong=kw)
    rooms = dao.load_room()
    return render_template('booking.html', roomcategories=roomcategories,rooms=rooms,ngaynhan=ngaynhan,ngaytra=ngaytra)


@app.route('/order', methods=['get', 'post'])
def order():
    if request.method == 'POST':
        phong = request.form.get('tenphong')

    # render_template('order.html',room = phong)


@login.user_loader
def user_loader(user_id):
    return dao.get_user_by_id(user_id=user_id)


@app.route('/admin-login', methods=['post'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)
    return redirect('/admin')
@app.route('/user-logout')
def user_logout():
    logout_user()
    return redirect(url_for('login_my_user'))

@app.route('/cart')
def cart():

    return render_template('confirmation.html',stats = utils.cart_stats(session['cart']),roomcategories=dao.load_fullroomcategories())

@app.route('/cart',methods=['post'])
def add_to_cart():
    data = request.json
    id = str(data['id'])

    key = app.config['CART_KEY']


    cart = session[key] if key in session else {}

    if id in cart:
        cart[id]['quantity'] = 1
    else:
        name = data['name']
        price = data['price']
        sokhachtoida = data['sokhachtoida']
        loaiphong = data['loaiphong']
        cart[id] = {
            "id": id,
            "name": name,
            "price": price,
            "quantity": 1,
            "sokhachtoida": sokhachtoida,
            "loaiphong": loaiphong,
        }

    session[key] = cart

    return jsonify(utils.cart_stats(cart))

@app.route('/complete',methods=['post'])
def pay():
        request.form.getlist('hoten[]'),
        request.form.getlist('diachi[]'),
        request.form.getlist('cmnd[]'),
        request.form.getlist('quocgia[]')
        dao.dat_phong(session['cart'])
        return render_template('complete.html',dsdp=dao.get_phieu_dat_phong(current_user.id),dskh=dao.get_danh_sach_dat_phong(current_user.id))
if __name__ == '__main__':
    app.run(debug=True)
