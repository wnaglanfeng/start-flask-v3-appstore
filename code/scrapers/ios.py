from typing import Dict, Any
import requests
from config.country import countries

class IosScraper:
    def __init__(self):
        self.base_url = "https://itunes.apple.com"
        self.headers = {
            "accept": "application/json",
        }

    def search(self, market: str, region: str, keyword: str, page: int = 1, pagesize: int = 20) -> Dict[str, Any]:
        """
        执行苹果商店应用搜索
        :param market: 应用市场（iOS）
        :param region: 地区
        :param keyword: 关键词
        :param page: 页码
        :param pagesize: 每页大小
        :return: 搜索结果
        """
        url = f"{self.base_url}/search"
        params = {
            "term": keyword,
            "country": region,
            "media": "software",
            "limit": pagesize,
            "offset": (page - 1) * pagesize
        }

        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            results = response.json().get("results", [])
            
            return {
                "success": True,
                "data": [self._standardize_app_info(app) for app in results]
            }
        except requests.RequestException as e:
            return {
                "success": False,
                "error": str(e)
            }

    def detail(self, market: str, region: str, appid: str) -> Dict[str, Any]:
        """
        获取苹果商店应用详情
        :param market: 应用市场（iOS）
        :param region: 地区
        :param appid: 应用ID
        :return: 应用详情
        """
               # 验证应用商店和地区
        region_info = countries.get(region)
     
        
        url = f"{self.base_url}/lookup"
        params = {
            "id": appid,
            "country": region_info['simple_country_code']
        }

        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            app_info = response.json().get("results", [{}])[0]
            
            return self._standardize_app_info(app_info)
        except (requests.RequestException, IndexError) as e:
            return {
                "success": False,
                "error": str(e)
            }

    def _standardize_app_info(self, app_info: Dict[str, Any]) -> Dict[str, Any]:
        """标准化iOS应用信息"""
         # 合并 genreIds 和 genres
        genre_ids = app_info.get("genreIds", [])
        genres = app_info.get("genres", [])
        tags = [{"id": genre_id, "name": genre} for genre_id, genre in zip(genre_ids, genres)]
        
        return {
            "app_name": app_info.get("trackName", ""),
            "app_id": app_info.get("trackId", ""),
            "icon_url": app_info.get("artworkUrl512", app_info.get("artworkUrl100", "")),
            "tags": tags,
            "developer": app_info.get("artistName", ""),
            "download_count": 0,
            "icp_number": "",
            "introduction": app_info.get("description", ""),
            "bounde_id": app_info.get("bundleId", ""),
            "rating": app_info.get("averageUserRating", 0.0),
            "rating_count": app_info.get("userRatingCount", 0),
            "screenshots": app_info.get("screenshotUrls", []),
            "store": "ios",
            "update_time": app_info.get("currentVersionReleaseDate", ""),
            "version": app_info.get("version", ""),
            "download_url": app_info.get("trackViewUrl", ""),
            "region": app_info.get("country", "")
        }