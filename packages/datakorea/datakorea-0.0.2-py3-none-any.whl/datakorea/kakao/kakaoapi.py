
class kakaoapi:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://dapi.kakao.com/v2/search"
        self.headers = {
            "Authorization": f"KakaoAK {self.api_key}"
        }

    def search_blog(self, query, page=1, size=10):
        url = f"{self.base_url}/blog"
        params = {
            "query": query,
            "page": page,
            "size": size
        }
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()


