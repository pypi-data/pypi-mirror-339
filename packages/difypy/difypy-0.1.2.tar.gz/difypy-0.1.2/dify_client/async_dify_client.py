from typing import Optional
from .auth import Auth
from .async_request import AsyncRequester
from .workflows import AsyncWorkflowsClient
from .chat import AsyncChatClient
from .files import AsyncFilesClient
from .datasets import AsyncDatasetsClient

class AsyncDifyClient:
    def __init__(
        self,
        api_key: str,
        base_url: str
    ):
        """
        初始化异步 Dify 客户端
        
        Args:
            api_key: API密钥
            base_url: API基础URL
        """
        if not base_url:
            raise ValueError("base_url is required")
            
        self.auth = Auth(api_key)
        self.base_url = base_url.rstrip('/')
        self.requester = AsyncRequester(self.auth, self.base_url)

        # 初始化各个客户端
        self._workflows: Optional[AsyncWorkflowsClient] = None
        self._chat: Optional[AsyncChatClient] = None
        self._files: Optional[AsyncFilesClient] = None
        self._datasets: Optional[AsyncDatasetsClient] = None

    async def __aenter__(self):
        await self.requester.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.requester.__aexit__(exc_type, exc_val, exc_tb)

    @property
    def workflows(self) -> AsyncWorkflowsClient:
        if not self._workflows:
            self._workflows = AsyncWorkflowsClient(self.requester)
        return self._workflows

    @property
    def chat(self) -> AsyncChatClient:
        if not self._chat:
            self._chat = AsyncChatClient(self.requester)
        return self._chat

    @property
    def files(self) -> AsyncFilesClient:
        if not self._files:
            self._files = AsyncFilesClient(self.requester)
        return self._files

    @property
    def datasets(self) -> AsyncDatasetsClient:
        if not self._datasets:
            self._datasets = AsyncDatasetsClient(self.requester)
        return self._datasets 