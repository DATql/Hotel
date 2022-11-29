from flask import render_template
from app import app

@app.route("/")
def home():
    return render_template('index.html', des = "Mường Thanh - Chuỗi khách sạn tư nhân lớn nhất Đông Dương", title = "Trang Chủ")


if __name__=='__main__':
    app.run(debug=True)