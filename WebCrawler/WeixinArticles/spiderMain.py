import requests
from urllib.parse import urlencode
from requests.exceptions import ConnectionError
import random
from pyquery import PyQuery as pq
from config import *

'''
反代理爬取微信公众号文章
'''


baseurl = "http://weixin.sogou.com/weixin?"
# cookies 头信息
# headers = {
#     'Cookie':'IPLOC=CN4403; SUID=9CF70FB72613910A000000005AA23FB7; SUV=0081272DB70FF79C5AA23FB972DBF008; pgv_pvi=9741034496; SMYUV=1520837726860941; CXID=35B560A8B25A52401B3F3D5BFEC0660B; GOTO=Af22661; usid=ZgFJ1tI0dqy_TTAl; ld=3kllllllll2bF9lqlllllVHGyxUlllllHZ@egyllll9lllll9llll5@@@@@@@@@@; LSTMV=220%2C291; LCLKINT=2439; ad=xlllllllll2bQXcglllllVHzKPtllllltqAZCyllll9lllllpCxlw@@@@@@@@@@@; ABTEST=8|1534079060|v1; SNUID=DC276F760E0B7E31907948CB0E1B4C30; weixinIndexVisited=1; sct=3; JSESSIONID=aaaXMXXqYinla4pWVu7tw',
#     'Host':'weixin.sogou.com',
#     'Upgrade-Insecure-Requests':'1',
#     'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
# }
# 返回一个随机的请求头 headers
def get_headers():
    user_agent_list = [ \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
    UserAgent = random.choice(user_agent_list)
    headers = {
        'Cookie':'IPLOC=CN4403; SUID=9CF70FB72613910A000000005AA23FB7; SUV=0081272DB70FF79C5AA23FB972DBF008; pgv_pvi=9741034496; SMYUV=1520837726860941; CXID=35B560A8B25A52401B3F3D5BFEC0660B; GOTO=Af22661; usid=ZgFJ1tI0dqy_TTAl; ld=3kllllllll2bF9lqlllllVHGyxUlllllHZ@egyllll9lllll9llll5@@@@@@@@@@; LSTMV=220%2C291; LCLKINT=2439; ad=xlllllllll2bQXcglllllVHzKPtllllltqAZCyllll9lllllpCxlw@@@@@@@@@@@; ABTEST=8|1534079060|v1; SNUID=DC276F760E0B7E31907948CB0E1B4C30; weixinIndexVisited=1; sct=3; SUIR=DC276F760E0B7E31907948CB0E1B4C30; JSESSIONID=aaaIM2xt0CP6OegnJe7tw; ppinf=5|1534126540|1535336140|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTo5OlNjb2VmaWVsZHxjcnQ6MTA6MTUzNDEyNjU0MHxyZWZuaWNrOjk6U2NvZWZpZWxkfHVzZXJpZDo0NDpvOXQybHVQZ1l0NlpucDd2Ymk2NS1EWklEdzI0QHdlaXhpbi5zb2h1LmNvbXw; pprdig=NMs4cwxNvPoSmQ-c-vw-RWC9rHIWLMZItZqflHMk7z2aEyHS66X8600aYLwwHFEDNXqQy1auprYms319OU2t9UWny2tP6JC5ILS5EgDMvhq2WHO64VdM7LcorukA0gW55MhplM97ip9-YPnp8eLXht8F8nl79QbaGvju7bccjnk; sgid=20-36559441-AVtw6cvOqQuicSbWfMm71RKU; ppmdig=1534126540000000706b0cf55d2dc477f96660c6586ccb30',
        'Host':'weixin.sogou.com',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent': UserAgent,
        }
    return headers

proxy = None

ip_lists = []
def read_ip_pool():
    with open('ip.txt', 'r') as f:
        lines = f.readlines()
    for line in lines:
        ip_lists.append(line.strip())
    # print(ip_lists)
    return ip_lists


def get_proxy():
    proxy_ip = random.choice(read_ip_pool())
    return proxy_ip

# 获取HTML
def get_html(url, count=1):
    print("Crawing:", url)
    print("Try count", count)
    global proxy
    if count >= COUNT_MAX:
        print("Try too many counts!")
        return None
    try:
        if proxy:
            proxies = {
                'http': 'http://' + proxy
            }
            response = requests.get(url, allow_redirects=False, headers=get_headers(), proxies=proxies)
        else:
            response = requests.get(url, allow_redirects=False, headers=get_headers())
        if response.status_code == 200:
            return response.text
        if response.status_code == 302:
            # 需要代理
            print("302")
            proxy = get_proxy()
            if proxy:
                print("Using Proxy:", proxy)
                return get_html(url)
            else:
                print("Get Proxy fail!!!")
                return None
    except ConnectionError as e:
        print("Error:", e.args)
        proxy = get_proxy()
        count += 1
        return get_html(url)

# 获取索引页
def get_index(keyword, page):
    data = {
        'query': keyword,
        'type': 2,
        'page': page,
    }
    queries = urlencode(data)
    url = baseurl + queries
    return url

# 解析索引页HTML
def parse_index(html):
    doc = pq(html)
    items = doc('.news-box .news-list li .txt-box h3 a').items()
    for item in items:
        yield item.attr['href']

def get_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None

def parse_detail(html):
    doc = pq(html)
    title = doc('.rich_media_title').text()
    content = doc('.rich_media_content').text().replace('\n', '')
    publish_time = doc('#post_time').text() # publish_time
    # nickname = doc('.rich_media_meta_list .rich_media_meta_nickname').text()
    nickname = doc('#js_profile_qrcode > div > p:nth-child(3) > span').text()
    return {
        'title': title,
        'content': content,
        'publish_time': publish_time,
        'nickname': nickname
    }


def main():
    for page in range(1, 101):
        url = get_index(KEYWORD, page)
        html = get_html(url)
        if html:
            article_urls = parse_index(html)
            for article_url in article_urls:
                # print(article_url)
                article_html = get_detail(article_url)
                if article_html:
                    article_data = parse_detail(article_html)
                    print(article_data)

if __name__ == '__main__':
    main()