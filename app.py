import requests
from flask import Flask, render_template, request, session, Response
from spider.get_audio import get_audio_url
from spider.get_url import search_keyword
from spider.get_video import get_video_url
from spider.get_vip import get_vip_video_and_audio_url
from spider.info import cookies, params, headers

# 代理接口通过代理绕过防盗链 url为要获取的目标音频/视频
def proxy_bilibili(target_url:str):
    if not target_url:
        return "Error: Missing 'url' parameter", 400  # 返回错误信息

    # 3. 转发请求到目标URL（stream=True表示流式传输，适合大文件如视频）
    resp = requests.get(target_url, headers=headers, params=params ,cookies=cookies ,stream=True)

    # 构造响应头（覆盖或新增关键头）
    head = {
        'Content-Type': resp.headers.get('Content-Type', 'application/octet-stream'),
        'Content-Length': resp.headers.get('Content-Length'),
        'Content-Disposition': f'attachment; filename="audio.m4a"',  # 强制下载并指定文件名
        'Access-Control-Allow-Origin': '*'  # 允许跨域
    }

    # 4. 返回目标URL的响应（保持原始状态码和Headers）
    return Response(
        resp.iter_content(chunk_size=8192),  # 流式传输（避免内存爆炸）
        status=resp.status_code,             # 返回原始状态码（如200）
        headers=head                      # 传递原始Headers（如Content-Type）
    )

app = Flask(__name__)
app.secret_key = 'dev-secret-key-123!'  # 设置 secret_key（生产环境要用更安全的值
# 首页路由
@app.route('/')
def home():
    return render_template('home.html')


# 目标页面路由 包含 搜索 功能
@app.route('/my_bilibili')
def my_bilibili():
    return render_template('my_bilibili.html')


# 显示 搜索 得到的信息 用户可以选择是否下载
@app.route('/my_bilibili/search')
def search():
    #获取前端传进来的关键词
    keyword=request.args.get('keyword')

    if not keyword:
        return "未检测到输入信息 请重新输入"

    datas=search_keyword(keyword)  # 获得的是一个包含多个列表的字典

    titles=datas["titles"]
    urls=datas["urls"]
    #images=datas["pictures"]       #先不用图片

    # 存入 session（跨请求可用）
    session['urls'] = urls

    return render_template('search.html',titles=titles,urls=urls)


#VIP视频播放页面 注意没有声音
@app.route('/my_bilibili/search_vip')
def search_vip():
    # 获取前端传进来的关键词
    url = request.args.get('vip_url')
    if not url:
        return "未检测到输入信息 请重新输入"
    elif not '/' in url:
        url=f'https://search.bilibili.com/{url}'

    video_url,audio_url=get_vip_video_and_audio_url(url) #获取目标资源的地址
    session["video_url"]=video_url      #视频资源的地址
    session["audio_url"]=audio_url

    return render_template('vip_player.html')


#本地代理访问目标资源url以绕过B站防盗链
@app.route('/my_bilibili/vip_player')
def vip_player_video():
    video_url=session["video_url"]

    #print(video_url)
    resp=requests.get(video_url,params=params,headers=headers,cookies=cookies,stream=True) #流式传输这里不要忘了加stream避免爆内存

    # 构建Flask的流式响应，直接转发数据
    def generate():
        for chunk in resp.iter_content(chunk_size=8192):  # 分块读取数据
            yield chunk

    # 返回流式响应，传递原始视频的Content-Type
    return Response(generate(), content_type=resp.headers.get('Content-Type'))


#下载音频文件到本地
@app.route('/my_bilibili/vip_player_audio')
def vip_player_audio():
    audio_url = session["audio_url"]
    resp = requests.get(audio_url, params=params, headers=headers, cookies=cookies,stream=True)  # 流式传输这里不要忘了加stream避免爆内存

    # 构建Flask的流式响应，直接转发数据
    def generate():
        for chunk in resp.iter_content(chunk_size=8192):  # 分块读取数据
            yield chunk

    # 返回流式响应，传递原始视频的Content-Type
    return Response(generate(), content_type=resp.headers.get('Content-Type'))


# 由页面的 “下载” 键 触发请求 获得对应的音频文件url 在本地代理处理
# 利用session实现不同路由对应函数的数据交换
@app.route('/get_audio_download/<int:i>')
def get_audio_download(i:int):
    urls = session['urls']
    url_audio = get_audio_url(urls[i])
    return proxy_bilibili(url_audio)

@app.route('/get_video_download/<int:i>')
def get_video_download(i:int):
    urls =session['urls']
    url_video= get_video_url(urls[i])
    return proxy_bilibili(url_video)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)



