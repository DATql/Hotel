from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_babelex import Babel
import cloudinary
from flask_login import  LoginManager

app = Flask(__name__)
app.secret_key ='djasldkasjd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Goneanhem1@localhost/demohotel2?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app=app)
babel = Babel(app=app)
login = LoginManager(app=app)
cloudinary.config(
            cloud_name= 'dwm0k3plm',
            api_key='724374213342363' ,
            api_secret='mgr32fpAe1xa4oecwLV-v1QdoOk'

)
app.config['CART_KEY'] = 'cart'
def get_locale():
    return 'vi'