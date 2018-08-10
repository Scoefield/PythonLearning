import requests
from bs4 import BeautifulSoup
import re
import os

# ----------------------- 方法一：用re正在表达式解析 ---------------------------------
def re_parse_url(html):
    restr = '<li>.*?href="(.*?)".*?extiw'
    patern = re.compile(restr, re.S)
    items = re.findall(patern, html)
    print(items)


# ----------------------- 方法二：用BeautifulSoup解析库解析 ------------------------------
def parse_page_url(html):

    soup = BeautifulSoup(html, 'lxml')
    li_lists = soup.find_all(name='ul')[0].find_all(name='li')
    # print(li_lists)
    count = 0
    # temp_lists = []
    temp_dict = {}
    for li in li_lists:
        count += 1
        if count <= 8:
            a_lists = li.find_all(name='a')[0]
      
            a_url = "http:" + a_lists.attrs['href']
            end_word = a_url.replace('ebooks', 'cache/epub').split('/')[-1]
            end_url = a_url.replace('ebooks', 'cache/epub') + "/pg" + end_word + ".txt"
            # print(a_url)
            # temp_lists.append(end_url)
            temp_dict[end_word] = end_url
        else:
            break
        # print(a_lists.attrs['href'])
    return temp_dict


def get_page_url(main_url):
    response = requests.get(main_url)
    if response.status_code == 200:
        # print(response.text)
        return response.text
    return None
    # soup = BeautifulSoup(html, 'lxml')

def save_text(url_dicts):
    file_dir = os.path.join(os.getcwd(), 'result')
    if not os.path.exists(file_dir):
        os.mkdir(file_dir)
    for urlkey, urlvalue in url_dicts.items():
        content = get_page_url(urlvalue)
        file_path = os.path.join(file_dir, urlkey) + '.txt'
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                # f.close()

def main():
    main_url = "https://www.gutenberg.org/wiki/Education"
    print("开始爬取目标URL......")
    html = get_page_url(main_url)   # 根据目标URL获得HTML
    # print(html)
    print("获取HTML成功！正在解析HTML......")
    # re_parse_url(html)    # 方法一：
    url_dicts = parse_page_url(html)    # 方法二：解析HTML，返回字典
    print("解析HTML成功！正在保存爬取的数据......")
    save_text(url_dicts)    # 保存文本
    print("数据保存成功！已完成爬取！")
   

if __name__ == '__main__':
    main()