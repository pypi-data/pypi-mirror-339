from typing import Optional, Dict, Any, List, AsyncIterator
from ..async_request import AsyncRequester
from ..model import DatasetResponse, DatasetListResponse, Dataset
from ..paginator import Paginator

class AsyncDatasetsClient:
    def __init__(self, requester: AsyncRequester):
        self.requester = requester

    async def create(
        self,
        name: str,
        description: Optional[str] = None,
        indexing_technique: str = "high_quality"
    ) -> DatasetResponse:
        """
        创建数据集
        
        Args:
            name: 数据集名称
            description: 数据集描述
            indexing_technique: 索引技术，可选值：high_quality, economy
            
        Returns:
            DatasetResponse: 数据集响应
        """
        data = {
            "name": name,
            "indexing_technique": indexing_technique
        }
        if description:
            data["description"] = description
            
        response = await self.requester.post("/datasets", json=data)
        return DatasetResponse(**response)

    def list(
        self,
        limit: int = 20,
        order: str = "desc"
    ) -> Paginator[Dataset]:
        """
        获取数据集列表（分页）
        
        Args:
            limit: 每页数量
            order: 排序方式，可选值：asc, desc
            
        Returns:
            Paginator[Dataset]: 数据集分页器
        """
        params = {
            "limit": limit,
            "order": order
        }
        return Paginator(
            requester=self.requester,
            path="/datasets",
            params=params,
            item_class=Dataset
        )

    async def get_list(
        self,
        limit: int = 20,
        order: str = "desc"
    ) -> DatasetListResponse:
        """
        获取数据集列表（单页）
        
        Args:
            limit: 数据集数量限制
            order: 排序方式，可选值：asc, desc
            
        Returns:
            DatasetListResponse: 数据集列表响应
        """
        params = {
            "limit": limit,
            "order": order
        }
        response = await self.requester.get("/datasets", params=params)
        return DatasetListResponse(**response)

    async def get(self, dataset_id: str) -> DatasetResponse:
        """
        获取数据集信息
        
        Args:
            dataset_id: 数据集ID
            
        Returns:
            DatasetResponse: 数据集响应
        """
        response = await self.requester.get(f"/datasets/{dataset_id}")
        return DatasetResponse(**response)

    async def update(
        self,
        dataset_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None
    ) -> DatasetResponse:
        """
        更新数据集
        
        Args:
            dataset_id: 数据集ID
            name: 数据集名称
            description: 数据集描述
            
        Returns:
            DatasetResponse: 数据集响应
        """
        data = {}
        if name:
            data["name"] = name
        if description:
            data["description"] = description
            
        response = await self.requester.put(f"/datasets/{dataset_id}", json=data)
        return DatasetResponse(**response)

    async def delete(self, dataset_id: str) -> Dict:
        """
        删除数据集
        
        Args:
            dataset_id: 数据集ID
            
        Returns:
            Dict: 响应数据
        """
        return await self.requester.delete(f"/datasets/{dataset_id}")

    async def add_documents(
        self,
        dataset_id: str,
        documents: List[Dict[str, Any]]
    ) -> Dict:
        """
        添加文档到数据集
        
        Args:
            dataset_id: 数据集ID
            documents: 文档列表
            
        Returns:
            Dict: 响应数据
        """
        data = {
            "documents": documents
        }
        return await self.requester.post(f"/datasets/{dataset_id}/documents", json=data) 