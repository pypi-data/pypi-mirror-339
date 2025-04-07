import logging
import json
from typing import Optional
from datetime import datetime

class DifyLogger:
    """Dify日志记录器"""
    def __init__(self, name: str = "dify_client"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # 如果没有处理器，添加默认处理器
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def setup_logging(
        self,
        level: int = logging.INFO,
        format: Optional[str] = None,
        filename: Optional[str] = None
    ):
        """
        配置日志
        
        Args:
            level: 日志级别
            format: 日志格式
            filename: 日志文件路径
        """
        self.logger.setLevel(level)
        
        # 清除现有处理器
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
            
        # 添加新的处理器
        if filename:
            handler = logging.FileHandler(filename)
        else:
            handler = logging.StreamHandler()
            
        if format:
            formatter = logging.Formatter(format)
        else:
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_request(self, method: str, url: str, headers: dict, data: Optional[dict] = None):
        """
        记录请求日志
        
        Args:
            method: 请求方法
            url: 请求URL
            headers: 请求头
            data: 请求数据
        """
        if self.logger.isEnabledFor(logging.DEBUG):
            log_data = {
                "method": method,
                "url": url,
                "headers": headers,
                "data": data,
                "timestamp": datetime.now().isoformat()
            }
            self.logger.debug(f"Request: {json.dumps(log_data, indent=2)}")

    def log_response(self, status_code: int, headers: dict, data: Optional[dict] = None):
        """
        记录响应日志
        
        Args:
            status_code: 状态码
            headers: 响应头
            data: 响应数据
        """
        if self.logger.isEnabledFor(logging.DEBUG):
            log_data = {
                "status_code": status_code,
                "headers": headers,
                "data": data,
                "timestamp": datetime.now().isoformat()
            }
            self.logger.debug(f"Response: {json.dumps(log_data, indent=2)}")

    def log_error(self, error: Exception):
        """
        记录错误日志
        
        Args:
            error: 错误对象
        """
        self.logger.error(f"Error: {str(error)}", exc_info=True)

# 创建全局日志记录器实例
logger = DifyLogger()

def setup_logging(
    level: int = logging.INFO,
    format: Optional[str] = None,
    filename: Optional[str] = None
):
    """
    配置全局日志
    
    Args:
        level: 日志级别
        format: 日志格式
        filename: 日志文件路径
    """
    logger.setup_logging(level, format, filename) 