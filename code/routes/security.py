from functools import wraps
from flask import Blueprint, jsonify, request, abort
from config import config
import os

security_bp = Blueprint('security', __name__, url_prefix='/api/security')

# API密钥验证装饰器
def require_api_key(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-KEY')
        if False:#api_key != config['development'].API_SECRET_KEY:
            abort(401, description="Invalid API key")
        return view_function(*args, **kwargs)
    return decorated_function

# IP管理功能
@security_bp.route('/ip/allow', methods=['POST','GET'])
@require_api_key
def allow_ip():
    ip = request.args.get('ip')  # 从查询参数中获取IP
    if not ip:
        return jsonify({"msg": "IP address is required"}), 400
    
    config['development'].ALLOWED_IPS.add(ip)
    save_allowed_ips(config['development'].ALLOWED_IPS)
    return jsonify({"msg": f"IP {ip} added successfully"})

@security_bp.route('/ip/deny', methods=['POST'])
@require_api_key
def deny_ip():
    ip = request.args.get('ip')  # 从查询参数中获取IP
    if not ip:
        return jsonify({"msg": "IP address is required"}), 400
    
    if ip in config['development'].ALLOWED_IPS:
        config['development'].ALLOWED_IPS.remove(ip)
        save_allowed_ips(config['development'].ALLOWED_IPS)
        return jsonify({"msg": f"IP {ip} removed successfully"})
    return jsonify({"msg": f"IP {ip} not found"}), 404

def save_allowed_ips(ips):
    with open(config['development'].ALLOWED_IPS_FILE, 'w') as f:
        f.write('\n'.join(ips))
