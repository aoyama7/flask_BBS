import json
from bson import ObjectId
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from ..extensions import mongo
from ..models import User
from .. import utils
from random import randint
from werkzeug.security import generate_password_hash
from .. form import RegisterForm, LoginForm
from flask_login import login_user, logout_user

# 创建蓝图，第一个参数为自定义，供前端使用，第二个参数为固定写法
# 第三个参数为URL前缀
user_view = Blueprint('user', __name__, url_prefix='/user', template_folder="templates", static_folder="static")


class MyEncoder(json.JSONEncoder):
    '''
    该类作为 json.dumps 方法的 cls 参数的值
    以处理特殊的、不能被序列化的值
    '''

    def default(self, o):
        '''参数 o 为被序列化的值'''
        # 如果 o 是 _id 字段或者 datetime 类型的数据，将其转化为字符串
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return o.isoformat()
        # 否则调用父类的同名方法触发 TypeError 异常
        super().default(o)


@user_view.route('/')
def home():
    # mongo.db 就是 PyFly 数据库，find 方法的返回值就是迭代器
    # 这里使用list方法将他转换为列表
    users = list(mongo.db.users.find())
    # cls参数用于处理特殊类型的数据
    # ensure_ascii=False 使得 JSON 字符串 UTF-8 编码
    return json.dumps(users, cls=MyEncoder, ensure_ascii=False)


@user_view.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # 当用户提交之后，执行 if 语句块中的内容
    if form.is_submitted():
        # 如果没有通过表单类中割割字段的验证，返回错误信息
        if not form.validate():
            return jsonify({'status': 50001, 'msg': str(form.errors)})
        vercode = form.vercode.data     # 获取答案
        try:
            utils.verify_num(vercode)   # 验证答案
        except Exception as e:
            return '<h1>{}</h1>'.format(e), 404
        # 从数据库中查询对应的用户数据
        user = mongo.db.users.find_one({'email': form.email.data})
        # 进行对应字段的验证
        if not user:
            return jsonify({'status': 50102, 'msg': '用户不存在!'})
        if not User.validate_login(user['password'], form.password.data):
            return jsonify({'status': 50000, 'msg': '密码错误!'})
        if not user.get('is_active'):
            return jsonify({'status': 443, 'msg': '账号未激活'})
        # 通过验证后，把用户名加入session
        # 验证通过后，使用login_user 方法替换 session 实现登陆状态
        #session['username'] = user['username']
        login_user(User(user))
        # redirect 用于重定向到网站首页
        # url_for 用于构造 URL ，参数为字符串，蓝图，视图函数
        return redirect(url_for('index.index'))
        return '<h1>登陆成功</h1>'
    ver_code = utils.gen_verify_num()
    return render_template('user/login.html', ver_code=ver_code['question'], form=form)


@user_view.route('/register')
def register():
    form = RegisterForm()
    if form.is_submitted():
        if not form.validate():
            return jsonify({'status': 50001, 'smy': str()})
        try:
            utils.verify_num(form.vercode.data)
        except Exception as e:
            return '<h1>{}</h1>'.format(e), 404
        # 这步用来验证邮箱是否已经被注册
        user = mongo.db.users.find_one({'email': form.email.data})
        if user:
            return jsonify({'status': '该邮箱已经注册'})
        # 创建注册用户的基本信息
        user = {'is_active': False,
                'coin': 0,
                'email': form.email.data,
                'username': form.username.data,
                'vip': 0,
                'reply_count': 0,
                'avatar': url_for('static', filename='images/avatar/{}.jpg'.format(randint(0, 12))),
                'password': generate_password_hash(form.password.data),
                'created_at': datetime.utcnow()
                }
        mongo.db.users.insert_one(user)
        return redirect(url_for('.login'))
    ver_code = utils.gen_verify_num()
    return render_template('user/register.html', ver_code=ver_code['question'], form=form)


# 定义登出函数
@user_view.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('index.index'))
