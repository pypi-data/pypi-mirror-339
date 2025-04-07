from dataclasses import dataclass
from typing import Optional

@dataclass
class TimeoutConfig:
    """超时配置类"""
    connect: float = 10.0  # 连接超时时间（秒）
    read: float = 30.0  # 读取超时时间（秒）
    write: float = 30.0  # 写入超时时间（秒）
    total: Optional[float] = None  # 总超时时间（秒）

    def to_aiohttp_timeout(self) -> dict:
        """
        转换为aiohttp的超时配置
        
        Returns:
            dict: aiohttp的超时配置
        """
        timeout = {
            "connect": self.connect,
            "sock_read": self.read,
            "sock_write": self.write
        }
        if self.total is not None:
            timeout["total"] = self.total
        return timeout 