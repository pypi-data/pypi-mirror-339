from typing import TypeVar, Generic, List, Optional, AsyncIterator, Dict, Any
from dataclasses import dataclass

T = TypeVar('T')

@dataclass
class Page(Generic[T]):
    """分页数据"""
    items: List[T]
    total: int
    page: int
    page_size: int
    has_more: bool

class Paginator(Generic[T]):
    """分页器"""
    def __init__(
        self,
        requester,
        path: str,
        params: Dict[str, Any],
        item_class: type
    ):
        """
        初始化分页器
        
        Args:
            requester: 请求器
            path: 请求路径
            params: 请求参数
            item_class: 数据项类型
        """
        self.requester = requester
        self.path = path
        self.params = params
        self.item_class = item_class
        self._current_page: Optional[Page[T]] = None

    async def fetch_page(self, page: int) -> Page[T]:
        """
        获取指定页的数据
        
        Args:
            page: 页码
            
        Returns:
            Page[T]: 分页数据
        """
        params = self.params.copy()
        params["page"] = page
        response = await self.requester.get(self.path, params=params)
        
        items = [self.item_class(**item) for item in response.get("items", [])]
        return Page(
            items=items,
            total=response.get("total", 0),
            page=page,
            page_size=response.get("page_size", 20),
            has_more=response.get("has_more", False)
        )

    async def __aiter__(self) -> AsyncIterator[T]:
        """
        异步迭代器，遍历所有数据项
        
        Yields:
            T: 数据项
        """
        page = 1
        while True:
            current_page = await self.fetch_page(page)
            if not current_page.items:
                break
                
            for item in current_page.items:
                yield item
                
            if not current_page.has_more:
                break
                
            page += 1

    async def iter_pages(self) -> AsyncIterator[Page[T]]:
        """
        异步迭代器，遍历所有分页
        
        Yields:
            Page[T]: 分页数据
        """
        page = 1
        while True:
            current_page = await self.fetch_page(page)
            if not current_page.items:
                break
                
            yield current_page
                
            if not current_page.has_more:
                break
                
            page += 1

    @property
    async def current_page(self) -> Page[T]:
        """
        获取当前页数据
        
        Returns:
            Page[T]: 当前页数据
        """
        if self._current_page is None:
            self._current_page = await self.fetch_page(1)
        return self._current_page 