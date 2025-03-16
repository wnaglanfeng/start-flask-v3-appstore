import logging
from flask import jsonify

logger = logging.getLogger(__name__)

ERROR_CODES = {
    "MISSING_PARAMETERS": {"code": 40001, "msg": "缺少必要参数"},
    "INVALID_MARKET": {"code": 40002, "msg": "无效的应用市场"},
    "INVALID_REGION": {"code": 40003, "msg": "无效的地区"},
    "SUCCESS": {"code": 20000, "msg": "成功"},
    "NOT_FOUND": {"code": 40400, "msg": "未找到资源"},
    "SERVER_ERROR": {"code": 50000, "msg": "服务器内部错误"}
}

def build_response(status, data=None):
    return jsonify({
        "msg": ERROR_CODES[status]["msg"],
        "code": ERROR_CODES[status]["code"],
        "data": data if data is not None else {}
    })
