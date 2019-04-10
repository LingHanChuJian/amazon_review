import requests

from utils.api import *
from setting import AMAZON_DOMAIN


class AmazonRequests:
    def __init__(self, directed_id, country):
        self.country = country
        self.directedId = directed_id
        self.session = requests.Session()

    def get_amazon_domain(self):
        return AMAZON_DOMAIN[self.country.upper()]

    def get_user_url(self):
        return USER_URL.format(domain=self.get_amazon_domain(), directedId=self.directedId)

    def get_review_url(self):
        return REVIEWS_URL.format(domain=self.get_amazon_domain())

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
