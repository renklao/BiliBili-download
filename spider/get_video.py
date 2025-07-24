"""有个问题 ： """

from lxml import html
import json
import re
import requests
from spider.info import cookies,headers,params

#返回状态码并且下载文件到本地
def get_status_code_or_download(url: str) -> int: #返回状态码
    response_inside=requests.get(url, params=params, cookies=cookies, headers=headers)
    if response_inside.status_code==200:
        #决定是否要下载
        """with open("music.m4a","wb") as f:
            f.write(response_inside.content)"""
        return 200
    else:
        return response_inside.status_code

def get_video_url(url:str) -> str:
    response = requests.get(url, params=params, cookies=cookies, headers=headers)

    #进一步精准定位
    tree = html.fromstring(response.text)    #将字符串转换为html格式
    try:
        text = tree.xpath('//script[contains(text(), "window.__playinfo__")]/text()')[0]
    except IndexError:
        return "无法获取视频 可能是因为是直播视频 请点击其他视频"

    pattern=r'("video":.*?),"audio"'        #找音频是audio 视频改成video即可
    result=re.search(pattern,text)
    file=json.loads("{"+result.group(1)+"}") #获得video和video的json字符串

    video_url="未找到对应的音频地址" #默认为该字符串
    video_url=file["video"][0]["baseUrl"]
    #取得视频并且下载

    return video_url



if __name__=="__main__":
    url=input("请输入网址:")
    # url='https://upos-sz-302ppio.bilivideo.com/upgcxcode/95/75/1610537595/1610537595_sr1-1-100035.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&oi=1912152734&trid=4abbba695cbb445d950d902e25c5efep&mid=443936770&uipk=5&platform=pc&gen=playurlv3&os=upos&og=hw&deadline=1753266654&nbs=1&upsig=2cc5839de2814400832a630259f278bd&uparams=e,oi,trid,mid,uipk,platform,gen,os,og,deadline,nbs&bvc=vod&nettype=0&bw=6718617&agrr=1&buvid=142F644F-F85D-0A86-005B-DA128702DFA925164infoc&build=0&dl=0&f=p_0_0&orderid=0,4'
    # resp = requests.get(url, params=params, cookies=cookies, headers=headers, stream=True)
    # print(resp.status_code)
    #
    # if resp.status_code == 200:
    #     with open('1.m4s', 'wb') as f:  # 建议保存为 .m4s 扩展名
    #         for chunk in resp.iter_content(chunk_size=1024 * 1024):  # 分块下载，避免内存占用过高
    #             f.write(chunk)
    #     print("下载完成")
    # else:
    #     print(f"下载失败，状态码：{resp.status_code}")