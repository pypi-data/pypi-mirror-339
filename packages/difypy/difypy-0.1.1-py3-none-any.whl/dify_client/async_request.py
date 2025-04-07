import aiohttp
import asyncio
from typing import Optional, Dict, Any, Union
from .exception import DifyError, create_error_from_response, TimeoutError
from .util import remove_url_trailing_slash
from .stream import StreamResponse
from .logger import logger
from .retry import retry, RetryConfig
from .timeout import TimeoutConfig
from .rate_limit import RateLimiter, RateLimitConfig
from .trace import TraceManager, Trace

class AsyncRequester:
    def __init__(
        self,
        auth,
        base_url: str,
        retry_config: Optional[RetryConfig] = None,
        timeout_config: Optional[TimeoutConfig] = None,
        rate_limit_config: Optional[RateLimitConfig] = None,
        enable_tracing: bool = False
    ):
        """
        初始化异步请求器
        
        Args:
            auth: 认证对象
            base_url: API基础URL
            retry_config: 重试配置
            timeout_config: 超时配置
            rate_limit_config: 速率限制配置
            enable_tracing: 是否启用追踪
        """
        if not base_url:
            raise ValueError("base_url is required")
            
        self.auth = auth
        self.base_url = remove_url_trailing_slash(base_url)
        self.session = None
        self.headers = self.auth.get_headers()
        self.retry_config = retry_config or RetryConfig()
        self.timeout_config = timeout_config or TimeoutConfig()
        self.rate_limiter = RateLimiter(rate_limit_config)
        self.enable_tracing = enable_tracing
        self.trace_manager = TraceManager() if enable_tracing else None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers=self.headers,
            timeout=aiohttp.ClientTimeout(**self.timeout_config.to_aiohttp_timeout())
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    @retry()
    async def _handle_response(self, response: aiohttp.ClientResponse, trace: Optional[Trace] = None) -> Dict:
        try:
            if response.status >= 400:
                error_data = await response.json()
                error = create_error_from_response(response.status, error_data)
                if trace:
                    trace.add_event("error", {
                        "status_code": response.status,
                        "error": error.__dict__
                    })
                logger.log_error(error)
                raise error
            data = await response.json()
            if trace:
                trace.add_event("response", {
                    "status_code": response.status,
                    "headers": dict(response.headers),
                    "data": data
                })
            logger.log_response(response.status, dict(response.headers), data)
            return data
        except asyncio.TimeoutError as e:
            error = TimeoutError(
                message=str(e),
                details={"timeout_config": self.timeout_config.__dict__}
            )
            if trace:
                trace.add_event("error", {
                    "type": "timeout",
                    "error": error.__dict__
                })
            logger.log_error(error)
            raise error
        except aiohttp.ClientError as e:
            error = DifyError(
                message=str(e),
                status_code=0,
                code="connection_error"
            )
            if trace:
                trace.add_event("error", {
                    "type": "connection",
                    "error": error.__dict__
                })
            logger.log_error(error)
            raise error
        except Exception as e:
            error = DifyError(
                message=str(e),
                status_code=0,
                code="unknown_error"
            )
            if trace:
                trace.add_event("error", {
                    "type": "unknown",
                    "error": error.__dict__
                })
            logger.log_error(error)
            raise error

    async def _make_request(self, method: str, path: str, **kwargs) -> Dict:
        """
        发送请求，应用速率限制和追踪
        
        Args:
            method: 请求方法
            path: 请求路径
            **kwargs: 请求参数
            
        Returns:
            Dict: 响应数据
        """
        trace = None
        if self.enable_tracing:
            trace = self.trace_manager.start_trace()
            trace.add_event("request_start", {
                "method": method,
                "path": path,
                "params": kwargs
            })

        try:
            await self.rate_limiter.acquire(path)  # 使用路径作为限制键
            url = f"{self.base_url}{path}"
            logger.log_request(method, url, self.headers, kwargs.get("json") or kwargs.get("data"))
            
            if trace:
                trace.add_event("rate_limit_acquired", {
                    "path": path
                })

            async with getattr(self.session, method.lower())(url, **kwargs) as response:
                return await self._handle_response(response, trace)
        finally:
            if trace:
                trace.end()
                self.trace_manager.end_trace(trace.trace_id)

    @retry()
    async def get(self, path: str, params: Optional[Dict] = None) -> Dict:
        return await self._make_request("GET", path, params=params)

    @retry()
    async def post(self, path: str, data: Optional[Dict] = None, json: Optional[Dict] = None) -> Dict:
        return await self._make_request("POST", path, data=data, json=json)

    @retry()
    async def put(self, path: str, data: Optional[Dict] = None, json: Optional[Dict] = None) -> Dict:
        return await self._make_request("PUT", path, data=data, json=json)

    @retry()
    async def delete(self, path: str) -> Dict:
        return await self._make_request("DELETE", path)

    @retry()
    async def post_file(self, path: str, files: Dict[str, Any], data: Optional[Dict] = None) -> Dict:
        form_data = aiohttp.FormData()
        if data:
            for key, value in data.items():
                form_data.add_field(key, str(value))
        for key, value in files.items():
            if isinstance(value, tuple):
                form_data.add_field(key, value[1], filename=value[0])
            else:
                form_data.add_field(key, value)
        return await self._make_request("POST", path, data=form_data)

    @retry()
    async def stream(self, path: str, data: Optional[Dict] = None, json: Optional[Dict] = None) -> StreamResponse:
        """
        发送流式请求
        
        Args:
            path: 请求路径
            data: 表单数据
            json: JSON数据
            
        Returns:
            StreamResponse: 流式响应
        """
        trace = None
        if self.enable_tracing:
            trace = self.trace_manager.start_trace()
            trace.add_event("stream_request_start", {
                "path": path,
                "data": data,
                "json": json
            })

        try:
            await self.rate_limiter.acquire(path)  # 使用路径作为限制键
            url = f"{self.base_url}{path}"
            logger.log_request("POST", url, self.headers, json or data)
            
            if trace:
                trace.add_event("rate_limit_acquired", {
                    "path": path
                })

            async with self.session.post(url, data=data, json=json) as response:
                if response.status >= 400:
                    error_data = await response.json()
                    error = create_error_from_response(response.status, error_data)
                    if trace:
                        trace.add_event("error", {
                            "status_code": response.status,
                            "error": error.__dict__
                        })
                    logger.log_error(error)
                    raise error
                return StreamResponse(response)
        finally:
            if trace:
                trace.end()
                self.trace_manager.end_trace(trace.trace_id)

    def get_trace(self, trace_id: str) -> Optional[Dict[str, Any]]:
        """
        获取追踪数据
        
        Args:
            trace_id: 追踪ID
            
        Returns:
            Optional[Dict[str, Any]]: 追踪数据
        """
        if not self.enable_tracing:
            return None
        trace = self.trace_manager.get_trace(trace_id)
        return trace.to_dict() if trace else None 