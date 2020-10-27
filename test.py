import re
import os
import json
import time
import random
import threading

from queue import Queue
from multiprocessing import cpu_count

from setting import RE_TOKEN, RE_TYPE, RE_NAME, RE_RANK, RE_IMAGE_URL, RE_URL_ASIN, RE_VIDEOS
from main import AmazonMain
from utils.dispose import AmazonFollowDispose, AmazonReviewDispose, AmazonProductDetailsDispose
from urllib.parse import urlparse
from utils.proxies import Proxy
from utils.log import log


def test():
    with open('amazon.txt', 'r', encoding='utf-8') as f:
        html = f.read()
        token = re.search(RE_TOKEN, html, re.M).group(1)
        types = re.search(RE_TYPE, html, re.M).group(1)
        name = re.search(RE_NAME, html, re.M).group(1)
        rank = re.search(RE_RANK, html, re.M).group(1)
        print(token)
        print(types)
        print(name)
        print(rank)


def test2():
    data = {'review_order_id': '127460', 'amazon_buyer_url': 'AGTY2X5LLDAWOTH6P6XTYUR6UKDQ',
            'country': 'US', 'asin': 'B009GYQZBE'}
    main = AmazonMain(data)
    review_data = main.start()
    print(review_data)
    pass


def test3():
    with open('amazon.txt', 'r', encoding='utf-8') as f:
        html = f.read()
        dispose = AmazonProductDetailsDispose('DE', html)
        print(dispose.dispose())


def test4():
    json_text = '{"https://images-na.ssl-images-amazon.com/images/I/71c91AnZLXL._AC_SY450_.jpg":[450,450],' \
                '"https://images-na.ssl-images-amazon.com/images/I/71c91AnZLXL._AC_SX425_.jpg":[425,425],' \
                '"https://images-na.ssl-images-amazon.com/images/I/71c91AnZLXL._AC_SX522_.jpg":[522,522],' \
                '"https://images-na.ssl-images-amazon.com/images/I/71c91AnZLXL._AC_SX679_.jpg":[679,679],' \
                '"https://images-na.ssl-images-amazon.com/images/I/71c91AnZLXL._AC_SX466_.jpg":[466,466],' \
                '"https://images-na.ssl-images-amazon.com/images/I/71c91AnZLXL._AC_SX569_.jpg":[569,569],' \
                '"https://images-na.ssl-images-amazon.com/images/I/71c91AnZLXL._AC_SY355_.jpg":[355,355]}'
    try:
        # json_text = ''
        images = [key for key in json.loads(json_text)]
        return re.compile(RE_IMAGE_URL).sub('_US150_', os.path.basename(images[0])) if images else ''
    except Exception as e:
        print(e)
        return ''


def test5():
    res = ['\n      ', 'Duo', '\n    ', '\n      ', 'Duo Evo Plus', '\n    ', '\n      ', 'Duo Crisp', '\n    ']
    print(list(filter(None, [''.join(item).strip().replace('\n', '') if item else '' for item in res])))


def test6():
    # res = 'http://www.amazon.ca/dp/B081R6GTYM'
    # res = 'http://www.amazon.ca/dp/B081R6GTYM?ref=myi_title_dp'
    res = 'https://www.amazon.com/gp/product/B086P4VQSF/ref=ag_xx_cont_xx'
    cur_path = urlparse(res).path
    asin = re.search(RE_URL_ASIN, cur_path)
    return asin.group(asin.lastindex).replace('/', '') if asin else ''


def test7():
    res = "[[VIDEOID:4335d8ed8c384b2f942c1452379f9ac0]] [[VIDEOID:4335d8ed8c384b2f942c1452379f9ac0]] I want to give special attention and rating to COWIN's " \
          "AMAZING customer service.<br />I never imagined they could be so kind and understanding and after " \
          "contacting them I just had to go back and write this thankful review.<br /><br />I'm using the headphones " \
          "for music, TV, PlayStation and they work great. The noise canceling feature does a nice job for that " \
          "matter as well."
    videos = re.search(RE_VIDEOS, res)
    if videos:
        print(videos.group(0))
        res = res.replace(videos.group(0), '')
    return res.replace('<br />', '').strip()


def test8(data):
    return ' '.join(''.join(data).strip().replace('\n', '').split()) if data else ''


class Base:
    def __init__(self, data):
        self.data = data

    def log(self):
        print(self.data)


class Sun(Base):
    def __init__(self, name):
        self.name = name
        super(Sun, self).__init__(self.name + 'super')

    def log2(self):
        print(self.name)


class ThreadingTest:
    def __init__(self):
        self.names = []
        q = Queue()
        t_arr = []
        for item in range(cpu_count()):
            t = threading.Thread(target=self.get_name, args=(item, q,))
            t.setDaemon(True)
            t_arr.append(t)
            t.start()
        for t_item in t_arr:
            t_item.join()
            self.names.append(q.get())
        print(self.names)

    @staticmethod
    def random_num():
        return random.randint(0, 20)

    def get_name(self, timer, q):
        print(timer)
        time.sleep(timer)
        q.put(self.random_num())


if __name__ == '__main__':
    # sun = Sun('凌寒初见')
    # sun.log()
    # sun.log2()
    # test3()
    # print(test6())
    # print(test7())
    # print(test4())
    # print(test8('by        adada'))
    # proxies = Proxy().get_proxies()
    # print(proxies)
    # proxies.get_proxies()
    # ThreadingTest()
    # log(1, {'a': 'b'}, [1,2,3,4])
    # log('你好')
    print(os.path.dirname(__file__))

