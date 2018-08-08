import requests, re
import json
from connectmysql import ConnectMysql

"""
提取出猫眼电影TOP100的电影名称、时间、评分、图片等信息，
提取的站点URL为http://maoyan.com/board/4，提取的结果会以文件形式保存下来。
"""
indexs_re = '<dd>.*?board-index.*?>(.*?)</i>'
image_re = '<dd>.*?data-src="(.*?)"'
re_index_img = '<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)"'

def parse_one_page(html):
    # 正则表达式提取电影排名、图片、电影名、主演、发布时间等信息
    re_str = '<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>'
    patern = re.compile(re_str, re.S)
    items = re.findall(patern, html)
    # print(items)
    '''
        带有 yield 的函数不再是一个普通函数，而是一个生成器generator，可用于迭代，工作原理同上。
        yield 是一个类似 return 的关键字，迭代一次遇到yield时就返回yield后面的值。重点是：下一次迭代时，从上一次迭代遇到的yield后面的代码开始执行。
        简要理解：yield就是 return 返回一个值，并且记住这个返回的位置，下次迭代就从这个位置后开始。
    '''
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2].strip(),
            'actor': item[3].strip()[3:] if len(item[3]) > 3 else '',
            'time': item[4].strip()[5:] if len(item[4]) > 5 else '',
            'score': item[5].strip() + item[6].strip()
        }
        # print(item)


def write_to_json(content):
    with open('CrawMaoyanMoveInfo/result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False)+'\n')
        # f.write(str(content))

def get_one_page(url):
    # print("正在请求url...")
    response = requests.get(url)
    if response.status_code == 200: # ok响应
        return response.text
    return None

def main(offset):
    connsql = ConnectMysql()

    url = "http://maoyan.com/board/4?offset=" + str(offset)
    html = get_one_page(url)
    # with open('test.txt', 'w', encoding='utf-8') as f:    # 打印出HTML用于调试
    #     f.write(html)
    # print(html)

    results = parse_one_page(html)
    for result in results:
        # write_to_json(result) # 以json格式生成txt文件
        connsql.mysql_collect_data(result)  # 收集并保存数据于列表中
        # print(result)
   
    connsql.saveData()  # 写入数据库


if __name__ == "__main__":
    for i in range(10):
        main(offset=i*10)
    
    print("完成！")