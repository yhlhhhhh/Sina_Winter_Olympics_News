# -*- coding: utf-8 -*-
# 作者: 杨昊霖
# 作品名称: 新浪网冬奥新闻爬虫分析器
import os
import time
import requests
import datetime
from collections import Counter
try:
    import jieba
    import pandas as pd
    from bs4 import BeautifulSoup
    from pyecharts import options as opts
    from pyecharts.charts import WordCloud
    from pyecharts.globals import ThemeType
except ImportError:
    print('您有第三方库未安装, 请按照requirements.txt中的第三方库列表安装')
    exit()


class abstract:
    # 爬取搜索条目并保存到本地
    # Get all search items and save them locally
    ## request_method: get
    ## _IO output: HTML & CSS & JS, string, txt
    ### thread: url -> website_code_string -> txt
    def get_news_abstract():
        ### 爬虫
        url = 'https://search.sina.com.cn/?c=news&q=%E5%86%AC%E5%A5%A5&from=home&ie=utf-8'
        r = requests.get(url)
        ### 将页面代码写入txt文件并保存便于后面解析
        with open('pages.txt', 'w') as f:
            f.write(r.text)


class detail:
    # 处理爬取的条目, 遍历出所有条目URL
    # Process all items and traverse URL of all items
    ## _IO parameter data: input_type:: BeautifulSoup Object; Tag:: all_<h2>
    ## _IO output: url, string, list
    ### thread: BeautifulSoup Object -(loop)-> Tag:: <a> -> attribute href -(loop)-> list
    def get_url(data):
        return list(map(lambda i: i.a['href'], data))


    # 处理爬取的条目, 遍历出所有条目的报道媒体以及时间和日期
    # Process all items and traverse the reporting media, time and date of all items
    ## _IO parameter data: input_type:: BeautifulSoup Object; Tag:: all_<h2>
    ## _IO output: string, list (today:: length = 2; o:: length = 3), list
    ### thread: BeautifulSoup Object -(loop)-> Tag:: <span> -> lstrip -> rstrip -> split -(loop)-> list
    def get_media_time(data):
        return list(map(lambda i: str(i.span).lstrip('<span class="fgray_time">').rstrip('</span>').split(' '), data))


    # 处理爬取到的日期
    def process_date(data):
        date = []
        for i in data:
            if len(i) == 2:
                date.append(datetime.datetime.now().strftime('%Y-%m-%d'))
            else:
                date.append(i[1])
        return date


    # 处理爬取到的媒体名称
    def process_media(data):
        return list(map(lambda i: i[0], data))

    # 获取每篇文章的标题
    def get_title(link):
        r = requests.get(link)
        bs = BeautifulSoup(r.content)
        title = bs.title
        return str(title).lstrip('<title>').rstrip('</title>').split('|')[0]


# main
## 获取搜索摘要界面并处理存储到本地
abstract.get_news_abstract()

## 获取上级路径以方便后续存储操作
path = os.path.abspath('./')


## 获取并处理爬取信息
with open(f'{path}/pages.txt', 'r') as f:
    d = BeautifulSoup(f).find_all('h2')
    data = detail.get_media_time(d)
    date = detail.process_date(data)
    media = detail.process_media(data)
    url = detail.get_url(d)


## 获取每篇文章的标题
title_list = []
for i in url:
    title_list.append(detail.get_title(i))
    ### 延迟0.5秒, 防止被反爬虫机制发现
    time.sleep(0.5)


## 分词并统计词频
count_title = dict(Counter(jieba.cut(''.join(title_list)))).items()

## 画词云图并以html格式输出
result_title = (
    WordCloud(init_opts = opts.InitOpts(theme = ThemeType.LIGHT))
    .add('', count_title, word_size_range = [12, 55])
    .set_global_opts(title_opts = opts.TitleOpts(title = '新浪网有关冬奥标题词云'))
)
result_title.render(f'{path}/results/新浪网有关冬奥标题词云.html')

## 创建详情数据字典
data = {
    'title': title_list,
    'date': date,
    'media': media,
    'URL': url
}

## 将详情数据输出为Excel表格
pd.DataFrame(data).to_csv(f'{path}/results/details.csv')
