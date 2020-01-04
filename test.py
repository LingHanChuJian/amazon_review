import re
import os

from setting import RE_TOKEN, RE_TYPE, RE_NAME, RE_RANK, RE_IMAGE_URL, RE_URL_ASIN
from main import AmazonMain
from utils.dispose import AmazonFollowDispose, AmazonReviewDispose
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
        dispose = AmazonReviewDispose('US', html)
        print(dispose.dispose())


def test4():
    res = re.compile(RE_IMAGE_URL).sub('US150', os.path.basename('https://images-na.ssl-images-amazon.com'
                                                                 '/images/I/51B9FMLBfGL._SX679_.jpg'))
    print(res)


def test5():
    res = ['\n      ', 'Duo', '\n    ', '\n      ', 'Duo Evo Plus', '\n    ', '\n      ', 'Duo Crisp', '\n    ']
    print(list(filter(None, [''.join(item).strip().replace('\n', '') if item else '' for item in res])))


def test6():
    res = 'https://www.amazon.com/VATI-Compatible-Silicone-Replacement-iWatch/dp/B07PBYZ1SC?' \
          'pf_rd_p=c4a36063-ed31-585b-b9d3-e14ee41d7e8c&pf_rd_r=QJ8XXG7002KAVMB4KNNZ&pd_rd_wg=Qfr1q&ref_=pd_gw_ri' \
          '&pd_rd_w=eZuVZ&pd_rd_r=5afeed1d-d9a7-4cee-b492-aff411ca9402&th=1'
    cur_path = urlparse(res).path
    asin = re.search(RE_URL_ASIN, cur_path)
    return asin.group(1) if asin else ''


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
    test3()
    # print(test6())