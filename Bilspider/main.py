import AI_Spider
import AI_Spider1
import os

# 失败品
"""
def Bil_Video_Spider():
    Keyword = input('请输入关键字：')
    Partition = input('请输入分区：')

    # 爬取某个区的数据
    for j in range(3, 4):
        # 爬取页数 [(j - 1) * 10 + 1, j * 10]
        START = (j - 1) * 10 + 1
        END = j * 10
        if j == 3:
            END += 3
        b_spider = AI_Spider.BilVideoSpider(Keyword)
        b_spider.video_run(START, END, Partition)

    
# work
Bil_Video_Spider()
# os.system("shutdown -s -t  60 ")
"""


def Bil_Video_Spider():

    keyword = input('请输入搜索关键字:')
    # partition = input('请输入搜索分区:')
    start = int(input('请输入开始爬取页数:'))
    end = int(input('请输入爬虫结束页面:'))
    for partition in tids:
        a = AI_Spider1.BilVideoSpider(keyword=keyword)
        a.run(partition=partition, start=start, end=end)


tids = ['知识','影视']
Bil_Video_Spider()
os.system("shutdown -s -t  60 ")
# tids = ['动画', '音乐', '舞蹈', '游戏', '知识', '科技', '运动', '生活', '时尚', '娱乐', '影视']
