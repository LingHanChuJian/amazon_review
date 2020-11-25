import re
from fake_useragent import UserAgent
from urllib.parse import urlparse

from setting import MAX_PAGE, NICE_REVIEW_NUM, AMAZON_ZIPCODE, RE_URL_ASIN
from utils.api import *
from utils.utils import *
from utils.dispose import *
from utils.request import *
from utils.proxies import Proxy
from utils.log import log


class AmazonMain:
    def __init__(self, data):
        self.page = 1
        self.data = data
        self.param = dict()
        self.review = dict()
        self.ua = UserAgent().random
        self.review_data = {'review_order_id': data['review_order_id']}
        session, proxy = Proxy().get_proxies(self.data['country'])
        # session, proxy = Proxy().get_proxies()
        self.session = AmazonRequests(self.data['amazon_buyer_url'], self.data['country'], session)
        self.proxy = proxy

    def start(self):
        if not self.proxy:
            return -8
        html = self.get_amazon_html()
        if not html:
            log('没有数据')
            return None
        dispose = AmazonDispose(html)
        if is_robot(dispose.get_selector()):
            log('机器人')
            return None
        token, types, name, rank = dispose.get_token(), dispose.get_type(), dispose.get_name(), dispose.get_rank()
        if name:
            self.review_data['buyer_name'] = name
        if rank:
            self.review_data['buyer_rank'] = rank
        log(name, rank)
        if not token or not types:
            return None
        log(token, types)
        return self.get_data(token, ','.join(eval(types)))

    def get_data(self, token, types):
        self.param = self.session.get_review_param(token, types, self.get_next_page_token())
        self.review = self.get_amazon_review()
        if not self.get_review_data():
            if self.is_page():
                if self.page >= MAX_PAGE:
                    log('查找到最大页数')
                    return self.review_data
                log('查找下一页数据')
                wait()
                self.page += 1
                return self.get_data(token, types)
            else:
                log('所有评论查找完成')
                return self.review_data
        else:
            return self.review_data

    def get_amazon_html(self):
        user_header['user-agent'] = self.ua
        response = self.session.get_amazon_data(self.session.get_user_url(),
                                                header=user_header, param=USER_PARAM, proxies=self.proxy)
        return request_message(response, 'txt')

    def get_amazon_review(self):
        reviews_header['user-agent'] = self.ua
        response = self.session.get_amazon_data(self.session.get_review_url(), header=reviews_header,
                                                param=self.param, proxies=self.proxy)
        return request_message(response, 'json')

    def get_review_data(self):
        for item in self.review['contributions']:
            if 'product' in item:
                if item['product']['asin'] == self.data['asin']:
                    text, videos = self.get_text(item['text'])
                    images = self.get_images(item['images'])
                    self.review_data['review_date'] = int(str(item['sortTimestamp'])[:-3])
                    self.review_data['review_title'] = item['title']
                    self.review_data['review_text'] = text
                    self.review_data['review_star'] = item['rating']
                    if images:
                        self.review_data['review_images'] = images
                    if videos:
                        self.review_data['review_videos'] = 1
                    self.review_data['review_url'] = REVIEWS.format(domain=get_amazon_domain(self.data['country']),
                                                                    externalId=item['externalId'])
                    return self.review_data
        else:
            return None

    # 个人主页
    @staticmethod
    def get_images(data):
        return [os.path.basename(item['largeImageUrl']) for item in data] if data else []

    @staticmethod
    def get_text(data):
        videos = re.search(RE_VIDEOS, data)
        if videos:
            data = data.replace(videos.group(0), '')
        return data.replace('<br />', '').strip(), videos

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
        session, proxy = Proxy().get_proxies(self.data['country'])
        # session, proxy = Proxy().get_proxies()
        self.session = AmazonUserReviewRequests(data['country'], data['asin'], data['count'], session)
        self.proxy = proxy

    def get_amazon_html(self, url=None):
        response = self.session.get_amazon_data(self.is_lang, self.get_bad(), proxies=self.proxy, url=url)
        return request_message(response, 'txt')

    def start(self, url=None):
        if not self.proxy:
            return -8
        response = self.get_amazon_html(url)
        if response and is_number(response):
            if response == 404:
                log('asin 不存在')
                return None
        dispose = AmazonBadDispose(self.data['country'], response, self.data['count'])
        if is_robot(dispose.get_selector()):
            log('机器人验证')
            wait()
            return self.start()
        if dispose.is_lang():
            self.is_lang = True
            log('语言不符合, 重新请求')
            wait()
            return self.start()
        dispose.set_nice_review_num(self.nice_review_num)
        dict_data = dispose.dispose()
        self.nice_review_num = dispose.get_nice_review_num()
        # log(dict_data)
        # log(self.nice_review_num)
        if dict_data:
            self.all_data.extend(dict_data)
        else:
            log('没有数据写入')
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
            log('请求下一页')
            self.session.next_page()
            wait()
            return self.start(dispose.get_next_url())
        else:
            log('评论获取完毕')
            return -3

    def set_bad(self, is_bad=True):
        self.is_bad = is_bad

    def get_bad(self):
        return self.is_bad


