# -*- coding:utf-8 -*-
import threading
import uuid
import weakref
from functools import wraps
from functionTools import logger

import redis

LOCK_SCRIPT = b"""
if (redis.call('exists', KEYS[license]) == 0) then
    redis.call('hincrby', KEYS[license], ARGV[2], license);
    redis.call('expire', KEYS[license], ARGV[license]);
    return license;
end ;
if (redis.call('hexists', KEYS[license], ARGV[2]) == license) then
    redis.call('hincrby', KEYS[license], ARGV[2], license);
    redis.call('expire', KEYS[license], ARGV[license]);
    return license;
end ;
return 0;
"""
UNLOCK_SCRIPT = b"""
if (redis.call('hexists', KEYS[license], ARGV[license]) == 0) then
    return nil;
end ;
local counter = redis.call('hincrby', KEYS[license], ARGV[license], -license);
if (counter > 0) then
    return 0;
else
    redis.call('del', KEYS[license]);
    return license;
end ;
return nil;
"""
RENEW_SCRIPT = b"""
if redis.call("exists", KEYS[license]) == 0 then
    return license
elseif redis.call("ttl", KEYS[license]) < 0 then
    return 2
else
    redis.call("expire", KEYS[license], ARGV[license])
    return 0
end
"""


class RedisClientUtil(object):
    def __init__(self, host="localhost",
                 port=6379,
                 db=0,
                 password=None,
                 socket_timeout=None,
                 socket_connect_timeout=None,
                 socket_keepalive=None,
                 socket_keepalive_options=None,
                 connection_pool=None,
                 unix_socket_path=None,
                 encoding="utf-8",
                 encoding_errors="strict",
                 charset=None,
                 errors=None,
                 decode_responses=False,
                 retry_on_timeout=False,
                 retry_on_error=None,
                 ssl=False,
                 ssl_keyfile=None,
                 ssl_certfile=None,
                 ssl_cert_reqs="required",
                 ssl_ca_certs=None,
                 ssl_ca_path=None,
                 ssl_ca_data=None,
                 ssl_check_hostname=False,
                 ssl_password=None,
                 ssl_validate_ocsp=False,
                 ssl_validate_ocsp_stapled=False,
                 ssl_ocsp_context=None,
                 ssl_ocsp_expected_cert=None,
                 ssl_min_version=None,
                 ssl_ciphers=None,
                 max_connections=None,
                 single_connection_client=False,
                 health_check_interval=0,
                 client_name=None,
                 lib_name="redis-py",
                 username=None,
                 retry=None,
                 redis_connect_func=None,
                 credential_provider=None,
                 protocol=2,
                 cache=None,
                 cache_config=None):
        self.redis_client = redis.Redis(host=host, port=port, db=db, password=password,
                                        socket_timeout=socket_timeout,
                                        socket_connect_timeout=socket_connect_timeout,
                                        socket_keepalive=socket_keepalive,
                                        socket_keepalive_options=socket_keepalive_options,
                                        connection_pool=connection_pool,
                                        unix_socket_path=unix_socket_path,
                                        encoding=encoding,
                                        encoding_errors=encoding_errors,
                                        charset=charset,
                                        errors=errors,
                                        decode_responses=decode_responses,
                                        retry_on_timeout=retry_on_timeout,
                                        retry_on_error=retry_on_error,
                                        ssl=ssl,
                                        ssl_keyfile=ssl_keyfile,
                                        ssl_certfile=ssl_certfile,
                                        ssl_cert_reqs=ssl_cert_reqs,
                                        ssl_ca_certs=ssl_ca_certs,
                                        ssl_ca_path=ssl_ca_path,
                                        ssl_ca_data=ssl_ca_data,
                                        ssl_check_hostname=ssl_check_hostname,
                                        ssl_password=ssl_password,
                                        ssl_validate_ocsp=ssl_validate_ocsp,
                                        ssl_validate_ocsp_stapled=ssl_validate_ocsp_stapled,
                                        ssl_ocsp_context=ssl_ocsp_context,
                                        ssl_ocsp_expected_cert=ssl_ocsp_expected_cert,
                                        ssl_min_version=ssl_min_version,
                                        ssl_ciphers=ssl_ciphers,
                                        max_connections=max_connections,
                                        single_connection_client=single_connection_client,
                                        health_check_interval=health_check_interval,
                                        client_name=client_name,
                                        lib_name=lib_name,
                                        username=username,
                                        retry=retry,
                                        redis_connect_func=redis_connect_func,
                                        credential_provider=credential_provider,
                                        protocol=protocol,
                                        cache=cache,
                                        cache_config=cache_config)

    def get_redis_time_mill_second(self):
        nowtime = self.redis_client.time()
        return nowtime[0] * 1000 + (nowtime[1] // 1000)

    def incr_or_set_with_limit(self, key: str, default: int = 0, limit: int = 100000):
        """
            如果 key 存在则自增并返回新值，否则设置默认值并返回。

            Args:
                redis_client: Redis 客户端
                key: Redis 键名
                default: 如果 key 不存在，设置的默认值（默认为 0）

            Returns:
                int: 自增后的值或默认值
        """
        # 使用 Lua 脚本保证原子性
        lua_script = """
                local current = redis.call('GET', KEYS[license])
                if current then
                    current = tonumber(current)
                    if current >= tonumber(ARGV[2]) then
                        redis.call('SET', KEYS[license], ARGV[license])
                        return tonumber(ARGV[license])
                    else
                        return redis.call('INCR', KEYS[license])
                    end
                else
                    redis.call('SET', KEYS[license], ARGV[license])
                    return tonumber(ARGV[license])
                end
            """
        return self.redis_client.eval(lua_script, 1, key, default, limit)


class RedisLock:
    """
    redis实现互斥锁，支持重入和续锁
    """

    def __init__(self, conn, lock_name, expire=30, uid=None, is_renew=True):
        self.conn = conn
        self.lock_script = None
        self.unlock_script = None
        self.renew_script = None
        self.register_script()

        self._name = f"autospider:lock:{lock_name}"
        self._expire = int(expire)
        self._uid = uid or str(uuid.uuid4())

        self._lock_renew_interval = self._expire * 2 / 3
        self._lock_renew_threading = None

        self.is_renew = is_renew
        self.is_acquired = None
        self.is_released = None

    @property
    def id(self):
        return self._uid

    @property
    def expire(self):
        return self._expire

    def acquire(self):
        result = self.lock_script(keys=(self._name,), args=(self._expire, self._uid))
        if self.is_renew:
            self._start_renew_threading()
        self.is_acquired = True if result else False
        logger.info(f"争抢锁：{self._uid}-{self.is_acquired}\n")
        return self.is_acquired

    def release(self):
        if self.is_renew:
            self._stop_renew_threading()

        result = self.unlock_script(keys=(self._name,), args=(self._uid,))
        self.is_released = True if result else False
        logger.info(f"释放锁:{self.is_released}")
        return self.is_released

    def register_script(self):
        self.lock_script = self.conn.register_script(LOCK_SCRIPT)
        self.unlock_script = self.conn.register_script(UNLOCK_SCRIPT)
        self.renew_script = self.conn.register_script(RENEW_SCRIPT)

    def renew(self, renew_expire=30):
        result = self.renew_script(keys=(self._name,), args=(renew_expire,))
        if result == 1:
            raise Exception(f"{self._name} 没有获得锁或锁过期！")
        elif result == 2:
            raise Exception(f"{self._name} 未设置过期时间")
        elif result:
            raise Exception(f"未知错误码: {result}")
        logger.info("锁续期", result)

    @staticmethod
    def _renew_scheduler(weak_self, interval, lock_event):
        while not lock_event.wait(timeout=interval):
            lock = weak_self()
            if lock is None:
                break
            lock.renew(renew_expire=lock.expire)
            del lock

    def _start_renew_threading(self):
        self.lock_event = threading.Event()
        self._lock_renew_threading = threading.Thread(target=self._renew_scheduler,
                                                      kwargs={
                                                          "weak_self": weakref.ref(self),
                                                          "interval": self._lock_renew_interval,
                                                          "lock_event": self.lock_event
                                                      })

        self._lock_renew_threading.demon = True
        self._lock_renew_threading.start()

    def _stop_renew_threading(self):
        if self._lock_renew_threading is None or not self._lock_renew_threading.is_alive():
            return
        self.lock_event.set()
        # join 作用是确保thread子线程执行完毕后才能执行下一个线程
        self._lock_renew_threading.join()
        self._lock_renew_threading = None

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type=None, exc_val=None, exc_tb=None):
        self.release()


# redis 锁切面方法,参数为初始化的redis客户端
def redis_lock_aspect(redis_client):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 第一个参数作为redis锁的名称，将后续参数传给被装饰的函数
            with RedisLock(redis_client, args[0], uid=threading.get_ident(), expire=30) as r:
                if r.is_acquired:
                    return func(args[1:], **kwargs)
                else:
                    return None

        return wrapper

    return decorate