from flask import Flask, request, jsonify
import arrow
from flask_swagger_ui import get_swaggerui_blueprint
import logging
from config.market import markets
from config.country import countries

app = Flask(__name__)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 错误字典
ERROR_CODES = {
    "MISSING_PARAMETERS": {"code": 40001, "msg": "缺少必要参数"},
    "INVALID_MARKET": {"code": 40002, "msg": "无效的应用市场"},
    "INVALID_REGION": {"code": 40003, "msg": "无效的地区"},
    "SUCCESS": {"code": 20000, "msg": "成功"},
    "NOT_FOUND": {"code": 40400, "msg": "未找到资源"},
    "SERVER_ERROR": {"code": 50000, "msg": "服务器内部错误"}
}

# Swagger UI 配置
SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "App Store API"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

def build_response(status, data=None):
    return {
        "msg": ERROR_CODES[status]["msg"],
        "code": ERROR_CODES[status]["code"],
        "data": data if data is not None else {}
    }

@app.route("/search", methods=["GET", "POST", "PUT", "DELETE"])
@app.route("/search/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def search(path):
    try:
        market = request.args.get("market")
        region = request.args.get("region")
        keyword = request.args.get("keyword")
        page = request.args.get("page")
        pagesize = request.args.get("pagesize")
        
        # 参数校验
        if not all([market, region, keyword]):
            return jsonify(build_response("MISSING_PARAMETERS")), 400
            
        if market not in markets:
            return jsonify(build_response("INVALID_MARKET")), 400
            
        if region not in countries:
            return jsonify(build_response("INVALID_REGION")), 400

        return jsonify(build_response("SUCCESS", {
            "market": market,
            "region": region,
            "keyword": keyword,
            "page": page,
            "pagesize": pagesize
        }))
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        return jsonify(build_response("SERVER_ERROR")), 500

@app.route("/detail", methods=["GET", "POST", "PUT", "DELETE"])
@app.route("/detail/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def detail(path):
    try:
        market = request.args.get("market")
        region = request.args.get("region")
        appid = request.args.get("appid")
        
        # 参数校验
        if not all([market, region, appid]):
            return jsonify(build_response("MISSING_PARAMETERS")), 400
            
        if market not in markets:
            return jsonify(build_response("INVALID_MARKET")), 400
            
        if region not in countries:
            return jsonify(build_response("INVALID_REGION")), 400

        return jsonify(build_response("SUCCESS", {
            "market": market,
            "region": region,
            "appid": appid
        }))
    except Exception as e:
        logger.error(f"Detail error: {str(e)}")
        return jsonify(build_response("SERVER_ERROR")), 500

@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE"])
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def hello_world(path):
    try:
        return jsonify(build_response("SUCCESS", {
            "query": str(request.query_string, "utf-8"),
            "path": path,
            "data": str(request.stream.read(), "utf-8"),
            "clientIp": request.headers.get("x-forwarded-for"),
        }))
    except Exception as e:
        logger.error(f"Root error: {str(e)}")
        return jsonify(build_response("SERVER_ERROR")), 500

@app.errorhandler(404)
def not_found(error):
    logger.error(f"Not found: {str(error)}")
    return jsonify(build_response("NOT_FOUND")), 404

@app.errorhandler(500)
def server_error(error):
    logger.error(f"Server error: {str(error)}")
    return jsonify(build_response("SERVER_ERROR")), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)



