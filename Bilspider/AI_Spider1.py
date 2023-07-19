import os
import re
import time
import random
import requests
import traceback
import pandas as pd
from lxml import etree
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options

"""
b站搜索 API: 
https://api.bilibili.com/x/web-interface/wbi/search/all/v2?page={}&page_size=42&keyword={}&tid={}
b站视频详情 API:
https://api.bilibili.com/x/web-interface/view?bvid={}
b站评论区详情 API:
https://api.bilibili.com/x/v2/reply/main?next={页数}&type=1&oid={av号}&mode={评论排序方式(1,2,3)}
3: 热度
2和: 时间排序
"""


def exception_capture(func):
    """
    装饰器
    :param func: 函数对象
    :return:
    """

    def work(*args, **kwargs):
        """
        捕捉异常并写入文件
        :param args: 位置参数
        :param kwargs: 关键字参数
        :return:
        """
        file = open("log.log", 'a', encoding='utf-8')
        try:
            res = func(*args, **kwargs)  # 调用函数
            return res
        except Exception as e:
            traceback.print_exc(limit=None, file=file)  # 捕捉异常
        file.close()

    return work


class BilVideoSpider(object):
    """
    爬虫类: 通过搜索, 对得到B站视频信息进行收集
    操作对象: 浏览器元素
    """
    tids = {'动画': 1,
            '音乐': 3,
            '舞蹈': 129,
            '游戏': 4,
            '知识': 36,
            '科技': 188,
            '运动': 234,
            '生活': 160,
            '时尚': 155,
            '娱乐': 5,
            '影视': 181,
            '全部': 0}

    # log 文件
    file = open("log.log", 'a', encoding='utf-8')

    @exception_capture
    def __init__(self, keyword: str) -> None:
        self.keyword = keyword

        # 储存所有 信息
        self.total_target = {}
        self.list_title = []
        self.list_date = []
        self.list_playback_volume = []
        self.list_barrage_counts = []
        self.list_like_counts = []
        self.list_coin_counts = []
        self.list_favorite_counts = []
        self.list_share_counts = []
        self.list_tag = []

    # 获取 search_html
    @exception_capture
    def get_search_html(self, url: str) -> str:
        # 创建ChromeOptions对象
        options = Options()

        # 设置headless模式（隐藏浏览器）
        options.add_argument('--headless')

        # 隐藏 侦听信息
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        # 创建一个Chrome WebDriver实例
        driver = webdriver.Chrome(
            executable_path='<path-to-chrome>', options=options)

        # 打开网页
        driver.get(url)

        # 刷新网页
        driver.refresh()
        time.sleep(random.randint(4, 6))

        # 获取网页的HTML
        html_str = driver.page_source

        # 关闭WebDriver
        driver.quit()
        print('*'*40)

        return html_str

    # 解析 search_html 获取 sub_url
    @exception_capture
    def parse_search_html(self, html_str: str) -> list:
        # 创建 lxml 解析对象
        parse_html = etree.HTML(html_str)

        # 提取目标元素
        e_list = parse_html.xpath(
            '//div[@class="bili-video-card__wrap __scale-wrap"]/a/@href')

        # 修饰目标元素
        sub_url_list = []
        for i in e_list:
            sub_url_list.append(r'https:' + i)

        print('本次解析获取{}条视频链接'.format(len(sub_url_list)))
        return sub_url_list

    # 请求 sub_url 函数
    @exception_capture
    def get_sub_url(self, sub_url: str) -> str:
        # 随机产生用户代理
        UA = UserAgent()
        ua = UA.Chrome
        headers = {'UserAgent': str(ua)}

        # 使用 requests 模块得到响应对象
        response = requests.get(sub_url, headers=headers, verify=True)
        # 更改编码格式
        response.encoding = 'utf-8'
        # 得到 html 文件
        html = response.text

        return html

    # 解析 parse_sub_html
    @exception_capture
    def parse_sub_html(self, html: str) -> None:
        list_tag_tmp = []

        pattern_share = re.compile(r'收藏人数.*?、转发人数 (.*?), 视频作者', re.S)
        self.list_share_counts.append(pattern_share.findall(html)[0])

        html = etree.HTML(html)

        self.list_title.extend(html.xpath(
            '//div[@id="viewbox_report"]/h1/@title'))
        self.list_date.extend(html.xpath(
            '//span[@class="pudate-ip item"]/span[@class="pudate"]/@title'))
        self.list_playback_volume.extend(html.xpath(
            '//div[@class="video-data-list"]/span[@class="view item"]/@title'))
        self.list_barrage_counts.extend(html.xpath(
            '//div[@class="video-data-list"]/span[@class="dm item"]/@title'))
        self.list_like_counts.extend(html.xpath(
            '//span[@class="like"]/span[@class="info-text"]/text()'))
        self.list_coin_counts.extend(html.xpath(
            '//span[@class="coin"]/span[@class="info-text"]/text()'))
        self.list_favorite_counts.extend(html.xpath(
            '//span[@class="collect"]/span[@class="info-text"]/text()'))
        list_tag_tmp.extend(html.xpath(
            '//a[@aria-labelby="new_channel"]/text()'))
        list_tag_tmp.extend(html.xpath('//a[@class="tag-link"]/text()'))
        self.list_tag.append(list_tag_tmp)

    # 保存数据
    @exception_capture
    def save_data(self, filename: str) -> None:
        if filename != '全部':
            filepath = 'DATA/{}区.csv'.format(filename)
        else:
            filepath = 'DATA/全部分区({}).csv'.format(self.keyword)

        print('*'*20, '打印各个字段的数量', '*'*20)
        print('标题: ', len(self.list_title))
        print('日期: ', len(self.list_date))
        print('播放量: ', len(self.list_playback_volume))
        print('弹幕量: ', len(self.list_barrage_counts))
        print('点赞数: ', len(self.list_like_counts))
        print('投硬币数: ', len(self.list_coin_counts))
        print('收藏人数: ', len(self.list_favorite_counts))
        print('分享数: ', len(self.list_share_counts))
        print('标签: ', len(self.list_tag))

        if len(self.list_share_counts) != len(self.list_tag):
            self.file.write("信息数量不匹配, 跳过本次写入")
            return None

        df = pd.DataFrame(self.total_target)

        if not os.path.exists(filepath):
            # 将DataFrame写入csv文件
            df.to_csv(filepath, header=True, index=False, encoding='utf_8_sig')
        else:
            # 将要追加的数据追加到已存在的csv文件中
            df.to_csv('existing.csv', mode='a', header=False,
                      index=False, encoding='utf_8_sig')

    # 爬虫启动
    @exception_capture
    def run(self, partition: str, start: int, end: int) -> None:
        start_time = time.time()

        tid = self.tids[partition]    # 获取分区id
        sub_url_lists = []     # 存储所有 sub_url

        # 解析 search_url
        for page in range(start, end + 1):
            print('开始解析第{}页'.format(page))
            search_url = r'https://search.bilibili.com/video?&keyword={}&tids={}&page={}&o={}'.format(
                self.keyword, tid, page, 30 * (page - 1))

            sub_url_list = self.parse_search_html(
                self.get_search_html(search_url))
            sub_url_lists.extend(sub_url_list)

            print('池中共{}条视频链接'.format(len(sub_url_lists)))
            time.sleep(random.randint(2, 4))

        print('*'*40)

        # 解析 sub_url
        counts = 0
        for sub_url in sub_url_lists:
            counts += 1
            self.parse_sub_html(self.get_sub_url(sub_url))
            if counts % 10 == 0:
                time.sleep(random.randint(2, 4))
            else:
                time.sleep(random.randint(1, 3))
            print('解析第{}条视频链接'.format(counts))

        self.total_target['标题'] = self.list_title
        self.total_target['日期'] = self.list_date
        self.total_target['播放量'] = self.list_playback_volume
        self.total_target['弹幕量'] = self.list_barrage_counts
        self.total_target['点赞数'] = self.list_like_counts
        self.total_target['投硬币数'] = self.list_coin_counts
        self.total_target['收藏人数'] = self.list_favorite_counts
        self.total_target['分享数'] = self.list_share_counts
        self.total_target['标签'] = self.list_tag

        self.save_data(filename=partition)
        print('*'*40)
        end_time = time.time()
        run_time = end_time - start_time
        print('恭喜您，数据保存成功, 程序共运行{}秒'.format(run_time))


if __name__ == '__main__':
    # a test demon
    '''
    keyword = input('请输入搜索关键字:')
    partition = input('请输入搜索分区：')
    start = int(input('请输入开始爬取页数:'))
    end = int(input('请输入爬虫结束页面:'))
    a = BilVideoSpider(keyword=keyword)
    a.run(partition=partition, start=start, end=end)
    '''

    '''
    输入 关键字 分区 页数
    拼接 url
    解析 url
    收集 sub_url
    解析 sub_url
    保存 信息
    '''
