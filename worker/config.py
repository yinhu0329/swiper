broker_url = 'redis://:123456@127.0.0.1:6379/4'
broker_pool_limit = 10  # Borker 连接池, 默认是10

timezone = 'Asia/Shanghai'
accept_content = ['pickle', 'json']

task_serializer = 'pickle'
result_expires = 3600  # 任务结果过期时间

result_backend = 'redis://:123456@127.0.0.1:6379/4'
result_serializer = 'pickle'
result_cache_max = 10000  # 任务结果最大缓存数量

worker_redirect_stdouts_level = 'INFO'