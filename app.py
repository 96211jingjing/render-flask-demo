"""
活动安排系统 - API 后端 + Web 前端
本地运行: py -3 app.py
生产部署: gunicorn app:app
"""
import os
from flask import Flask
from flask_cors import CORS

from config import SECRET_KEY
from models import init_db, close_db

app = Flask(__name__)
app.secret_key = SECRET_KEY
CORS(app, supports_credentials=True)

# 注册蓝图
from api import api_bp
from web import web_bp

app.register_blueprint(api_bp)
app.register_blueprint(web_bp)

# 数据库生命周期
app.teardown_appcontext(close_db)

# Render 上首次请求时自动初始化数据库
with app.app_context():
    init_db()

if __name__ == "__main__":
    print("=" * 50)
    print("  活动安排系统 V7")
    print("  Web 管理端: http://127.0.0.1:5000")
    print("  API 接口:   http://127.0.0.1:5000/api/")
    print("=" * 50)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
