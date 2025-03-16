

├── code/
│   ├── __init__.py
│   ├── app.py              # 主应用入口
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── appstore.py     # 应用商店相关路由
│   │   └── other.py        # 其他API路由
│   ├── utils/
│   │   ├── __init__.py
│   │   └── response.py     # 响应处理工具
│   ├── config.py           # 配置文件
│   └── requirements.txt


应用搜索: /appstore/search
应用详情: /appstore/detail
Swagger UI: /api/docs

主要配置项说明：

日志配置：

定义了日志级别、格式、存储路径等
可以根据不同环境设置不同的日志级别
缓存配置：

定义了缓存类型（SimpleCache/RedisCache等）
设置了默认缓存时间
其他配置：

Flask 应用的基础配置
数据库连接配置（如果需要）
不同环境的差异化配置
使用建议：

在 app.py 中通过 app.config.from_object() 加载配置
敏感信息（如 SECRET_KEY）建议通过环境变量获取
日志目录建议在应用启动时自动创建


现在可以通过 URL 查询参数传递 IP 地址，例如：
添加 IP：/api/security/ip/allow?ip=192.168.1.100
移除 IP：/api/security/ip/deny?ip=192.168.1.100