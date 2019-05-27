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


class AmazonReviewRequests:

    def __init__(self, review_id, country, asin):
        self.page = 1
        self.asin = asin
        self.id = review_id
        self.country = country
        self.ua = UserAgent().random
        self.session = requests.session()

    def get_reviews_url(self):
        return ALL_REVIEWS_URL.format(domain=get_amazon_domain(self.country), asin=self.asin)

    def get_amazon_data(self, is_lang=False):
        all_review_param['pageNumber'] = self.get_page()
        if is_lang and self.country.upper() == 'US':
            all_review_param['filterByLanguage'] = 'en_US'
        all_reviews_header['user-agent'] = self.ua
        response = \
            self.session.get(url=self.get_reviews_url(), headers=all_reviews_header, params=all_review_param, timeout=20)
        response.encoding = 'utf-8'
        return response

    def next_page(self):
        self.page += 1

    def get_page(self):
        return self.page
