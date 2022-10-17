import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from pyquery import PyQuery as Pq

from config.__init__ import read_conf
from db.RankGoods import RankGoods, RankHistory


class BidCrawl(object):
    """
    BidCrawl
    """
    def change_address(self, driver, value):
        while True:
            try:
                driver.find_element_by_id('glow-ingress-line1').click()
                time.sleep(2)
            except Exception as e:
                print("get glow-ingress-line1 id fail!!!,retry", e)
                driver.refresh()
                time.sleep(5)
                continue
            try:
                driver.find_element_by_id("GLUXChangePostalCodeLink").click()
                time.sleep(2)
            except:
                print("get GLUXChangePostalCodeLink id fail!!!")
                pass
            try:
                driver.find_element_by_id('GLUXZipUpdateInput').send_keys(value)
                time.sleep(1)
                break
            except:
                driver.refresh()
                time.sleep(10)
                continue
        driver.find_element_by_id('GLUXZipUpdate').click()
        time.sleep(1)
        driver.refresh()
        time.sleep(3)

    def parse_detail(self, page_source, page_index, keyword, global_split_list):
        print(keyword)
        global write_row_index

        finish = False
        doc = Pq(page_source)
        # 判断是否为最后一页，最后一页就停止往下获取
        last = doc('.a-disabled.a-last').text()
        if last.strip() != "":
            finish = True
        print("last text = ", last, " finish = ", finish)
        # 获取商品所有信息
        main_list = doc('.s-main-slot.s-result-list.s-search-results.sg-row')
        par_list = main_list.children().items()
        normal_count = 0
        for child in par_list:
            # flag_text为空的表示非正常商品链接
            flag_text = child.attr('data-asin')
            position = child.attr('data-index')
            if flag_text.strip() == "":
                continue
            normal_count += 1
            # asin_id
            AsinId = flag_text
            # 是否为广告
            sponsor = child('.s-label-popover-default .a-color-secondary').text()
            # 标题
            title = child('.a-size-base-plus.a-color-base.a-text-normal').text()
            # 价格，但是会有打折价格，所以多个价格只选第一个
            price_list = child('.a-price .a-offscreen').text().split(" ")
            price = price_list[0]
            # 当前商品位置
            cur_pos = str(page_index) + "-" + str(normal_count)
            # 评论数
            review_num = child('.a-section.a-spacing-none.a-spacing-top-micro .a-row.a-size-small .a-size-base').text()
            # 评分
            level = child('.a-icon-alt').text()
            # 配送地址
            adds = child(
                '.a-row.a-size-base.a-color-secondary.s-align-children-center .a-size-small.a-color-secondary').text()
            data_list = []
            for val in global_split_list:
                if val == "标题":
                    data_list.append(title)
                if val == '页面位置':
                    data_list.append(position)
                elif val == "AsinId":
                    data_list.append(AsinId)
                elif val == "价格":
                    data_list.append(price)
                elif val == "广告":
                    data_list.append(sponsor)
                elif val == "自然位置":
                    data_list.append(cur_pos)
                elif val == "评论数":
                    data_list.append(review_num)
                elif val == "评分":
                    data_list.append(level)
                elif val == "配送地址":
                    data_list.append(adds)
            print(f"current keyword is {keyword} ----- {title}, {position}, {AsinId}, {price}, {sponsor}, {cur_pos}, {level}, {review_num}, {adds}")
            if normal_count >= 3:
                break
            asinId = read_conf(conf_type='amasins')['asinid']
            asin_rank_one = RankGoods.select(RankGoods.id, RankGoods.asin_id).filter(
                RankGoods.asin_id == asinId).first()
            # 查询库中是否已有当前asin
            # 无次asin 则新增
            main_url = "https://www.amazon.com/dp/"
            if not asin_rank_one:
                asin_rank_one = RankGoods()
                asin_rank_one.title = title
                asin_rank_one.price = price
                asin_rank_one.asin_id = AsinId
                asin_rank_one.is_sponsor = True if sponsor != '' else False
                asin_rank_one.score = level
                asin_rank_one.comment_count = review_num
                asin_rank_one.url = f"{main_url}{asinId}"
                asin_rank_one.save()
                # 第一次跑 没有这个asin 先存asin 再存排名记录 asin和其排名历史 是one_to_all
                rank_history_one = RankHistory()
                rank_history_one.rank_good_id = asin_rank_one.id
                rank_history_one.page_num = cur_pos
                rank_history_one.last_page_num = 0
                rank_history_one.keyword = keyword
                rank_history_one.bid_price = 0
                rank_history_one.total = 1
                rank_history_one.is_sponsor = True if sponsor != '' else False
                rank_history_one.check_time = time.strftime("end %Y-%m-%d %H:%M:%S", time.localtime())
                rank_history_one.save()
                return finish
            else:
                # 存在这个asin 继续往下走
                # 对某个asin进行排行历史查询
                cur_rank_history_one = RankHistory. \
                    select(RankHistory.id,
                           RankHistory.keyword,
                           RankHistory.last_page_num,
                           RankHistory.page_num,
                           RankHistory.bid_price,
                           RankHistory.total). \
                    filter(RankHistory.rank_good_id == asin_rank_one.id,
                           RankHistory.keyword == keyword).order_by(RankHistory.id.desc()).first()
                # print(cur_rank_history_one._to_dict())
                # 没有相应记录(一般是第一次) 则新增一条
                rank_history_one = RankHistory()
                rank_history_one.rank_good_id = asin_rank_one.id
                rank_history_one.total = cur_rank_history_one.total + 1
                rank_history_one.last_page_num = cur_rank_history_one.page_num
                if not rank_history_one:
                    rank_history_one.total = 1
                    rank_history_one.last_page_num = 0
                rank_history_one.page_num = cur_pos
                rank_history_one.keyword = keyword
                rank_history_one.bid_price = 0
                rank_history_one.is_sponsor = True if sponsor != '' else False
                rank_history_one.check_time = time.strftime("end %Y-%m-%d %H:%M:%S", time.localtime())
                rank_history_one.save()
                return finish

    def get_keywords(self):
        """
        get keywords
        :return:
        """
        keywords = ['broadlink smart switch']
        return keywords

    def start_crawl(self):
        # 配送地址
        global_adds_list = []
        # 筛选信息
        global_split_list = []
        # 获取关键词
        global_key_list = self.get_keywords()
        print("global_key_list = ", global_key_list)
        if len(global_split_list) <= 0:
            global_split_list = ['标题', 'AsinId', '页面位置', '价格', '广告', '自然位置', '评论数', '评分']

        # 设置get直接返回，不再等待界面加载完成
        desired_capabilities = DesiredCapabilities.CHROME
        desired_capabilities["pageLoadStrategy"] = "none"
        chrome_options = webdriver.ChromeOptions()
        # 无窗口模式
        chrome_options.add_argument('--headless')
        # 禁止硬件加速，避免严重占用cpu
        chrome_options.add_argument('--disable-gpu')
        # 关闭安全策略
        chrome_options.add_argument("disable-web-security")
        # 禁止图片加载
        chrome_options.add_experimental_option('prefs', {'profile.managed_default_content_settings.images': 2})
        # 隐藏Chrome正在受到自动软件的控制
        chrome_options.add_argument('disable-infobars')
        # no sandbox
        chrome_options.add_argument('--no-sandbox')
        # 设置开发者模式启动，该模式下webdriver属性为正常值
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 模拟移动设备
        chrome_options.add_argument(
            'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"')
        driver = webdriver.Chrome(options=chrome_options, executable_path=read_conf(conf_type='driver_path')['path'])
        # 返回驱动等待的变量
        wait = WebDriverWait(driver, 20)
        # driver.maximize_window()

        print(time.strftime("start %Y-%m-%d %H:%M:%S", time.localtime()))
        search_url = 'https://www.amazon.com/'
        if len(global_adds_list) >= 1:
            driver.get(search_url)
            time.sleep(3)
            self.change_address(driver, global_adds_list[0])

        # 固定搜索内容，变化的只有页面
        search_page_url = 'https://www.amazon.com/s?k={}&page={}'
        for key in global_key_list:
            for i in range(1, 2):
                # 爬取页数限制
                print("正在爬取", search_page_url.format(key, i))
                driver.get(search_page_url.format(key, i))
                time.sleep(3)
                # css选择器，返回结果存在跳出，异常报错
                try:
                    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "div.s-result-list")))
                    isEnd = self.parse_detail(driver.page_source, i, key, global_split_list)
                    if isEnd:
                        break
                except:
                    print("url: " + search_page_url.format(i) + "获取失败")
                    pass
        print(time.strftime("end %Y-%m-%d %H:%M:%S", time.localtime()))
        driver.quit()
