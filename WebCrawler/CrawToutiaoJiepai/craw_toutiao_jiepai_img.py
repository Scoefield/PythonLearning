import requests
from urllib.parse import urlencode
import os
from hashlib import md5
from multiprocessing.pool import Pool
 
def save_image(item):
    if not os.path.exists(item.get('title')):
        os.mkdir(item.get('title'))
    try:
        response = requests.get("http:" + item.get('image'))
        # print(response)
        if response.status_code == 200:
            # print(response.content)
            file_path = '{0}/{1}.{2}'.format(item.get('title'), md5(response.content).hexdigest(), 'jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(response.content)
            else:
                print('Already Downloaded', file_path)
    except requests.ConnectionError:
        print('Failed to Save Image')

def get_images(json):
    if json.get('data'):
        for item in json.get('data'):
            title = item.get('title')
            # images = item.get('image_detail')
            images = item.get('image_list')
            for image in images:
                yield {
                    'image': image.get('url'),
                    'title': title
                }

'''
实现方法get_page()来加载单个Ajax请求的结果。其中唯一变化的参数就是offset，所以我们将它当作参数传递
'''
def get_page(offset, keyword):
    params = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoloas': 'true',
        'count': '20',
        'cur_tab': '1',
        'from': 'search_tab'
    }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(params)
    # print(url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError:
        return None

 
def main(offset):
    keyword = "街拍"
    json = get_page(offset, keyword)
    
    for item in get_images(json):
        print(item)
        save_image(item)

 
if __name__ == '__main__':
    GROUP_START = 1
    GROUP_END = 20

    pool = Pool()
    groups = ([x * 20 for x in range(GROUP_START, GROUP_END + 1)])
    pool.map(main, groups)
    pool.close()
    pool.join()