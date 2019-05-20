from flask import Flask
from App.views import blue
from App.exts import init_exts


def create_app():
    app = Flask(__name__)
    app.config['ENV'] = 'development'  # 配置成开发环境

    # 数据库配置
    # sqlite
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:rock1204@localhost:3306/myblock"

    # 禁止对象追踪修改
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = "abc"
    # 加载Flask插件
    init_exts(app)

    # 注册蓝图
    app.register_blueprint(blue)

    return app

