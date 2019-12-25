import requests
from fake_useragent import UserAgent

from utils.api import *
from utils.utils import get_amazon_domain


class AmazonRequests:
    def __init__(self, directed_id, country):
        self.country = country
        self.directedId = directed_id
        self.session = requests.Session()

    def get_user_url(self):
        return USER_URL.format(domain=get_amazon_domain(self.country), directedId=self.directedId)

    def get_review_url(self):
        return REVIEWS_URL.format(domain=get_amazon_domain(self.country))

    def get_amazon_data(self, url, header, param=None):
        response = self.session.get(url=url, headers=header, params=param, timeout=20)
        response.encoding = 'utf-8'
        return response

    def get_review_param(self, token, types, next_page=''):
        reviews_param = dict()
        reviews_param['token'] = token
        reviews_param['nextPageToken'] = next_page
        reviews_param['filteredContributionTypes'] = types
        reviews_param['directedId'] = 'amzn1.account.%s' % self.directedId
        return reviews_param


class AmazonUserReviewRequests:

    def __init__(self, country, asin, count):
        self.page = 1
        self.asin = asin
        self.country = country
        self.count = count
        self.ua = UserAgent().random
        self.session = requests.session()

    def get_reviews_url(self):
        return ALL_REVIEWS_URL.format(domain=get_amazon_domain(self.country), asin=self.asin)

    def get_amazon_data(self, is_lang=False, is_bad=True):
        all_reviews_header['user-agent'] = self.ua
        response = self.session.get(url=self.get_reviews_url(), headers=all_reviews_header,
                                    params=self.get_all_review_param(is_lang, is_bad), timeout=20)
        response.encoding = 'utf-8'
        return response

    def get_all_review_param(self, is_lang=False, is_bad=True):
        param = all_review_param.copy()
        param['pageNumber'] = self.get_page()
        if is_lang and self.country.upper() == 'US':
            param['filterByLanguage'] = 'en_US'
        if self.count == 3 and not is_bad:
            param['filterByStar'] = 'five_star'
        return param

    def next_page(self):
        self.page += 1

    def get_page(self):
        return self.page


class DirectBase:
    def __init__(self, country):
        self.country = country
        self.ua = UserAgent().random
        self.session = requests.session()

    def get_requests_data(self, url, header):
        response = self.session.get(url=url, headers=header, timeout=20)
        response.encoding = 'utf-8'
        return response

    def post_data(self, url, header, data):
        response = self.session.post(url=url, data=data, headers=header, timeout=20)
        response.encoding = 'utf-8'
        return response

    def post_address_change(self, data):
        cur_header = address_header.copy()
        cur_header['user-agent'] = self.ua
        return self.post_data(AMAZON_ADDRESS.format(domain=get_amazon_domain(self.country)), cur_header, data)


class AmazonFollowRequests(DirectBase):
    def __init__(self, country, asin):
        self.asin = asin
        self.country = country
        super(AmazonFollowRequests, self).__init__(self.country)

    def get_follow_url(self):
        return ASIN_FOLLOW_OFFER.format(domain=get_amazon_domain(self.country), asin=self.asin)

    def get_amazon_data(self, url):
        cur_header = asin_follow_offer_header.copy()
        cur_header['user-agent'] = self.ua
        return self.get_requests_data(url, cur_header)


class AmazonProductDetailsRequests(DirectBase):

    def get_amazon_data(self, url):
        cur_header = product_details_header.copy()
        cur_header['user-agent'] = self.ua
        return self.get_requests_data(url, cur_header)


class AmazonReviewRequests(DirectBase):

    def get_amazon_data(self, url):
        cur_header = review_header.copy()
        cur_header['user-agent'] = self.ua
        return self.get_requests_data(url, cur_header)
