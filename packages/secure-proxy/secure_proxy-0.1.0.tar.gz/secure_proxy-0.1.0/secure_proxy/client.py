import httpx

class SecureProxyClient:
    def __init__(self, api_base: str, proxy_token: str):
        self.api_base = api_base
        self.proxy_token = proxy_token
        self.proxy_url = self._get_proxy_url()

    def _get_proxy_url(self):
        """Serverdan shifrlangan proxy URL'ni ochib olish"""
        response = httpx.get(f"{self.api_base}/api/decrypt_proxy", params={"proxy_token": self.proxy_token})
        data = response.json()
        if "proxy_url" in data:
            return data["proxy_url"]
        else:
            raise ValueError("Invalid or expired proxy token")

    def request(self, url: str):
        """Proxy orqali HTTP so‘rov yuborish"""
        proxies = {"http://": self.proxy_url, "https://": self.proxy_url}
        with httpx.Client(proxies=proxies) as client:
            response = client.get(url)
        return response.content, response.status_code