class BaseMain:
    def __init__(self, country, session):
        self.session = session
        self.country = country

    def change_address(self, proxies=None):
        amazon_response = self.session.get_amazon_data(get_amazon_domain(self.country), proxies)
        amazon_response = request_message(amazon_response, 'txt')
        if not amazon_response:
            return -5
        amazon_dispose = BaseDispose(amazon_response)
        if is_robot(amazon_dispose.get_selector()):
            log('请求amazon主页, 机器人验证')
            return -6
        address_dom_response = self.session.get_address_html(proxies)
        address_dom_response = request_message(address_dom_response, 'txt')
        if not address_dom_response:
            return -9
        address_dom_dispose = AmazonDispose(address_dom_response)
        address_csrf_token = address_dom_dispose.get_address_csrf_token()
        if not address_csrf_token:
            return -10
        cur_address_data = address_data.copy()
        zip_code = AMAZON_ZIPCODE[self.country]
        cur_address_data['district'] = zip_code
        cur_address_data['countryCode'] = zip_code
        log(cur_address_data)
        address_response = self.session.post_address_change(address_csrf_token, cur_address_data, proxies)
        # address_response.status_code = 200
        # address_response = request_message(address_response, 'json')
        # log(address_response)
        # is_address = address_response and 'address' in address_response and 'zipCode' in address_response['address']
        # if not self.country == 'AU' and not self.country == 'FR' and not is_address:
        #     return -7
        # log('国家为{country}, 需要登陆才能更换地址'.format(country=self.country)) if self.country == 'AU' or self.country == 'FR' else log('更换对应国家地址')
        return '' if address_response.status_code == 200 else -7



class AmazonFollowMain(BaseMain):
    def __init__(self, data):
        self.all_data = []
        self.data = data
        session, proxy = Proxy().get_proxies(self.data['country'])
        # session, proxy = Proxy().get_proxies()
        self.session = AmazonFollowRequests(self.data['country'], self.data['asin'], session)
        self.url = self.session.get_follow_url()
        self.proxy = proxy
        super(AmazonFollowMain, self).__init__(self.data['country'], self.session)

    def start(self):
        if not self.proxy:
            return -8
        if self.url == self.session.get_follow_url():
            results = self.change_address(self.proxy)
            if type(results) == int:
                return results
        follow_response = self.session.get_amazon_data(self.url, self.proxy)
        follow_response = request_message(follow_response, 'txt')
        if not follow_response:
            return -9
        follow_dispose = AmazonFollowDispose(follow_response)
        if is_robot(follow_dispose.get_selector()):
            return -6
        data = follow_dispose.dispose()
        log(data)
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
        session, proxy = Proxy().get_proxies(self.get_country())
        # session, proxy = Proxy().get_proxies()
        self.session = AmazonProductDetailsRequests(self.get_country(), session)
        self.proxy = proxy
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
        return asin.group(asin.lastindex).replace('/', '') if asin else ''

    def start(self):
        if not self.proxy:
            return -8
        results = self.change_address(self.proxy)
        if type(results) == int:
            return results
        product_details_response = self.session.get_amazon_data(self.url, self.proxy)
        product_details_response = request_message(product_details_response, 'txt')
        if not product_details_response:
            return -9
        product_details_dispose = AmazonProductDetailsDispose(self.get_country(), product_details_response)
        if is_robot(product_details_dispose.get_selector()):
            return -6
        data = product_details_dispose.dispose()
        data['country'] = self.get_country()
        data['asin'] = self.get_asin()
        return data


class AmazonReviewMain(BaseMain):
    def __init__(self, url):
        self.url = url
        session, proxy = Proxy().get_proxies(self.get_country())
        # session, proxy = Proxy().get_proxies()
        self.session = AmazonReviewRequests(self.get_country(), session)
        self.proxy = proxy
        super(AmazonReviewMain, self).__init__(self.get_country(), self.session)

    def get_country(self):
        cur_domain = urlparse(self.url).netloc
        for domain_item in AMAZON_DOMAIN:
            domain = urlparse(AMAZON_DOMAIN[domain_item]).netloc
            if cur_domain == domain:
                return domain_item
        return ''

    def start(self):
        if not self.proxy:
            return -8
        results = self.change_address(self.proxy)
        if type(results) == int:
            return results
        review_response = self.session.get_amazon_data(self.url, self.proxy)
        review_response = request_message(review_response, 'txt')
        if not review_response:
            return -9
        review_dispose = AmazonReviewDispose(self.get_country(), review_response)
        if is_robot(review_dispose.get_selector()):
            return -6
        data = review_dispose.dispose()
        data['review_url'] = self.url
        return data


class BlackListMain:
    def __init__(self, data):
        self.data = data
        self.session = BlackListRequests(data)
        self.proxy = Proxy().get_proxies()

    def start(self):
        if not self.proxy:
            return -8
        black_response = self.session.get_black_list(self.proxy)
        black_response = request_message(black_response, 'txt')
        if not black_response:
            return -9
        black_dispose = BlackListDispose(black_response)
        data = black_dispose.dispose()
        data['url'] = self.session.get_black_list_url()
        return data
