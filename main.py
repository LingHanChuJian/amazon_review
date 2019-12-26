import re
from fake_useragent import UserAgent
from urllib.parse import urlparse

from setting import MAX_PAGE, NICE_REVIEW_NUM, AMAZON_ZIPCODE, RE_URL_ASIN
from utils.api import *
from utils.utils import *
from utils.dispose import *
from utils.request import *


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
        self.is_bad = True
        self.nice_review_num = 0
        self.session = AmazonUserReviewRequests(data['country'], data['asin'], data['count'])

    def get_amazon_html(self):
        response = self.session.get_amazon_data(self.is_lang, self.get_bad())
        return request_message(response, 'txt')

    def start(self):
        response = self.get_amazon_html()
        if response and is_number(response):
            if response == 404:
                print('asin 不存在')
                return None
        dispose = AmazonBadDispose(self.data['country'], response, self.data['count'])
        if is_robot(dispose.get_selector()):
            print('机器人验证')
            return self.start()
        if dispose.is_lang():
            self.is_lang = True
            print('语言不符合, 重新请求')
            wait()
            return self.start()
        dispose.set_nice_review_num(self.nice_review_num)
        dict_data = dispose.dispose()
        self.nice_review_num = dispose.get_nice_review_num()
        # print(dict_data)
        # print(self.nice_review_num)
        if dict_data:
            self.all_data.extend(dict_data)
        else:
            print('没有数据写入')
        if self.data['count'] == 1 and self.nice_review_num >= NICE_REVIEW_NUM:
            if self.all_data:
                return self.all_data
            else:
                return -3
        if self.data['count'] != 1:
            if self.all_data:
                return self.all_data
            else:
                return -3
        if dispose.is_next_page():
            print('请求下一页')
            self.session.next_page()
            wait()
            return self.start()
        else:
            print('评论获取完毕')
            return -3

    def set_bad(self, is_bad=True):
        self.is_bad = is_bad

    def get_bad(self):
        return self.is_bad


class BaseMain:
    def __init__(self, country, session):
        self.session = session
        self.country = country

    def change_address(self):
        amazon_response = self.session.get_amazon_data(get_amazon_domain(self.country))
        amazon_response = request_message(amazon_response, 'txt')
        if not amazon_response:
            return -5
        amazon_dispose = BaseDispose(amazon_response)
        if is_robot(amazon_dispose.get_selector()):
            return -6
        cur_data = address_data.copy()
        zip_code = AMAZON_ZIPCODE[self.country]
        cur_data['zipCode'] = zip_code
        if self.country == 'AE':
            del cur_data['zipCode']
            cur_data['locationType'] = 'CITY'
            cur_data['city'] = zip_code
            cur_data['cityName'] = zip_code
        address_response = self.session.post_address_change(cur_data)
        address_response = request_message(address_response, 'json')
        print(address_response)
        is_address = 'address' in address_response and 'zipCode' in address_response['address']
        if not self.country == 'AU' and not is_address:
            return -7
        print('国家为AU, 需要登陆才能更换地址') if self.country == 'AU' else print('更换对应国家地址')
        return ''


class AmazonFollowMain(BaseMain):
    def __init__(self, data):
        self.all_data = []
        self.data = data
        self.session = AmazonFollowRequests(self.data['country'], self.data['asin'])
        self.url = self.session.get_follow_url()
        super(AmazonFollowMain, self).__init__(self.data['country'], self.session)

    def start(self):
        if self.url == self.session.get_follow_url():
            results = self.change_address()
            if type(results) == int:
                return results
        follow_response = self.session.get_amazon_data(self.url)
        follow_response = request_message(follow_response, 'txt')
        if not follow_response:
            return -5
        follow_dispose = AmazonFollowDispose(follow_response)
        if is_robot(follow_dispose.get_selector()):
            return -6
        data = follow_dispose.dispose()
        print(data)
        self.all_data.extend(data)
        if follow_dispose.get_next_page():
            self.url = ASIN_FOLLOW_OFFER_NEXT.format(domain=get_amazon_domain(self.data['country']),
                                                     next_url=follow_dispose.get_next_page())
            wait()
            return self.start()
        return self.all_data if self.all_data else -3

    def get_url(self):
        return self.url


class AmazonProductDetailsMain(BaseMain):
    def __init__(self, url):
        self.url = url
        self.session = AmazonProductDetailsRequests(self.get_country())
        super(AmazonProductDetailsMain, self).__init__(self.get_country(), self.session)

    def get_country(self):
        cur_domain = urlparse(self.url).netloc
        for domain_item in AMAZON_DOMAIN:
            domain = urlparse(AMAZON_DOMAIN[domain_item]).netloc
            if cur_domain == domain:
                return domain_item
        return ''

    def get_asin(self):
        cur_path = urlparse(self.url).path
        asin = re.search(RE_URL_ASIN, cur_path)
        return asin.group(1) if asin else ''

    def start(self):
        results = self.change_address()
        if type(results) == int:
            return results
        product_details_response = self.session.get_amazon_data(self.url)
        product_details_response = request_message(product_details_response, 'txt')
        if not product_details_response:
            return -5
        product_details_dispose = AmazonProductDetailsDispose(product_details_response)
        if is_robot(product_details_dispose.get_selector()):
            return -6
        data = product_details_dispose.dispose()
        data['country'] = self.get_country()
        data['asin'] = self.get_asin()
        return data


class AmazonReviewMain(BaseMain):
    def __init__(self, url):
        self.url = url
        self.session = AmazonReviewRequests(self.get_country())
        super(AmazonReviewMain, self).__init__(self.get_country(), self.session)

    def get_country(self):
        cur_domain = urlparse(self.url).netloc
        for domain_item in AMAZON_DOMAIN:
            domain = urlparse(AMAZON_DOMAIN[domain_item]).netloc
            if cur_domain == domain:
                return domain_item
        return ''

    def start(self):
        results = self.change_address()
        if type(results) == int:
            return results
        review_response = self.session.get_amazon_data(self.url)
        review_response = request_message(review_response, 'txt')
        if not review_response:
            return -5
        review_dispose = AmazonReviewDispose(self.get_country(), review_response)
        if is_robot(review_dispose.get_selector()):
            return -6
        data = review_dispose.dispose()
        data['review_url'] = self.url
        return data
