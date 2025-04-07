import os
from typing import Optional, Union, Awaitable, List
import redis
import aioredis
from aioredis.client import ChannelT, ExpiryT, PubSub
from redis.typing import KeyT, EncodableT, ResponseT


class BaseRedisClient:
    def __init__(self, username: str = "", host: str = "", port: int = None, password: str = "", db_num: int = 7,
                 is_async=False):
        self.is_async = is_async
        self.db_num = db_num
        self.host = host if host else os.getenv("REDIS_HOST", "localhost")
        self.port = port if port else os.getenv("REDIS_PORT", "6379")
        self.password = password if password else os.getenv("REDIS_PASSWORD", "")
        self.username = username if username else os.getenv("REDIS_USER", "")
        self.conn = f"{self.host}:{self.port},password={self.password},connectTimeout=1000,abortConnect=false"
        if self.username:
            self.conn = f"username={self.username}," + self.conn

    def convert_to_redispy_pool(self) -> redis.ConnectionPool:
        """将apollo取出的redis连接串转成redispy所用的连接池"""
        parameters = {}

        # 分割连接串，获取参数列表
        params = self.conn.split(",")

        # 解析参数列表
        for param in params:
            key_value = param.split("=")
            if len(key_value) == 2:
                key, value = key_value
                parameters[key.strip()] = value.strip()
            elif len(key_value) == 1:
                if ":" in key_value[0]:
                    # 如果没有给定host参数，则将IP地址和端口号作为参数
                    host, port = key_value[0].split(":")
                    parameters["host"] = host.strip()
                    parameters["port"] = int(port.strip())
                else:
                    key = key_value[0].strip()
                    parameters[key] = ""

        host = parameters.get("host", "localhost")
        # 构建redis-py连接池
        if self.is_async:
            pool = aioredis.ConnectionPool(
                host=host,
                port=parameters.get("port", 6379),
                db=self.db_num,
                password=parameters.get("password"),
                username=parameters.get("username"),
                socket_timeout=int(parameters.get("connectTimeout", 1000)) / 1000,
                encoding='utf-8',
                decode_responses=True,
                max_connections=100,
                retry_on_timeout=True,
                socket_connect_timeout=30,
                health_check_interval=1

            )
        else:
            pool = redis.ConnectionPool(
                host=host,
                port=parameters.get("port", 6379),
                password=parameters.get("password"),
                username=parameters.get("username"),
                db=self.db_num,
                socket_timeout=int(parameters.get("connectTimeout", 1000)) / 1000,
                decode_responses=True,
            )
        return pool


class RedisClient(BaseRedisClient):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RedisClient, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, username: str = "", host: str = "", port: int = None, password: str = "", db_num: int = 7):
        super().__init__(username=username, host=host, port=port, password=password, db_num=db_num)
        self.db_num = db_num
        self.redis_client = redis.Redis(connection_pool=self.convert_to_redispy_pool(), retry_on_timeout=True,
                                        socket_timeout=30, socket_connect_timeout=30, retry_on_error=True,
                                        max_connections=100)

    def set(self, name: KeyT, value: EncodableT, expiry=None, **kwargs: object) -> ResponseT:
        """

        :rtype: object
        """
        return self.redis_client.set(name=name, value=value, ex=expiry, **kwargs)

    def ttl(self, name: KeyT) -> ResponseT:
        return self.redis_client.ttl(name)

    def llen(self, name: str) -> Union[Awaitable[int], int]:
        return self.redis_client.llen(name)

    def lpop(self, name: str, count: Optional[int] = None, ) -> Union[
        Awaitable[Union[str, List, None]], Union[str, List, None]]:
        return self.redis_client.lpop(name=name, count=count)

    def keys(self, name: KeyT) -> Union[Awaitable[List[str]], List[str]]:
        return self.redis_client.keys(name)


