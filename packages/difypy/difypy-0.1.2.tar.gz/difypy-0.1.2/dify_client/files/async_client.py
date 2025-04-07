from typing import Optional, Dict, Any, BinaryIO
from ..async_request import AsyncRequester
from ..model import FileUploadResponse, FileListResponse

class AsyncFilesClient:
    def __init__(self, requester: AsyncRequester):
        self.requester = requester

    async def upload(
        self,
        file: BinaryIO,
        filename: str,
        purpose: str = "file"
    ) -> FileUploadResponse:
        """
        上传文件
        
        Args:
            file: 文件对象
            filename: 文件名
            purpose: 文件用途
            
        Returns:
            FileUploadResponse: 文件上传响应
        """
        files = {
            "file": (filename, file)
        }
        data = {
            "purpose": purpose
        }
        response = await self.requester.post_file("/files", files=files, data=data)
        return FileUploadResponse(**response)

    async def list(
        self,
        purpose: Optional[str] = None,
        limit: int = 20,
        order: str = "desc"
    ) -> FileListResponse:
        """
        获取文件列表
        
        Args:
            purpose: 文件用途
            limit: 文件数量限制
            order: 排序方式，可选值：asc, desc
            
        Returns:
            FileListResponse: 文件列表响应
        """
        params = {
            "limit": limit,
            "order": order
        }
        if purpose:
            params["purpose"] = purpose
            
        response = await self.requester.get("/files", params=params)
        return FileListResponse(**response)

    async def delete(self, file_id: str) -> Dict:
        """
        删除文件
        
        Args:
            file_id: 文件ID
            
        Returns:
            Dict: 响应数据
        """
        return await self.requester.delete(f"/files/{file_id}")

    async def get(self, file_id: str) -> FileUploadResponse:
        """
        获取文件信息
        
        Args:
            file_id: 文件ID
            
        Returns:
            FileUploadResponse: 文件信息响应
        """
        response = await self.requester.get(f"/files/{file_id}")
        return FileUploadResponse(**response) 