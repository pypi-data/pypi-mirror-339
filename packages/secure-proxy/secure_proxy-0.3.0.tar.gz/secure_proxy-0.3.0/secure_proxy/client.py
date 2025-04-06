import httpx
from .config import API_BASE
from typing import Optional

class SecureProxyClient:
    def __init__(self, proxy_token: str):
        self.api_base = API_BASE
        self.proxy_token = proxy_token
        self.proxy_url = None

    async def _get_proxy_url(self) -> Optional[str]:
        """Serverdan shifrlangan proxy URL'ni ochib olish"""
        async with httpx.AsyncClient(follow_redirects=True) as client:
            try:
                response = await client.get(f"{self.api_base}", params={"proxy_token": self.proxy_token})
                print(response, "Res")
                response.raise_for_status()

                data = response.json()

                if "proxy_url" in data:
                    return data["proxy_url"]
                else:
                    raise ValueError("Invalid or expired proxy token")
            except httpx.HTTPStatusError as e:
                print(f"HTTP error occurred: {e}")
                return None
            except httpx.RequestError as e:
                print(f"Request error occurred: {e}")
                return None
            except ValueError as e:
                print(f"Error parsing response: {e}")
                return None
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                return None

    async def request(self, url: str):
        """Proxy orqali HTTP so‘rov yuborish"""
        if self.proxy_url is None:
            self.proxy_url = await self._get_proxy_url()

        async with httpx.AsyncClient(follow_redirects=True, proxy=self.proxy_url) as client:
            response = await client.post(url)
        return  response.content, response.status_code