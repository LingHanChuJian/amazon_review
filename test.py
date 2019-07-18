import re

from setting import RE_TOKEN, RE_TYPE, RE_NAME, RE_RANK
from main import AmazonMain
from utils.dispose import AmazonFollowDispose


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
        disponse = AmazonFollowDispose(html)
        print(disponse.dispose())


if __name__ == '__main__':
    test3()
