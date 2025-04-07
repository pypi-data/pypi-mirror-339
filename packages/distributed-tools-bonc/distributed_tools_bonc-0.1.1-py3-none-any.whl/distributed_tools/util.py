# -*- coding:utf-8 -*-
import threading

from distributed_tools.redis_util import RedisClientUtil


class Snowflake:
    def __init__(self, data_center_id, sequence):
        ### 机器标识ID
        ### 数据中心ID
        self.data_center_id = data_center_id
        ### 计数序列号
        self.sequence = sequence
        ### 时间戳
        self.last_timestamp = -1
        ### 锁
        self.lock = threading.Lock()

    def next_id(self, worker_id, timestamp):
        with self.lock:
            if timestamp < self.last_timestamp:
                raise Exception("Clock moved backwards. Refusing to generate id for %d milliseconds" % abs(
                    timestamp - self.last_timestamp))
            else:
                self.sequence = 0
            self.last_timestamp = timestamp
            self.sequence = self.sequence + 1
            return ((timestamp - 1288834974657) << 22) | (self.data_center_id << 17) | (
                    worker_id << 12) | self.sequence


# 按雪花算法生成随机数
def gen_snowflake(snowflake: Snowflake, redis_client_util: RedisClientUtil, worker_id: int):
    return snowflake.next_id(worker_id, redis_client_util.get_redis_time_mill_second())
