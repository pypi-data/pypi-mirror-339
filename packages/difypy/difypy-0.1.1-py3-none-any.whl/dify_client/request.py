import requests
from typing import Optional, Dict, Any, Union
from .exception import DifyError
from .util import remove_url_trailing_slash

class Requester:
    def __init__(self, auth, base_url: str):
        """
        初始化请求器
        
        Args:
            auth: 认证对象
            base_url: API基础URL
        """
        if not base_url:
            raise ValueError("base_url is required")
            
        self.auth = auth
        self.base_url = remove_url_trailing_slash(base_url)
        self.session = requests.Session()
        self.session.headers.update(self.auth.get_headers())

    def _handle_response(self, response: requests.Response) -> Dict:
        if response.status_code >= 400:
            error_data = response.json()
            raise DifyError(
                message=error_data.get("message", "Unknown error"),
                status_code=response.status_code
            )
        return response.json()

    def get(self, path: str, params: Optional[Dict] = None) -> Dict:
        url = f"{self.base_url}{path}"
        response = self.session.get(url, params=params)
        return self._handle_response(response)

    def post(self, path: str, data: Optional[Dict] = None, json: Optional[Dict] = None, files: Optional[Dict] = None) -> Dict:
        url = f"{self.base_url}{path}"
        response = self.session.post(url, data=data, json=json, files=files)
        return self._handle_response(response)

    def put(self, path: str, data: Optional[Dict] = None, json: Optional[Dict] = None) -> Dict:
        url = f"{self.base_url}{path}"
        response = self.session.put(url, data=data, json=json)
        return self._handle_response(response)

    def delete(self, path: str) -> Dict:
        url = f"{self.base_url}{path}"
        response = self.session.delete(url)
        return self._handle_response(response)