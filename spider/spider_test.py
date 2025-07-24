"""
该文件是爬虫程序的主入口
"""
from spider.get_audio import get_audio_url
from spider.get_url import search_keyword
import time

if __name__=="__main__":
    keyword = input("请输入关键词：")
    start_time = time.time()  # 记录开始时间

    #先获取搜索页面的所有信息
    datas=search_keyword(keyword)

    #先取一组
    url=datas["urls"][1]
    title=datas["titles"][1]
    picture=datas["pictures"][1]

    mid_time=time.time()
    print(f"程序第一阶段耗时：{mid_time - start_time:.2f}秒")

    #获得目标音频文件
    audio_url=get_audio_url(url)
    print(audio_url)

    end_time = time.time()  # 记录结束时间
    print(f"程序第二阶段耗时：{end_time - mid_time:.2f}秒")