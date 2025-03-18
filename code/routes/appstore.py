from flask import Blueprint, request, jsonify  # 添加 jsonify 导入
from utils.response import build_response
from config.market import markets
from config.country import countries
from services.appstore_service import AppStoreService  # 新增导入
import logging

logger = logging.getLogger(__name__)

appstore_bp = Blueprint('appstore', __name__, url_prefix='/api/appstore')

# 新增：获取应用市场和地区信息
@appstore_bp.route('/markets', methods=['GET'])
def get_markets():
    """
    获取所有应用市场信息
    """
    try:
        return jsonify(markets)
    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@appstore_bp.route('/countries', methods=['GET'])
def get_countries():
    """
    获取所有国家和地区信息
    """
    try:
        return jsonify(countries)
    except Exception as e:
        return jsonify({"msg": str(e)}), 500
    
    
    
@appstore_bp.route("/search", methods=["GET", "POST", "PUT", "DELETE"])
@appstore_bp.route("/search/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def search():
    try:
        market = request.args.get("market")
        region = request.args.get("region")
        keyword = request.args.get("keyword")
        page = request.args.get("page")
        pagesize = request.args.get("pagesize")
        sp = request.args.get("sp",default="diandian")

        
        # 参数校验
        if not all([market, region, keyword]):
            return build_response("MISSING_PARAMETERS"), 400
            
        if market not in markets:
            return build_response("INVALID_MARKET"), 400
            
        if region not in countries:
            return build_response("INVALID_REGION"), 400
        
        # 执行搜索逻辑,调用 AppStore Service 接口
           # 调用 AppStoreService 执行搜索逻辑
        service = AppStoreService()
        result = service.search(market, region, keyword, page, pagesize, sp)

        return build_response("SUCCESS", result)
        
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        return build_response("SERVER_ERROR"), 500

@appstore_bp.route("/detail", methods=["GET", "POST", "PUT", "DELETE"])
def detail():
    try:
        market = request.args.get("market")
        region = request.args.get("region")
        appid = request.args.get("appid")
        st = request.args.get("st")
        if st is None or st == "":
            st = market 
        
        if region is None or region == "":
            region = "CHN"
            
        # 参数校验
        if not all([market, region, appid]):
            return build_response("MISSING_PARAMETERS"), 400
            
        if market not in markets:
            return build_response("INVALID_MARKET"), 400
            
        if region not in countries:
            return build_response("INVALID_REGION"), 400

         # 调用 AppStoreService 获取应用详情
        service = AppStoreService()
        result = service.detail(market, region, appid, st)
        return build_response("SUCCESS", result)

    except Exception as e:
        logger.error(f"Detail error: {str(e)}")
        return build_response("SERVER_ERROR"), 500
