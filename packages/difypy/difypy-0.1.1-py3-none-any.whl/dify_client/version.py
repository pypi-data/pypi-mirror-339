__version__ = "0.1.0" 

class AsyncDifyClient:
    def __init__(self, api_key: str, base_url: str = DIFY_BASE_URL):
        self.auth = Auth(api_key)
        self.base_url = base_url
        self.requester = AsyncRequester(self.auth, self.base_url) 

# 添加 WebSocket 支持
class WebsocketsClient:
    def __init__(self, requester):
        self.requester = requester

# 添加音频处理
class AudioClient:
    def __init__(self, requester):
        self.requester = requester

# 添加用户管理
class UsersClient:
    def __init__(self, requester):
        self.requester = requester 

class DifyError(Exception):
    def __init__(self, message: str, status_code: int = None, error_code: str = None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(f"Dify API Error: {message} (Status: {status_code}, Code: {error_code})") 

def format_timestamp(timestamp: int) -> str:
    """格式化时间戳"""
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def validate_file_type(file_type: str) -> bool:
    """验证文件类型"""
    valid_types = ['document', 'image', 'audio', 'video']
    return file_type in valid_types 

import logging

logger = logging.getLogger('dify_client')

class Requester:
    def __init__(self, auth, base_url: str):
        self.auth = auth
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update(self.auth.get_headers())
        logger.info(f"Initialized Requester with base_url: {base_url}")

    def _handle_response(self, response: requests.Response) -> Dict:
        if response.status_code >= 400:
            error_data = response.json()
            logger.error(f"API Error: {error_data}")
            raise DifyError(
                message=error_data.get("message", "Unknown error"),
                status_code=response.status_code
            )
        return response.json() 