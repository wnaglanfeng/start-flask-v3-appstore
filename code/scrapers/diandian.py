import pickle
import random
import requests
import execjs
import re
import os
import time

from typing import Dict, Any, Optional
from config.market import markets
from config.country import countries

class DiandianScraper:
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.cookie_dir = os.path.join(self.current_dir, 'cookies')  # 新增cookie目录
        
        self.js_path = os.path.join(self.current_dir, 'diandian_encrypt.js')
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Origin': 'https://app.diandian.com',
            'Pragma': 'no-cache',
            'Referer': 'https://app.diandian.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        self.cookies = self._load_cookies()

    def _load_cookies(self):
        cookie_file = os.path.join(self.cookie_dir, 'diandian_auth.pkl')
        if os.path.exists(cookie_file):
            with open(cookie_file, 'rb') as f:
                pkl_data = pickle.load(f)
                return {cookie['name']: cookie['value'] for cookie in pkl_data} if isinstance(pkl_data, list) else pkl_data
        return {}

    def _validate_market_and_region(self, market, region):
        from config.market import markets
        market_info = markets.get(market)
        if not market_info:
            raise ValueError(f"Invalid market: {market}")
    
        if market_info['global_availability'] == 'single_region':
            return market, market_info['available_regions'][0]
        elif market_info['global_availability'] == 'multi_region':
            if region not in market_info['available_regions']:
                return market, market_info['available_regions'][0]
        return market, region

    def _generate_search_params(self, market: str, region: str, keyword: str, page: int, pagesize: int) -> Dict[str, str]:
        """生成搜索参数"""
        market_info = markets.get(market)
        region_info = countries.get(region)
        
        current_time = int(time.time())
        compare_time = current_time - (current_time % 86400) - 86400
        
        return {
            'market_id': str(market_info['dd_market_id']),
            'country_id': str(region_info['dd_country_id']),
            'word': requests.utils.quote(keyword),
            'device_id': '',
            'system_type': '4' if market_info['type'] == 'ios' else '',
            'time': str(current_time),
            'compare_time': str(compare_time),
            'result_type': '',
            'payment_type': '',
            'page': str(page),
            'page_size': str(pagesize),
            'width_google_other_data': '0',
            'market_type': '0' if market == 'ios' else '-1'
        }
    # http://localhost:9000/api/appstore/search?market=ios&region=CHN&keyword=weixin&page=1&pagesize=20&sp=diandian
    # 应用搜索接口
    def search(self, market: str, region: str, keyword: str, page: int = 1, pagesize: int = 20) -> Dict[str, Any]:
        # 验证应用商店和地区
        market, region = self._validate_market_and_region(market, region)
        
        # 生成搜索参数
        params = self._generate_search_params(market, region, keyword, page, pagesize)
        
        # 执行JS加密
        with open(self.js_path, 'r', encoding='utf-8') as f:
            js_code = f.read()
        js = execjs.compile(js_code)
        
        # 获取加密参数
        content = requests.get("https://app.diandian.com/", headers=self.headers, cookies=self.cookies).text
        s = re.findall('u:\{s:"(.*?)"', content)[0]
        k = re.findall('u:\{.*?k:"(.*?)"', content)[0]
        l = re.findall('u:\{.*?l:"(.*?)"', content)[0]
        
        data = {'s': s, 'k': k, 'l': l, 'd': 0, 'sort': 'dd', 'num': 10}
        params['k'] = js.call('gen_search_k', params, data)
        
        # 发送请求
        response = requests.get(
            'https://api.diandian.com/pc/app/v2/word/search',
            params=params,
            headers=self.headers,
            cookies=self.cookies
        )
        response.raise_for_status()
        apps = response.json().get("data", [])["list"]
         # 添加调试信息
        result = []
        for app in apps:
            print(f"Processing app: {app}")  # 打印出正在处理的app数据
            try:
                if app is None or app.get("app") is None or app.get("app").get("app_id") is None:
                    continue
                result.append(self._standardize_app_info(market, app["app"]))
            except Exception as e:
                print("---------------------------------------------")  
                print(f"Error processing app: {app}")  # 打印出有问题的app数据
                print(f"Error details: {str(e)}")  # 打印错误详情
                raise  # 重新抛出异常以便调试

        return result
        # return  [self._standardize_app_info(market,app["app"]) for app in apps]

    # http://localhost:9000/api/appstore/detail?market=ios&region=CHN&sp=diandian&appid=492ududjqxzr9aj
    # 应用详情接口
    def detail(self, market: str, region: str, appid: str) -> Dict[str, Any]:
        # 获取加密参数
        content = requests.get("https://app.diandian.com/", headers=self.headers, cookies=self.cookies).text
        s = re.findall('u:\{s:"(.*?)"', content)[0]
        k = re.findall('u:\{.*?k:"(.*?)"', content)[0]
        l = re.findall('u:\{.*?l:"(.*?)"', content)[0]
        
        # 验证应用商店和地区
        market, region = self._validate_market_and_region(market, region)
        
        # 获取市场和国家信息
        market_info = markets.get(market)
        region_info = countries.get(region)
        
        # 生成请求参数
        params = {
            'market_id': f'{str(market_info['dd_market_id'])}',
            'id': f'{appid}',
            'country_id': f'{str(region_info['dd_country_id'])}',
            'language_id': '3'  # 默认语言ID，可根据需要调整
        }
        
        data = {
            's': s,
            'k': k,
            'l': l,
            'd': 0,
            'sort': 'dd',
            'num': 10
        }
        
        # 执行JS加密
        with open(self.js_path, 'r', encoding='utf-8') as f:
            js_code = f.read()
        js = execjs.compile(js_code)
        params['k'] = js.call('gen_detail_k', params, data)
        
        # 发送请求
        response = requests.get(
            'https://api.diandian.com/pc/app/v1/app/info',
            params=params,
            headers=self.headers,
            cookies=self.cookies
        )
        response.raise_for_status()
        app_info = response.json().get("data", {})
            
        return self._standardize_app_info(market,app_info)
    
    def _standardize_app_info(self, market,app_info: Dict[str, Any]) -> Dict[str, Any]:
        """标准化iOS应用信息"""
        # 安全处理screenshots字段
        screenshots = []
        if app_info.get("screenshots"):
            try:
                screenshots = app_info["screenshots"][0].get("list", [])
            except (IndexError, KeyError, AttributeError):
                pass
            
        return {
            "app_name": app_info.get("name", ""),
            "app_id": app_info.get("app_id", ""),
            "icon_url": app_info.get("logo", ""),
            "tags": app_info.get("genres", []),
            "developer": app_info.get("developer", "")["name"],
            "download_count": 0,
            "icp_number": "",
            "introduction": "",
            "bounde_id": app_info.get("bundle_id", ""),
            "rating": app_info.get("rating", 0.0),
            "rating_count": app_info.get("rating_count", 0),
            "screenshots": screenshots,
            "store": market,
            "update_time": app_info.get("last_release_time", ""),
            "version": app_info.get("version", ""),
            "download_url": app_info.get("download_url", ""),
            "region": app_info.get("country_id", ""),
            "dd_id": app_info.get("id", ""),
            "ft_id":random.randint(100000, 999999)
        }