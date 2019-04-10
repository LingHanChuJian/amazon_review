import time
import random
from fake_useragent import UserAgent

from utils.api import *
from utils.dispose import AmazonDispose
from utils.request import AmazonRequests


class AmazonMain:
    def __init__(self, data):
        self.data = data
        self.param = dict()
        self.review = dict()
        self.ua = UserAgent().random
        self.review_data = {'review_order_id': data['review_order_id']}
        self.session = AmazonRequests(self.data['amazon_buyer_url'], self.data['country'])

    def start(self):
        html = self.get_amazon_html()
        if not html:
            return None
        if html.find("Robot Check") > -1:
            return None
        dispose = AmazonDispose(html)
        token, types, name = dispose.get_token(), dispose.get_type(), dispose.get_name()
        if not token or not types or not name:
            return None
        print(token, types, name)
        self.review_data['buyer_name'] = name
        return self.get_data(token, ','.join(eval(types)))

    def get_data(self, token, types):
        self.param = self.session.get_review_param(token, types, self.get_next_page_token())
        self.review = self.get_amazon_review()
        if not self.get_review_data():
            if self.is_page():
                print('查找下一页数据')
                random_time = random.randint(5, 10)
                print('等待时间 %s' % random_time)
                time.sleep(random_time)
                return self.get_data(token, types)
            else:
                print('所有评论查找完成')
                return None
        else:
            return self.review_data

    def get_amazon_html(self):
        user_header['user-agent'] = self.ua
        response = self.session.get_amazon_data(self.session.get_user_url(), header=user_header, param=USER_PARAM)
        return self.request_message(response, 'txt')

    def get_amazon_review(self):
        reviews_header['user-agent'] = self.ua
        response = self.session.get_amazon_data(self.session.get_review_url(), header=reviews_header, param=self.param)
        return self.request_message(response, 'json')

    def request_message(self, response, mode):
        if response.status_code != 200:
            return None
        if mode == 'json':
            return response.json()
        elif mode == 'txt':
            return response.text

    def get_review_data(self):
        for item in self.review['contributions']:
            if item['product']['asin'] == self.data['asin']:
                self.review_data['review_date'] = int(str(item['sortTimestamp'])[:-3])
                self.review_data['review_title'] = item['title']
                self.review_data['review_text'] = item['text']
                self.review_data['review_star'] = item['rating']
                self.review_data['review_url'] = REVIEWS.format(domain=self.session.get_amazon_domain(),
                                                                externalId=item['externalId'])
                return self.review_data
        else:
            return None

    def is_page(self):
        if not self.review or self.review['nextPageToken']:
            return True
        return False

    def get_next_page_token(self):
        if self.review and self.review['nextPageToken']:
            return self.review['nextPageToken']
        return ''
