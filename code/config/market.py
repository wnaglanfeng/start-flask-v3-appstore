# 应用市场映射字典
# 应用商店的地区可用性：
# global: 全球可用
# multi_region: 多个地区可用
# single_region: 仅单一地区可用

markets = {
    "ios": {
        "name": "苹果应用市场",
        "market_code": "ios",
        "type": "ios",
        "dd_market_id": 1,
        "dd_market_type":0,
        "global_availability": "global"  # 全球可用
    },
    "huawei": {
        "name": "华为应用市场",
        "market_code": "huawei",
        "type": "android",
        "dd_market_id": 2,
        "dd_market_type":-1,
        "global_availability": "single_region",  # 单地区
        "available_regions": ["CHN"]  # 示例地区
    },
    "xiaomi": {
        "name": "小米应用商店",
        "market_code": "xiaomi",
        "type": "android",
        "dd_market_id": 3,
        "dd_market_type":-1,
        "global_availability": "single_region",  # 单地区
        "available_regions": ["CHN"]  # 示例地区
    },
    "vivo": {
        "name": "vivo应用商店",
        "market_code": "vivo",
        "type": "android",
        "dd_market_id": 4,
        "dd_market_type":-1,
        "global_availability": "single_region",  # 单地区
        "available_regions": ["CHN"]  # 示例地区
    },
    "oppo": {
        "name": "OPPO软件商店",
        "market_code": "oppo",
        "type": "android",
        "dd_market_id": 5,
        "dd_market_type":-1,
        "global_availability": "single_region",  # 单地区
        "available_regions": ["CHN"]  # 示例地区
    },
    "meizu": {
        "name": "魅族应用中心",
        "market_code": "meizu",
        "type": "android",
        "dd_market_id": 6,
        "dd_market_type":-1,
        "global_availability": "single_region",  # 单地区
        "available_regions": ["CHN"]  # 示例地区
    },
    "yingyongbao": {
        "name": "应用宝",
        "market_code": "yingyongbao",
        "type": "android",
        "dd_market_id": 7,
        "dd_market_type":-1,
        "global_availability": "single_region",  # 单地区
        "available_regions": ["CHN"]  # 示例地区
    },
    "baidu": {
        "name": "百度手机助手",
        "market_code": "baidu",
        "type": "android",
        "dd_market_id": 8,
        "dd_market_type":-1,
        "global_availability": "single_region",  # 单地区
        "available_regions": ["CHN"]  # 示例地区
    },
    "qihoo": {
        "name": "360手机助手",
        "market_code": "qihoo",
        "type": "android",
        "dd_market_id": 9,
        "dd_market_type":-1,
        "global_availability": "single_region",  # 单地区
        "available_regions": ["CHN"]  # 示例地区
    },
    "wandoujia": {
        "name": "豌豆荚",
        "market_code": "wandoujia",
        "type": "android",
        "dd_market_id": 10,
        "dd_market_type":-1,
        "global_availability": "single_region",  # 单地区
        "available_regions": ["CHN"]  # 示例地区
    },
    "googleplay": {
        "name": "Google Play",
        "market_code": "googleplay",
        "type": "android",
        "dd_market_id": 11,
        "dd_market_type":-1,
        "dd_market_type":-1,
        "global_availability": "global"  # 全球可用
    },
    "taptap": {
        "name": "TapTap",
        "market_code": "taptap",
        "type": "android|ios",
        "dd_market_id": 12,
        "dd_market_type":-1,
        "global_availability": "global"  # 全球可用
    },
}
