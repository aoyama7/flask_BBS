import os


class DevConfig:
    '''开发环境配置'''

    MONGO_URI = 'mongodb://localhost:27017/pyfly'
    # 这里使用环境变量 SECRET_KEY 来设置该字段的值以策安全
    # 在启动应用之前，需要设置环境变量，否则使用第二个参数作为缺省值
    SECRET_KEY = os.environ.get('SECRET_KEY', 'shng_gnhs')
    # 禁用 CSRF 认证
    WTF_CSRF_ENABLED = False
class ProConfig(DevConfig):
    '''生产环境配置'''


class Dev:
    MONGO_URI = 'mongodb://localhost:27017/pyfly'


configs = {
            'Dev': DevConfig,
            'Pro': ProConfig
}
