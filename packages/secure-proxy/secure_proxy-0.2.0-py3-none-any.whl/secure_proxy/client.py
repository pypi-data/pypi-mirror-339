import httpx
from .config import API_BASE

class SecureProxyClient:
    def __init__(self, proxy_token: str):
        self.api_base = API_BASE
        self.proxy_token = proxy_token
        self.proxy_url = None

    async def _get_proxy_url(self):
        """Serverdan shifrlangan proxy URL'ni ochib olish"""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.api_base}", params={"proxy_token": self.proxy_token})
            data = response.json()
            if "proxy_url" in data:
                return data["proxy_url"]
            else:
                raise ValueError("Invalid or expired proxy token")

    async def request(self, url: str):
        """Proxy orqali HTTP so‘rov yuborish"""
        if self.proxy_url is None:
            self.proxy_url = await self._get_proxy_url()

        proxies = {"http://": self.proxy_url, "https://": self.proxy_url}
        
        async with httpx.AsyncClient(proxies=proxies) as client:
            response = await client.get(url)

        return response.content, response.status_code
