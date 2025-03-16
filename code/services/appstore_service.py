from scrapers import DiandianScraper, QimaiScraper, MarketScraper

class AppStoreService:
    def __init__(self):
        self.scrapers = {
            "diandian": DiandianScraper(),
            "qimai": QimaiScraper()
        }

    def search(self, market, region, keyword, page, pagesize, sp="diandian"):
        """
        执行搜索逻辑
        :param market: 应用市场
        :param region: 地区
        :param keyword: 关键词
        :param page: 页码
        :param pagesize: 每页大小
        :param scraper_type: 抓取器类型，默认为 "diandian"  # 修改参数说明
        :return: 搜索结果
        """
        # 获取抓取器实例
        scraper = self.scrapers.get(sp)  # 修改变量名
        if not scraper:
            scraper = MarketScraper(market)  # 修改类名

        # 调用抓取器搜索方法
        return scraper.search(market, region, keyword, page, pagesize)

    def detail(self, market, region, appid, scraper_type="diandian"):
        """
        获取应用详情
        :param market: 应用市场
        :param region: 地区
        :param appid: 应用ID
        :param scraper_type: 抓取器类型，默认为 "diandian"  # 修改参数说明
        :return: 应用详情
        """
        # 获取抓取器实例
        scraper = self.scrapers.get(scraper_type)  # 修改变量名
        if not scraper:
            scraper = MarketScraper(market)  # 修改类名

        # 调用抓取器详情方法
        return scraper.detail(market, region, appid)