"""
用于获取关键词对应的多个标题和urls 以及图片和时长信息
处理的是搜索页面的html
"""
import requests
from lxml import html
from spider.info import cookies,headers,params

#关键词搜索返回目标网址
def search_keyword(keyword:str) -> dict:
    url_search=f"https://search.bilibili.com/all?keyword={keyword}"
    response_inside=requests.get(url_search,params=params, cookies=cookies, headers=headers)
    tree = html.fromstring(response_inside.text)    #将字符串转换为html格式

    """每条视频对应的标题"""
    titles = tree.xpath('(//h3[contains(@class, "bili-video-card__info--tit")]/@title)[position() <= 10]') #"默认获取前面十条"

    """获得的均为相对网址 注意进行拼接!"""
    "跳转的url 因为获取到的都是相对的网址 因此在前面加上https:"
    original_urls=tree.xpath('(//h3[contains(@class, "bili-video-card__info--tit")]/../@href)[position() <= 10]')
    urls = [f"https:{url}" for url in original_urls]

    "图片url 与上同理"
    # original_pictures=tree.xpath('(//picture[contains(@class,"v-img bili-video-card__cover")]/source/@srcset)[position() <= 10]')
    # pictures=[f"https:{picture}" for picture in original_pictures]

    "获取视频的时长"
    #durations=tree.xpath("(//span[contains(@class,'bili-video-card__stats__duration')]/text())[position() <= 10]")

    return {
        "titles":titles,
        "urls":urls,
    }


if __name__=="__main__":
    search_keyword("2")