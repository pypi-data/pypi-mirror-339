import asyncio
import random
from typing import Callable, Type, Tuple, Optional
from functools import wraps
from .exception import DifyError, ConnectionError, TimeoutError, ServiceUnavailableError

class RetryConfig:
    """重试配置类"""
    def __init__(
        self,
        max_retries: int = 3,
        initial_delay: float = 1.0,
        max_delay: float = 10.0,
        exponential_base: float = 2.0,
        jitter: bool = True,
        retry_on_exceptions: Tuple[Type[Exception], ...] = (
            ConnectionError,
            TimeoutError,
            ServiceUnavailableError
        )
    ):
        """
        初始化重试配置
        
        Args:
            max_retries: 最大重试次数
            initial_delay: 初始延迟时间（秒）
            max_delay: 最大延迟时间（秒）
            exponential_base: 指数退避基数
            jitter: 是否添加随机抖动
            retry_on_exceptions: 需要重试的异常类型
        """
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter
        self.retry_on_exceptions = retry_on_exceptions

def retry(config: Optional[RetryConfig] = None):
    """
    重试装饰器
    
    Args:
        config: 重试配置，如果为None则使用默认配置
    """
    if config is None:
        config = RetryConfig()

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(config.max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except config.retry_on_exceptions as e:
                    last_exception = e
                    if attempt == config.max_retries:
                        break

                    # 计算延迟时间
                    delay = config.initial_delay * (config.exponential_base ** attempt)
                    if config.jitter:
                        delay = delay * (1 + random.random() * 0.1)  # 添加10%的随机抖动
                    delay = min(delay, config.max_delay)

                    # 等待重试
                    await asyncio.sleep(delay)
            raise last_exception
        return wrapper
    return decorator 