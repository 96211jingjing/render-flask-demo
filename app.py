"""
活动安排系统
本地运行: py -3 app.py
部署运行: gunicorn app:app --bind 0.0.0.0:$PORT
"""
import os
import sys
import traceback

from flask import Flask
from flask_cors import CORS

from config import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY
CORS(app, supports_credentials=True)

# --- 初始化数据库（带错误捕获）---
try:
    from models import init_db, close_db
    with app.app_context():
        init_db()
    app.teardown_appcontext(close_db)
    print("[OK] 数据库初始化成功", flush=True)
except Exception as e:
    print(f"[ERROR] 数据库初始化失败: {e}", flush=True)
    traceback.print_exc()

# --- 注册蓝图 ---
try:
    from api import api_bp
    from web import web_bp
    app.register_blueprint(api_bp)
    app.register_blueprint(web_bp)
    print("[OK] 蓝图注册成功", flush=True)
except Exception as e:
    print(f"[ERROR] 蓝图注册失败: {e}", flush=True)
    traceback.print_exc()

# --- 健康检查路由（Railway 需要）---
@app.route('/')
def health():
    return 'OK', 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"[启动] 端口: {port}", flush=True)
    app.run(host="0.0.0.0", port=port, debug=False)
