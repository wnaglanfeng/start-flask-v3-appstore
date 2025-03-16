from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
from routes.appstore import appstore_bp
from routes.security import security_bp
from config import config
import logging

app = Flask(__name__)
app.config.from_object(config['development'])

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# IP 验证
@app.before_request
def before_request():
    try:
        # 获取客户端 IP 地址，支持代理
        client_ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
        
        # 验证 IP 是否在白名单中
        if client_ip not in app.config['ALLOWED_IPS']:
            print(f"Access denied for IP: {client_ip}")
            logger.warning(f"Access denied for IP: {client_ip}")
            return jsonify({"msg": "Access denied"}), 403
        
        logger.debug(f"Access granted for IP: {client_ip}")
    except Exception as e:
        logger.error(f"IP validation error: {str(e)}")
        return jsonify({"msg": "Internal server error"}), 500
    
@app.route('/data/<path:filename>')
def deny_access(filename):
    return jsonify({"msg": "Access denied"}), 403

# Swagger UI 配置
SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config=app.config['SWAGGER_CONFIG']
)

# 注册蓝图
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
app.register_blueprint(appstore_bp)
app.register_blueprint(security_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)



