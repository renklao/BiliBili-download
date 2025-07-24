#获取VIP视频
import json
import re
import requests
from lxml import html
from spider.info import cookies,headers,params


def get_text(url:str):
    response = requests.get(url, params=params, cookies=cookies, headers=headers)
    input(response.text)
    # 进一步精准定位
    tree = html.fromstring(response.text)  # 将字符串转换为html格式
    # VIP视频html中的url存在位置与普通视频不一样
    try:
        text = tree.xpath('//script[contains(text(), "playurlSSRData")]/text()')[0]
        return text
    except IndexError:
        return "资源获取出错"


def get_vip_video_and_audio_url(url:str):
    text=get_text(url)
    #获取视频url
    pattern = r'("video":.*?),"audio"'  # 找音频是audio 视频改成video即可
    result = re.search(pattern, text)
    file = json.loads("{" + result.group(1) + "}")  # 获得video的json字符串
    video_url=file["video"][0]["base_url"]

    #获取音频url
    pattern = r'("audio":.*?),"dolby"'
    result = re.search(pattern, text)
    file = json.loads("{" + result.group(1) + "}")  # 获得video的json字符串
    audio_url = file["audio"][0]["base_url"]

    return video_url,audio_url

if __name__=="__main__":
    url='https://www.bilibili.com/video/BV1Gc411V7HC'
    get_vip_video_and_audio_url(url)
