import requests
import re
import pandas as pd
import traceback
import random
import time
import os
from fake_useragent import UserAgent


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
            func(*args, **kwargs)  # 调用函数
        except Exception as e:
            traceback.print_exc(limit=None, file=file)  # 捕捉异常
        file.close()

    return work


class BilVideoSpider(object):
    """
    爬虫类: 通过搜索, 对得到B站视频信息进行收集
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

    # 随机产生用户代理
    UA = UserAgent()
    ua = UA.Chrome
    headers = {'UserAgent': str(ua)}

    file = open("log.log", 'a', encoding='utf-8')

    # 初始化 URL 属性
    @exception_capture
    def __init__(self, keywords: str) -> None:

        self.keyword = keywords
        self.url = ''

    # 1.请求函数
    @exception_capture
    def get_html(self) -> str:
        # 使用 requests 模块得到响应对象
        response = requests.get(self.url, headers=self.headers, verify=True)
        # 更改编码格式
        response.encoding = 'utf-8'
        # 得到 html 文件
        html = response.text

        return html

    # 2.解析函数
    @exception_capture
    def parse_html(self) -> dict:
        # 创建正则表达式对象
        text = self.get_html()
        pattern_type = re.compile(
            r'<span class="type hide">(.*?)</span>', re.S)
        pattern_title = re.compile(
            r'<a title="(.*?)" href=".*?" target="_blank" class="title">', re.S)
        pattern_link = re.compile(
            r'<a title=".*?" href="//(.*?)" target="_blank" class="title">', re.S)
        sub_url = ['https://' + x for x in pattern_link.findall(text)]

        target = {'类型': pattern_type.findall(text),
                  '标题': pattern_title.findall(text),
                  'sub_url': sub_url}

        return target

    # 3.子请求函数
    @exception_capture
    def get_sub_html(self, parse_counts: int) -> list:
        list_html = []
        target = self.parse_html()
        i = 0
        # 提取 sub_html
        for sub_url in target['sub_url']:
            # 使用 requests 模块得到响应对象
            response = requests.get(sub_url, headers=self.headers, verify=True)
            # 更改编码格式
            response.encoding = 'utf-8'
            # 得到 html 文件
            list_html.append(response.text)
            time.sleep(random.randint(1, 2))
            i += 1
            print('第{}条response'.format(20 * (parse_counts - 1) + i))

        return list_html

    # 4.子解析函数
    @exception_capture
    def parse_sub_html(self, extract_counts: int) -> dict:
        list_date = []
        list_playback_volume = []
        list_barrage_counts = []
        list_like_counts = []
        list_coin_counts = []
        list_favorite_counts = []
        list_share_counts = []
        list_tag = []
        total_target = self.parse_html()
        list_html = self.get_sub_html(extract_counts)
        # 删除 sub_link
        print(total_target['sub_url'])
        del total_target['sub_url']

        i = 0
        # 提取关键内容
        for sub_html in list_html:
            # 创建模式
            pattern_date = re.compile(
                r'<span class="pudate-text">\n(.*?)</span>', re.S)
            pattern_playback = re.compile(r'视频播放量 (.*?)、弹幕量', re.S)
            pattern_barrage = re.compile(r'视频播放量.*?、弹幕量 (.*?)、点赞数', re.S)
            pattern_like = re.compile(r'弹幕量.*?、点赞数 (.*?)、投硬币枚数', re.S)
            pattern_coin = re.compile(r'点赞数.*?、投硬币枚数 (.*?)、收藏人数', re.S)
            pattern_favorite = re.compile(r'投硬币枚数.*?、收藏人数 (.*?)、转发人数', re.S)
            pattern_share = re.compile(r'收藏人数.*?、转发人数 (.*?), 视频作者', re.S)
            pattern_key_tag = re.compile(r'class="tag-link">.*?aria-labelby="new_channel".*?</path></svg>(.*?)</a>',
                                         re.S)
            pattern_tag = re.compile(
                r'from_source=video_tag" target="_blank" class="tag-link">(.*?)</a>', re.S)
            # 加入 list
            list_date.append(pattern_date.findall(sub_html))
            list_playback_volume.append(pattern_playback.findall(sub_html))
            list_barrage_counts.append(pattern_barrage.findall(sub_html))
            list_like_counts.append(pattern_like.findall(sub_html))
            list_coin_counts.append(pattern_coin.findall(sub_html))
            list_favorite_counts.append(pattern_favorite.findall(sub_html))
            list_share_counts.append(pattern_share.findall(sub_html))
            list_tag.append(pattern_tag.findall(sub_html) +
                            (pattern_key_tag.findall(sub_html)))

            i += 1
            print('第{}条提取'.format(20 * (extract_counts - 1) + i))

        time.sleep(random.randint(4, 6))
        # 加入数据字典
        total_target['日期'] = list_date
        total_target['播放量'] = list_playback_volume
        total_target['弹幕量'] = list_barrage_counts
        total_target['点赞数'] = list_like_counts
        total_target['投硬币数'] = list_coin_counts
        total_target['收藏人数'] = list_favorite_counts
        total_target['分享数'] = list_share_counts
        total_target['标签'] = list_tag
        return total_target

    # 5.保存文件函数
    @exception_capture
    def save_data(self, DATA: pd.DataFrame, filename: str) -> None:
        if filename != '全部':
            filename = 'DATA/{}区.csv'.format(filename)
        else:
            filename = 'DATA/全部分区({}).csv'.format(self.keyword)

        size = os.path.getsize(filename)
        if size != 0:
            DATA_csv = pd.read_csv(filename)
            DATA = pd.concat([DATA_csv, DATA], axis=0)

        DATA.to_csv(filename, index=False, encoding='utf_8_sig')

    # 6.入口函数
    @exception_capture
    def video_run(self, start: int, end: int, partition: str) -> None:
        data = pd.DataFrame()

        # 开始爬取
        for page in range(start, start + 2):
            print('加载第{}页\n'.format(page))
            self.url = r'https://search.bilibili.com/video?&keyword={}&tids={}&page={}&o={}'.format(
                self.keyword, self.tids[partition], page, 30 * (page - 1))
            print(self.url)
            data = pd.concat(
                [data, pd.DataFrame(self.parse_sub_html(page))], axis=0)
            data = data.reset_index(drop=True)
            if page % 5 == 0:
                time.sleep(random.randint(10, 20))

        self.save_data(data, partition)


# 以脚本的形式启动爬虫
if __name__ == '__main__':
    pass
    # a B_Spider demo
    '''
    Keyword = input('请输入关键字：')
    Partition = input('请输入分区：')
    b_spider = BilVideoSpider(Keyword)

    # 爬取某个区的数据
    for j in range(1, 2):
        # 爬取页数 [(j - 1) * 10 + 1, j]
        START = (j - 1) * 10 + 1
        END = j * 1
        b_spider.video_run(START, END, Partition)
    '''
