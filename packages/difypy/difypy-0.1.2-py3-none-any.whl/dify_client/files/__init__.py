from typing import Optional, Dict
from ..model import FileUploadResponse
import requests
import time
import logging
from .async_client import AsyncFilesClient

logger = logging.getLogger('dify_client')

class DifyError(Exception):
    def __init__(self, message: str, status_code: int, error_code: str = None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(f"Dify API Error: {message} (Status: {status_code}, Code: {error_code})")

class DifyAuthenticationError(DifyError):
    pass

class DifyValidationError(DifyError):
    pass

class FilesClient:
    def __init__(self, requester):
        self.requester = requester

    def upload(
        self,
        file_path: str,
        user: str,
        file_type: str = "document"
    ) -> FileUploadResponse:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {
                'user': user,
                'type': file_type
            }
            response = self.requester.post(
                "/files/upload",
                data=data,
                files=files
            )
            return FileUploadResponse(**response)

class Requester:
    def __init__(self, auth, base_url: str, max_retries: int = 3):
        self.max_retries = max_retries
        logger.info(f"Initialized Requester with base_url: {base_url}")
        # ...

    def _retry_request(self, method: str, *args, **kwargs) -> Dict:
        for attempt in range(self.max_retries):
            try:
                return getattr(self.session, method)(*args, **kwargs)
            except requests.exceptions.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise DifyError(f"Request failed after {self.max_retries} attempts: {str(e)}")
                time.sleep(2 ** attempt)

    def _handle_response(self, response: requests.Response) -> Dict:
        if response.status_code >= 400:
            error_data = response.json()
            logger.error(f"API Error: {error_data}")
            # ... 

class AsyncDifyClient:
    def __init__(self, api_key: str, base_url: str = DIFY_BASE_URL):
        self.auth = Auth(api_key)
        self.base_url = base_url
        self.requester = AsyncRequester(self.auth, self.base_url) 

__all__ = ['FilesClient', 'AsyncFilesClient'] 