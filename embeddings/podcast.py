import requests
import re
from bs4 import BeautifulSoup
import aiohttp
import asyncio

BASE_URL = "https://www.xiaoyuzhoufm.com"

def get_audio_addr(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    meta_tags = soup.find_all('meta')
    # 获取title标签
    title_tag = soup.title
    for meta in meta_tags:
        if meta.get('property') == 'og:audio':
            addr = meta.get('content')
            content = {
                "vol_name": title_tag.string,
                "vol_url": url,
                "vol_mark": episode_mark(title_tag.string),
                "vol_audio_addr": addr
            }
            print("Content:", content)
            return content

def episode_mark(text):
    # 编写正则表达式，使用()包含要提取的内容
    pattern = r'(.+?)\s'
    # 使用re模块的search函数查找符合条件的字符串
    match = re.search(pattern, text)
    # 如果找到了，输出提取到的内容
    if match:
        return match.group(1)
    return ""

def get_episode_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # 获取所有 <li> 标签
    li_list = soup.find_all('li')
    # 遍历每个 <li> 标签，获取第一个 <a> 标签的 ref 属性
    episode_urls = []
    for li in li_list:
        a = li.find('a')
        if a and 'href' in a.attrs:
            href = BASE_URL + a['href']
            episode_urls.append(href)
    return episode_urls

def get_auido(url):
    info = []
    episode_info = get_episode_info(url)
    if episode_info:
        for episode_url in episode_info:
            info.append(get_audio_addr(episode_url))
    return info

async def download_audio(session, url, filename):
    async with session.get(url) as response:
        with open(filename, 'wb') as f:
            while True:
                chunk = await response.content.read(1024)
                if not chunk:
                    break
                f.write(chunk)
        print(f"Downloaded {filename} from {url}")

async def main(urls):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i, url in enumerate(urls):
            filename = "./audio/{}_audio.mp3".format(url.get("vol_mark"))
            task = asyncio.ensure_future(download_audio(session, url.get("vol_audio_addr"), filename))
            tasks.append(task)

        await asyncio.gather(*tasks)

    print("All audio files downloaded")


if __name__ == "__main__":
    url = 'https://www.xiaoyuzhoufm.com/podcast/62c6ae08c4eaa82b112b9c84'
    download_url = get_auido(url)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(download_url))
     
