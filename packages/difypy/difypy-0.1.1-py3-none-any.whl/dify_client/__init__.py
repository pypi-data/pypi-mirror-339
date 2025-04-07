# __init__.py
from typing import Optional
from .auth import Auth
from .request import Requester
from .workflows import WorkflowsClient
from .chat import ChatClient
from .files import FilesClient
from .datasets import DatasetsClient
from .async_dify_client import AsyncDifyClient
from .logger import setup_logging
from .retry import RetryConfig
from .timeout import TimeoutConfig
from .rate_limit import RateLimitConfig
from .exception import (
    DifyError,
    AuthenticationError,
    PermissionDeniedError,
    ResourceNotFoundError,
    RateLimitError,
    ValidationError,
    InternalServerError,
    ServiceUnavailableError,
    ConnectionError,
    TimeoutError
)

class DifyClient:
    def __init__(
        self,
        api_key: str,
        base_url: str  # 改为必需参数
    ):
        """
        初始化 Dify 客户端
        
        Args:
            api_key: API密钥
            base_url: API基础URL，例如：https://dify.sre.gotokeep.com/v1
        """
        if not base_url:
            raise ValueError("base_url is required")
            
        self.auth = Auth(api_key)
        self.base_url = base_url.rstrip('/')
        self.requester = Requester(self.auth, self.base_url)

        # 初始化各个客户端
        self._workflows: Optional[WorkflowsClient] = None
        self._chat: Optional[ChatClient] = None
        self._files: Optional[FilesClient] = None
        self._datasets: Optional[DatasetsClient] = None

    @property
    def workflows(self) -> WorkflowsClient:
        if not self._workflows:
            self._workflows = WorkflowsClient(self.requester)
        return self._workflows

    @property
    def chat(self) -> ChatClient:
        if not self._chat:
            self._chat = ChatClient(self.requester)
        return self._chat

    @property
    def files(self) -> FilesClient:
        if not self._files:
            self._files = FilesClient(self.requester)
        return self._files

    @property
    def datasets(self) -> DatasetsClient:
        if not self._datasets:
            self._datasets = DatasetsClient(self.requester)
        return self._datasets

__all__ = [
    'DifyClient',
    'AsyncDifyClient',
    'setup_logging',
    'RetryConfig',
    'TimeoutConfig',
    'RateLimitConfig',
    'DifyError',
    'AuthenticationError',
    'PermissionDeniedError',
    'ResourceNotFoundError',
    'RateLimitError',
    'ValidationError',
    'InternalServerError',
    'ServiceUnavailableError',
    'ConnectionError',
    'TimeoutError'
]