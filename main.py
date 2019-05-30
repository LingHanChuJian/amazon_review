from fake_useragent import UserAgent

from setting import MAX_PAGE, NICE_REVIEW_NUM
from utils.api import *
from utils.utils import *
from utils.dispose import AmazonDispose, AmazonBadDispose
from utils.request import AmazonRequests, AmazonReviewRequests


class AmazonMain:
    def __init__(self, data):
        self.page = 1
        self.data = data
        self.param = dict()
        self.review = dict()
        self.ua = UserAgent().random
        self.review_data = {'review_order_id': data['review_order_id']}
        self.session = AmazonRequests(self.data['amazon_buyer_url'], self.data['country'])

    def start(self):
        html = self.get_amazon_html()
        if not html:
            print('没有数据')
            return None
        dispose = AmazonDispose(html)
        if is_robot(dispose.get_selector()):
            print('机器人')
            return None
        token, types, name, rank = dispose.get_token(), dispose.get_type(), dispose.get_name(), dispose.get_rank()
        if name:
            self.review_data['buyer_name'] = name
        if rank:
            self.review_data['buyer_rank'] = rank
        print(name, rank)
        if not token or not types:
            return None
        print(token, types)
        return self.get_data(token, ','.join(eval(types)))

    def get_data(self, token, types):
        self.param = self.session.get_review_param(token, types, self.get_next_page_token())
        self.review = self.get_amazon_review()
        if not self.get_review_data():
            if self.is_page():
                if self.page >= MAX_PAGE:
                    print('查找到最大页数')
                    return self.review_data
                print('查找下一页数据')
                wait()
                self.page += 1
                return self.get_data(token, types)
            else:
                print('所有评论查找完成')
                return self.review_data
        else:
            return self.review_data

    def get_amazon_html(self):
        user_header['user-agent'] = self.ua
        response = self.session.get_amazon_data(self.session.get_user_url(), header=user_header, param=USER_PARAM)
        return request_message(response, 'txt')

    def get_amazon_review(self):
        reviews_header['user-agent'] = self.ua
        response = self.session.get_amazon_data(self.session.get_review_url(), header=reviews_header, param=self.param)
        return request_message(response, 'json')

    def get_review_data(self):
        for item in self.review['contributions']:
            if item['product']['asin'] == self.data['asin']:
                self.review_data['review_date'] = int(str(item['sortTimestamp'])[:-3])
                self.review_data['review_title'] = item['title']
                self.review_data['review_text'] = item['text']
                self.review_data['review_star'] = item['rating']
                self.review_data['review_url'] = REVIEWS.format(domain=get_amazon_domain(self.data['country']),
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


class AmazonReviewsMain:

    def __init__(self, data):
        self.all_data = []
        self.data = data
        self.is_lang = False
        self.nice_review_num = 0
        self.session = AmazonReviewRequests(data['country'], data['asin'])

    def get_amazon_html(self):
        response = self.session.get_amazon_data(self.is_lang)
        return request_message(response, 'txt')

    def start(self):
        response = self.get_amazon_html()
        if response and is_number(response):
            if response == 404:
                print('asin 不存在')
                return None
        dispose = AmazonBadDispose(self.data['country'], response)
        dispose.set_nice_review_num(self.nice_review_num)
        if is_robot(dispose.get_selector()):
            print('机器人验证')
            return self.start()
        if dispose.is_lang():
            self.is_lang = True
            print('语言不符合, 重新请求')
            wait()
            return self.start()
        dict_data = dispose.dispose()
        self.nice_review_num = dispose.get_nice_review_num()
        print(dict_data)
        print(self.nice_review_num)
        if self.nice_review_num >= NICE_REVIEW_NUM:
            return self.all_data
        if dict_data:
            self.all_data.extend(dict_data)
        else:
            print('没有数据写入')
        if dispose.is_next_page():
            print('请求下一页')
            self.session.next_page()
            wait()
            return self.start()
        else:
            print('评论获取完毕')
            return -3




