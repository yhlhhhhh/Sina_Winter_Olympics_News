# 说明文档

---

## 简介

![image](https://github.com/yhlhhhhh/Sina_Winter_Olympics_News/blob/main/src%3Dhttp___www.zuowenku.net_Images_202109_16326457677012.thumb.jpg%26refer%3Dhttp___www.zuowenku.jpg)

这是一个能够爬取新浪网上有关冬奥会新闻并且进行数据分析以及可视化的程序。该程序会在运行时爬取当时新浪网搜索`冬奥`时的文章题目，并将所有文本进行分词，统计词频，最终根据词频生成一个HTML格式的词云。并且将爬取到的其他信息（例如：文章题目，发文时间，媒体名以及链接）输出为csv文件。

## 依赖库

1. jieba
2. pandas
3. BeautifulSoup
4. pyecharts
