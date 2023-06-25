import requests
from bs4 import BeautifulSoup
import csv

def recursive_crawl(url, visited_urls, csv_writer):
    try:
        headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        content = response.text

        soup = BeautifulSoup(content, 'html.parser')
        links = soup.find_all('a', title=True, target=True, class_=True)

        for link in links:
            href = link.get('href')
            if href and (href.startswith('http') or href.startswith('https') or href.startswith('//')):
                if href.startswith('//'):
                    href = 'https:' + href
                if href not in visited_urls:
                    visited_urls.add(href)
                    class_name = link.get('class')
                    if class_name and ('high_light' in class_name or 'name' in class_name or 'recommenditem' in class_name): # 在这个位置，如果有需要的可以根据网页中对应的class 进行调整
                        title = link.get('title')
                        if title:
                            csv_writer.writerow([title, href])  # 将class和标签内容写入CSV文件
                            print(title, href)
            recursive_crawl(href, visited_urls, csv_writer)

    except requests.exceptions.RequestException as e:
        print("请求错误:", e)

# 示例使用
start_url = "https://yw.zxxk.com/h/review-sce3207/index-2.html"
visited = set()

# 创建CSV文件并写入表头
csv_file = open('output.csv', 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['标题', '地址'])

recursive_crawl(start_url, visited, csv_writer)

# 关闭CSV文件
csv_file.close()
