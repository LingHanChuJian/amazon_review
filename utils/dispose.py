import re
from lxml import etree
from setting import *


class AmazonDispose:
    def __init__(self, content):
        self.content = content

    def get_token(self):
        token = re.search(RE_TOKEN, self.content, re.M)
        if not token:
            return ''
        return token.group(1)

    def get_type(self):
        types = re.search(RE_TYPE, self.content, re.M)
        if not types:
            return ''
        return types.group(1)

    def get_name(self):
        name = re.search(RE_NAME, self.content, re.M)
        if not name:
            return ''
        return name.group(1)

    def get_rank(self):
        rank = re.search(RE_RANK, self.content, re.M)
        if not rank:
            return ''
        return rank.group(1)

    def get_selector(self):
        return etree.HTML(self.content)


class AmazonBadDispose:
    def __init__(self, country, data):
        self.data = data
        self.country = country
        self.nice_review_num = 0
        self.selector = etree.HTML(data)

    def dispose(self):
        bad_review = []
        review_data = self.selector.xpath('//div[@data-hook="review"]')
        if not review_data:
            return None
        for review in review_data:
            if self.nice_review_num >= NICE_REVIEW_NUM:
                break
            review_row = {}
            review_href = review.xpath('div/div/div[2]/a[@data-hook="review-title"]/@href')
            review_stars = review.xpath('div/div/div[2]/a[@class="a-link-normal"]'
                                        '/i[@data-hook="review-star-rating"]/@class')
            review_stars = re.search(RE_STARS, self.get_data(review_stars))
            if review_stars:
                review_stars = review_stars.group(1)
            else:
                review_stars = 0
            review_helpful = review.xpath('div/div/div[5]/div/span[@data-hook="review-voting-widget"]'
                                          '/div/span[@data-hook="helpful-vote-statement"]//text()')
            review_helpful = re.search(RE_HELPFUL, self.get_data(review_helpful))
            if review_helpful:
                review_helpful = int(review_helpful.group(1))
            else:
                review_helpful = 0
            if int(review_stars) > BAD_STARS:
                self.nice_review_num += 1
            else:
                review_row['href'] = self.get_review_details_url(review_href)
                review_row['helpful'] = review_helpful
                bad_review.append(review_row)
        return bad_review

    def get_nice_review_num(self):
        return self.nice_review_num

    def set_nice_review_num(self, num):
        self.nice_review_num = num

    def get_selector(self):
        return self.selector

    def is_lang(self):
        lang = self.selector.xpath('//select[@id="language-type-dropdown"]')
        if not lang:
            return False
        for item in lang:
            param = item.xpath('option[@selected]/@value')
        for (key, value) in LANG_CODE.items():
            if value == self.get_data(param) and key == 'CN':
                return True
        return False

    def is_next_page(self):
        next_page = self.selector.xpath('//li[contains(@class, "a-last")]/@class')
        if next_page:
            if 'a-disabled' in next_page:
                return False
            else:
                return True
        else:
            return False

    @staticmethod
    def get_data(data):
        if data:
            return ''.join(data).strip().replace('\n', '')
        else:
            return ''

    def get_review_details_url(self, data):
        if data:
            return '%s%s' % (AMAZON_DOMAIN[self.country.upper()], self.get_data(data))
        else:
            return ''
