from flask import Flask

from .configs import configs
from .controllers import config_blueprints
# 导入 init 函数 作为 install_init
from fly_bbs.install_init import init as install_init
from fly_bbs.extensions import init_extensions
from .custom_functions import init_func


def create_app(config_name):
    app = Flask(__name__)
    # from_object 会从传入的对象中读取配置信息
    app.config.from_object(configs[config_name])
    # 初始化扩展，连接数据库
    init_extensions(app)
    # 将已经创建的视图函数注册到应用上
    config_blueprints(app)
    # 像数据库中添加数据
    install_init()
    init_func(app)
    return app

