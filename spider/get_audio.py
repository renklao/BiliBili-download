"""
获取视频页面的audio网址
后续优化考虑 异步 处理音频/视频的地址获取
"""
from lxml import html
import json
import re
import requests
from spider.info import cookies,headers,params  #这里因为app中要用这条语句 所以要相对于根路径进行导入

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


def get_audio_url(url:str) -> str:
    response = requests.get(url, params=params, cookies=cookies, headers=headers)

    #进一步精准定位
    tree = html.fromstring(response.text)    #将字符串转换为html格式
    try:
        text = tree.xpath('//script[contains(text(), "window.__playinfo__")]/text()')[0]
    except IndexError:
        return "无法获取视频 可能是因为是直播视频 请点击其他视频"

    pattern=r'("audio":.*?),"dolby"'        #找音频是audio 视频改成video即可
    result=re.search(pattern,text)
    file=json.loads("{"+result.group(1)+"}") #获得video和audio的json字符串

    audio_url="未找到对应的音频地址" #默认为该字符串
    audio_url=file["audio"][0]["baseUrl"]

    return audio_url



if __name__=="__main__":
    #url=input("请输入网址:")
    url="https://upos-sz-estgoss.bilivideo.com/upgcxcode/31/77/1604757731/1604757731_sr1-1-100035.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&oi=242113220&mid=443936770&deadline=1752923747&uipk=5&gen=playurlv3&os=upos&trid=e894621358e74b6dafa837bcc7cc365p&nbs=1&platform=pc&og=cos&upsig=258c5f3ac02f97197df5deac78bf8672&uparams=e,oi,mid,deadline,uipk,gen,os,trid,nbs,platform,og&bvc=vod&nettype=0&bw=7279654&agrr=1&buvid=142F644F-F85D-0A86-005B-DA128702DFA925164infoc&build=0&dl=0&f=p_0_0&orderid=0,4"
    # 流式下载
    response = requests.get(url, headers=headers, cookies=cookies, stream=True)
    print(response.status_code)