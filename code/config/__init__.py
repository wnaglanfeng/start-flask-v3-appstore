import os
from pathlib import Path

# 基础配置
class Config:
    # Flask 配置
    ALLOWED_IPS = set()  # IP 白名单
    API_SECRET_KEY = 'your-secure-api-key'  # 替换为实际的API密钥
    ALLOWED_IPS_FILE = 'data/allowed_ips.txt'
    DEBUG = False
    TESTING = False
    
    # 日志配置
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_DIR = Path('logs')
    LOG_FILE = LOG_DIR / 'app.log'
    
    # 缓存配置
    CACHE_TYPE = 'SimpleCache'  # 可以使用 RedisCache 等
    CACHE_DEFAULT_TIMEOUT = 300  # 默认缓存时间 5 分钟
    
    # 数据库配置（如果需要）
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # SWAGGER UI 配置
    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.json'
    SWAGGER_CONFIG = {
        'app_name': "App Store API",
        'layout': "StandaloneLayout",
        'deepLinking': True,
        'supportedSubmitMethods': ['get', 'post', 'put', 'delete', 'patch'],
        'docExpansion': 'list',
        'defaultModelExpandDepth': 1,
        'defaultModelsExpandDepth': -1,
        'validatorUrl': None,
        'operationsSorter': 'method',
        'tagsSorter': 'alpha',
        'showExtensions': True,
        'showCommonExtensions': True,
        'custom_css_url': '/static/showdoc-style.css',
        'persistAuthorization': True,  # 保持授权信息
        'displayRequestDuration': True,  # 显示请求耗时
        'filter': True,  # 启用搜索过滤
        'tryItOutEnabled': True  # 启用"Try it out"功能
    }
    
    

# 开发环境配置
class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = 'DEBUG',
    ALLOWED_IPS = {'127.0.0.1', '192.168.1.1'}  # 添加默认允许的IP地址

# 测试环境配置
class TestingConfig(Config):
    TESTING = True
    LOG_LEVEL = 'DEBUG'

# 生产环境配置
class ProductionConfig(Config):
    LOG_LEVEL = 'WARNING'

# 配置映射
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
