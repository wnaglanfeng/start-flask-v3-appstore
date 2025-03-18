from .diandian import DiandianScraper
from .qimai import QimaiScraper
from .market import MarketScraper
from .huawei import HuaweiScraper

# 定义标准化的应用信息结构
APP_INFO = {
    "app_name": "",  # 应用名称
    "app_id": "",  # 应用所在市场ID
    "icon_url": "",  # 应用图标URL
    "tags": [],  # 应用标签/分类
    "developer": "",  # 开发者名称
    "download_count": 0,  # 下载次数
    "icp_number": "",  # ICP备案号
    "introduction": "",  # 应用介绍
    "bounde_id": "",  # 应用包类型
    "rating": 0.0,  # 应用评分
    "rating_count": 0,  # 评分总数
    "screenshots": [],  # 应用截图
    "store": "",  # 应用商店标识
    "update_time": "",  # 更新时间
    "version": "",  # 应用版本
    "download_url": ""  # 下载链接
}

