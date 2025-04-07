from typing import Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum

class ErrorCode(Enum):
    """错误代码枚举"""
    UNKNOWN_ERROR = "unknown_error"
    INVALID_REQUEST = "invalid_request"
    AUTHENTICATION_ERROR = "authentication_error"
    PERMISSION_DENIED = "permission_denied"
    RESOURCE_NOT_FOUND = "resource_not_found"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    INTERNAL_SERVER_ERROR = "internal_server_error"
    SERVICE_UNAVAILABLE = "service_unavailable"
    VALIDATION_ERROR = "validation_error"
    CONNECTION_ERROR = "connection_error"
    TIMEOUT_ERROR = "timeout_error"

@dataclass
class DifyError(Exception):
    """Dify API错误基类"""
    message: str
    status_code: int
    code: ErrorCode = ErrorCode.UNKNOWN_ERROR
    details: Optional[Dict[str, Any]] = None

    def __str__(self) -> str:
        return f"{self.code.value}: {self.message} (status: {self.status_code})"

class AuthenticationError(DifyError):
    """认证错误"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=401,
            code=ErrorCode.AUTHENTICATION_ERROR,
            details=details
        )

class PermissionDeniedError(DifyError):
    """权限错误"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=403,
            code=ErrorCode.PERMISSION_DENIED,
            details=details
        )

class ResourceNotFoundError(DifyError):
    """资源未找到错误"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=404,
            code=ErrorCode.RESOURCE_NOT_FOUND,
            details=details
        )

class RateLimitError(DifyError):
    """速率限制错误"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=429,
            code=ErrorCode.RATE_LIMIT_EXCEEDED,
            details=details
        )

class ValidationError(DifyError):
    """验证错误"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=400,
            code=ErrorCode.VALIDATION_ERROR,
            details=details
        )

class InternalServerError(DifyError):
    """服务器内部错误"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=500,
            code=ErrorCode.INTERNAL_SERVER_ERROR,
            details=details
        )

class ServiceUnavailableError(DifyError):
    """服务不可用错误"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=503,
            code=ErrorCode.SERVICE_UNAVAILABLE,
            details=details
        )

class ConnectionError(DifyError):
    """连接错误"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=0,
            code=ErrorCode.CONNECTION_ERROR,
            details=details
        )

class TimeoutError(DifyError):
    """超时错误"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=0,
            code=ErrorCode.TIMEOUT_ERROR,
            details=details
        )

def create_error_from_response(status_code: int, error_data: Dict[str, Any]) -> DifyError:
    """
    根据响应创建对应的错误对象
    
    Args:
        status_code: HTTP状态码
        error_data: 错误数据
        
    Returns:
        DifyError: 对应的错误对象
    """
    message = error_data.get("message", "Unknown error")
    code = ErrorCode(error_data.get("code", ErrorCode.UNKNOWN_ERROR.value))
    details = error_data.get("details")
    
    error_map = {
        400: ValidationError,
        401: AuthenticationError,
        403: PermissionDeniedError,
        404: ResourceNotFoundError,
        429: RateLimitError,
        500: InternalServerError,
        503: ServiceUnavailableError
    }
    
    error_class = error_map.get(status_code, DifyError)
    return error_class(message=message, details=details) 