class AsyncRedisClient(BaseRedisClient):
    """
    创建的实例只允许在同一个时间循环中使用
    """

    def __init__(self, username: str = "", host: str = "", port: int = None, password: str = "", db_num: int = 7):
        super().__init__(username=username, host=host, port=port, password=password, db_num=db_num, is_async=True)
        self.redis_client = None

    async def connect(self):
        """连接到 Redis 服务器。"""
        self.redis_client = aioredis.Redis(connection_pool=self.convert_to_redispy_pool(), socket_connect_timeout=30,
                                           socket_timeout=30, retry_on_timeout=True, max_connections=100,
                                           health_check_interval=1)
        return self.redis_client

    async def disconnect(self):
        """断开与 Redis 服务器的连接。"""
        if self.redis_client:
            await self.redis_client.close()

    async def execute_func(self, func_name: str, *args, **kwargs) -> ResponseT:
        redis_client = await self.connect()
        self.redis_client = redis_client
        method = getattr(redis_client, func_name, None)
        if method is not None:
            return await method(*args, **kwargs)
        else:
            raise AttributeError(f'{redis_client.__class__.__name__} has no attribute {func_name}')

    async def execute_sync_func(self, func_name: str, *args, **kwargs) -> ResponseT:
        redis_client = await self.connect()
        self.redis_client = redis_client
        method = getattr(redis_client, func_name, None)
        if method is not None:
            return method(*args, **kwargs)
        else:
            raise AttributeError(f'{redis_client.__class__.__name__} has no attribute {func_name}')

    async def set(self, name, value, expiry=None):
        await self.connect()
        """设置键值对。"""
        return await self.execute_func("set", name, value, ex=expiry)

    async def get(self, name):
        """获取键对应的值。"""
        return await self.execute_func("get", name)

    async def keys(self, name: KeyT):
        return await self.execute_func("keys", name)

    async def publish(self, channel: ChannelT, message: EncodableT) -> None:
        """
        Publishes a message to a specific Redis channel.

        Args:
            channel (str): Channel or room ID.
            message (str): Message to be published.
        """
        return await self.execute_func("publish", channel=channel, message=message)

    async def lpush(self, name: KeyT, value: EncodableT):
        return await self.execute_func("lpush", name, value)

    async def rpush(self, name: KeyT, *values: EncodableT):
        return await self.execute_func(func_name="rpop", name=name, *values)

    async def rpop(self, name):
        return await self.execute_func(func_name="rpop", name=name)

    async def set_string(self, name: KeyT,
                         value: EncodableT,
                         ex: Optional[ExpiryT] = None,
                         px: Optional[ExpiryT] = None,
                         nx: bool = False,
                         xx: bool = False,
                         keepttl: bool = False, ):
        return await self.execute_func(func_name="set", name=name, value=value, ex=ex, px=px, nx=nx, xx=xx,
                                       keepttl=keepttl)

    async def llen(self, name):
        return await self.execute_func(func_name="llen", name=name)

    async def pubsub(self) -> PubSub:
        return await self.execute_sync_func(func_name="pubsub")


class RedisPubSubManager(BaseRedisClient):
    """
        Initializes the RedisPubSubManager.

    Args:
        host (str): Redis server host.
        port (int): Redis server port.
    """

    def __init__(self, username: str = "", host: str = "", port: int = None, password: str = "", db_num: int = 7):
        super().__init__(username=username, host=host, port=port, password=password, db_num=db_num, is_async=True)
        self.pubsub = None
        self.redis_client = None

    async def _get_redis_connection(self) -> aioredis.Redis:
        """
        Establishes a connection to Redis.

        Returns:
            aioredis.Redis: Redis connection object.
        """
        return aioredis.Redis(connection_pool=self.convert_to_redispy_pool())

    async def connect(self) -> None:
        """
        Connects to the Redis server and initializes the pubsub _client.
        """
        self.redis_client = await self._get_redis_connection()
        self.pubsub = self.redis_client.pubsub()

    async def publish(self, room_id: str, message: str) -> None:
        """
        Publishes a message to a specific Redis channel.

        Args:
            room_id (str): Channel or room ID.
            message (str): Message to be published.
        """
        await self.redis_client.publish(room_id, message)

    async def subscribe(self, room_id: str) -> aioredis.Redis:
        """
        Subscribes to a Redis channel.

        Args:
            room_id (str): Channel or room ID to subscribe to.

        Returns:
            aioredis.ChannelSubscribe: PubSub object for the subscribed channel.
        """
        await self.pubsub.subscribe(room_id)
        return self.pubsub

    async def unsubscribe(self, room_id: str) -> None:
        """
        Unsubscribes from a Redis channel.

        Args:
            room_id (str): Channel or room ID to unsubscribe from.
        """
        await self.pubsub.unsubscribe(room_id)
