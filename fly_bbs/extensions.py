from flask_pymongo import PyMongo
from flask_login import LoginManager
from bson import ObjectId

from .models import User

# 实例化一个PyMongo类
mongo = PyMongo()
# 创建LoginManager类的实例
login_manager = LoginManager()
login_manager.login_view = 'user_view.login'

# 使用该装饰器的作用是将 user_load 方法
# 设置为 login_manager 的 user_callback 属性
# 以便能够在需要的时候使用 user_id 参数找到对应的用户数据


@login_manager.user_loader
def user_load(user_id):
    # 如果 user_id 存在，find_one 方法返回字典对象
    # 否则返回 None
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    return User(user)


def init_extensions(app):
    # 调用 PyMongo 类的 init_app 方法进行初始化
    mongo.init_app(app)
    # 调用 init_app 方法注册 app
    # 此方法的主要作用就是将 login_manager 本身赋值给 app.login_manager 属性
    # 以便 app 能够使用其登录登出等功能
    login_manager.init_app(app)
