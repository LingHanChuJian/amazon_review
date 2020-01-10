import re
import os
import json
from setting import RE_TOKEN, RE_TYPE, RE_NAME, RE_RANK, RE_IMAGE_URL, RE_URL_ASIN, RE_VIDEOS
from main import AmazonMain
from utils.dispose import AmazonFollowDispose, AmazonReviewDispose, AmazonProductDetailsDispose
from urllib.parse import urlparse


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
        dispose = AmazonProductDetailsDispose('US', html)
        print(dispose.dispose())


def test4():
    # json_text = '{"https://images-na.ssl-images-amazon.com/images/I/31ZyMRGBoVL._AC_.jpg": [442, 499],' \
    #             '"https://images-na.ssl-images-amazon.com/images/I/31ZyMRGBoVL._AC_SX466_.jpg": [413, 466],' \
    #             '"https://images-na.ssl-images-amazon.com/images/I/31ZyMRGBoVL._AC_SX425_.jpg": [376, 425],' \
    #             '"https://images-na.ssl-images-amazon.com/images/I/31ZyMRGBoVL._AC_SX450_.jpg": [399, 450],' \
    #             '"https://images-na.ssl-images-amazon.com/images/I/31ZyMRGBoVL._AC_SX355_.jpg": [314, 355]}'
    try:
        json_text = ''
        images = [key for key in json.loads(json_text)]
        return re.compile(RE_IMAGE_URL).sub('US150', os.path.basename(images[0])) if images else ''
    except Exception as e:
        print(e)
        return ''


def test5():
    res = ['\n      ', 'Duo', '\n    ', '\n      ', 'Duo Evo Plus', '\n    ', '\n      ', 'Duo Crisp', '\n    ']
    print(list(filter(None, [''.join(item).strip().replace('\n', '') if item else '' for item in res])))


def test6():
    res = 'http://www.amazon.ca/dp/B081R6GTYM?ref=myi_title_dp'
    cur_path = urlparse(res).path
    asin = re.search(RE_URL_ASIN, cur_path)
    return asin.group(1).replace('/', '') if asin else ''


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


if __name__ == '__main__':
    # sun = Sun('凌寒初见')
    # sun.log()
    # sun.log2()
    # test3()
    # print(test6())
    print(test7())
    # print(test4())
    # print(test8('by        adada'))
