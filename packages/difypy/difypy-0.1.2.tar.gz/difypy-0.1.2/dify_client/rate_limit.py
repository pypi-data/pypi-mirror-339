import asyncio
import time
from typing import Optional, Dict, Any
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class RateLimitConfig:
    """速率限制配置类"""
    requests_per_minute: int = 60  # 每分钟请求数
    burst_size: int = 10  # 突发请求数
    window_size: int = 60  # 时间窗口大小（秒）

class TokenBucket:
    """令牌桶类"""
    def __init__(self, rate: float, burst: int):
        """
        初始化令牌桶
        
        Args:
            rate: 令牌产生速率（每秒）
            burst: 最大令牌数
        """
        self.rate = rate
        self.burst = burst
        self.tokens = burst
        self.last_update = time.monotonic()

    async def acquire(self) -> bool:
        """
        获取令牌
        
        Returns:
            bool: 是否获取成功
        """
        now = time.monotonic()
        time_passed = now - self.last_update
        self.tokens = min(self.burst, self.tokens + time_passed * self.rate)
        self.last_update = now

        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False

class RateLimiter:
    """速率限制器类"""
    def __init__(self, config: Optional[RateLimitConfig] = None):
        """
        初始化速率限制器
        
        Args:
            config: 速率限制配置
        """
        self.config = config or RateLimitConfig()
        self.buckets: Dict[str, TokenBucket] = defaultdict(
            lambda: TokenBucket(
                rate=self.config.requests_per_minute / self.config.window_size,
                burst=self.config.burst_size
            )
        )

    async def acquire(self, key: str = "default") -> None:
        """
        获取令牌，如果获取失败则等待
        
        Args:
            key: 限制键
        """
        while not await self.buckets[key].acquire():
            await asyncio.sleep(0.1)  # 等待100ms后重试 