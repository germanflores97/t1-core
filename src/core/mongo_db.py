from pymongo import MongoClient

from src.core.settings import configs

__CLIENT = MongoClient(
    configs().mongo_url, maxPoolSize=configs().mongo_pool_max_size, 
    minPoolSize=configs().mongo_pool_min_size, maxIdleTimeMS=configs().mongo_idle_time_ms
)

def get_db():
    return __CLIENT[configs().mongo_db_name]