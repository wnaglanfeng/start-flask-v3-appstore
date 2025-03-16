import pickle
import requests
import execjs
import re
import os
import time

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

    def search(self, market, region, keyword, page, pagesize):
        # 验证应用商店和地区
        market, region = self._validate_market_and_region(market, region)
        
        # 获取对应的 dd_market_id
        from config.market import markets
        market_info = markets.get(market)
        if not market_info or 'dd_market_id' not in market_info:
            raise ValueError(f"Invalid market or missing dd_market_id: {market}")

        dd_market_id = market_info['dd_market_id']
        # 如果部分地区可用，
 
        # 获取对应的 dd_region_id
        from config.country import countries
        region_info = countries.get(region)
        if not region_info or 'dd_country_id' not in region_info:
            raise ValueError(f"Invalid region or missing dd_country_id: {region}")
        dd_country_id = region_info['dd_country_id']
        # 根据 type 设置 system_type
        system_type = '4' if market_info['type'] == 'ios' else ''
    
    
    
        with open(self.js_path, 'r', encoding='utf-8') as f:
            js_code = f.read()
        js = execjs.compile(js_code)

        content = requests.get("https://app.diandian.com/", headers=self.headers, cookies=self.cookies).text
        s = re.findall('u:\{s:"(.*?)"', content)[0]
        k = re.findall('u:\{.*?k:"(.*?)"', content)[0]
        l = re.findall('u:\{.*?l:"(.*?)"', content)[0]

        current_time = int(time.time())
        compare_time = current_time - (current_time % 86400) - 86400
        #IOS 可以过
        params1 = {
            'market_id': '1',
            'country_id': '75',
            'word': '%E5%BF%AB%E6%89%8B',
            'device_id': '',
            'system_type': '4',
            'time': '1742070143',
            'compare_time': '1741968000',
            'result_type': '',
            'payment_type': '',
            'page': '1',
            'page_size': '20',
            'width_google_other_data': '0',
            'market_type': '0'
        }
        #国内 Android 可以过
        params = {
            'market_id': f'{dd_market_id}',
            'country_id': f'{dd_country_id}',
            'word': requests.utils.quote(keyword),
            'device_id': '',
            'system_type': system_type,
            'time': str(current_time),
            'compare_time':str(compare_time),
            'result_type': '',
            'payment_type': '',
            'page': f'{page}',
            'page_size': f'{pagesize}',
            'width_google_other_data': '0',
            'market_type': '0' if market == 'ios' else '-1'
        }
        for key in params1:
            if params1[key] != params.get(key):
                print(f"键 {key} 不同: params1={params1[key]}, params2={params.get(key)}")
                
        data = {
            's': s,
            'k': k,
            'l': l,
            'd': 0,
            'sort': 'dd',
            'num': 10
        }
        params['k'] = js.call('gen_search_k', params, data)
        response = requests.get('https://api.diandian.com/pc/app/v2/word/search', params=params, headers=self.headers, cookies=self.cookies)
        return response.json()

    def detail(self, market, region, appid):
        # 实现点点平台的详情逻辑
        pass
