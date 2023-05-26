# encoding: utf-8

from bs4 import BeautifulSoup
import requests
import string
import re
import os

WIDTH = 1242
HEIGHT = 1660

def get_html(url):
    response = requests.get(url)
    text = response.text
    html = BeautifulSoup(text, 'html.parser',from_encoding='utf-8')
    return html

def get_description(html: BeautifulSoup)->string:
    text = html.find('div', class_='section__description').get_text()
    output = ' '.join(text)
    new_text = output.translate(str.maketrans("", "", string.whitespace))
    return new_text

def get_icon(html:BeautifulSoup)->string:
    screenshots = html.find('div', class_='product-hero__media')
    sources = screenshots.find_all('source')
    links = []
    for source in sources:
        image_type = source['type']
        if image_type in ['image/webp','image/jpeg']:
            continue
        srcset = source['srcset']
        match = re.search(r'https:.*?217x0w.png', srcset)
        link = match.group(0).split(" ")[-1]
        links.append(link)
    return links

def get_screenshot_addr(html: BeautifulSoup)->list:
    screenshots = html.find('div', class_='we-screenshot-viewer__screenshots')
    sources = screenshots.find_all('source')
    links = []
    for source in sources:
        image_type = source['type']
        if image_type in ['image/jpeg','image/png']:
            continue
        srcset = source['srcset']
        match = re.search(r'https:.*?600x0w.webp', srcset)
        link = match.group(0).split(" ")[-1]
        links.append(link)
    return links

def download_img(urls, save_dir):
    # 检查目录是否存在，如果不存在，创建目录
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # 下载图片
    for i in range(len(urls)):
        response = requests.get(urls[i])
        if response.status_code == 200:
            # 获取文件名和扩展名
            file_name = os.path.basename(urls[i])
            save_path = os.path.join(save_dir, "{}_".format(i) +file_name)
            with open(save_path, 'wb') as f:
                f.write(response.content)
                print('图片已保存。')
        else:
            print('图片下载失败。')
            
def write_txt(text, filename):
    file_path = os.path.join(filename, filename) + ".txt"
    file = open(file_path, "w")
    # 写入内容到文件
    file.write(text)
    # 关闭文件
    file.close()

def main(url, app_name):
    html = get_html(url)
    screenshots = get_screenshot_addr(html)
    description = get_description(html)
    icon = get_icon(html)
    image_urls = icon + screenshots
    download_img(image_urls, app_name)
    write_txt(description, app_name)
    
    
# def get_color(path):
#     from haishoku.haishoku import Haishoku
#     haishoku = Haishoku.loadHaishoku(path)
#     print(haishoku.palette)
#     Haishoku.showPalette(path)

if __name__ == "__main__":
    url = "https://apps.apple.com/cn/app/%E9%A3%9E%E9%B1%BC%E8%AE%A1%E5%88%92-%E6%AF%8F%E4%B8%AA%E4%BA%BA%E7%9A%84%E5%85%A8%E8%83%BD%E8%AE%B0%E5%BD%95%E5%B7%A5%E5%85%B7/id1571229028?platform=iphone"
    app_name = "focus"
    main(url, app_name)
    