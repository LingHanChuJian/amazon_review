import re
from lxml import etree
from setting import *
from urllib import parse


def get_data(data):
    return ''.join(data).strip().replace('\n', '') if data else ''


class AmazonDispose:
    def __init__(self, content):
        self.content = content

    def get_token(self):
        token = re.search(RE_TOKEN, self.content, re.M)
        return '' if not token else token.group(1)

    def get_type(self):
        types = re.search(RE_TYPE, self.content, re.M)
        return '' if not types else types.group(1)

    def get_name(self):
        name = re.search(RE_NAME, self.content, re.M)
        return '' if not name else name.group(1)

    def get_rank(self):
        rank = re.search(RE_RANK, self.content, re.M)
        return '' if not rank else rank.group(1)

    def get_selector(self):
        return etree.HTML(self.content)


class AmazonBadDispose:
    def __init__(self, country, data, count):
        self.data = data
        self.count = count
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
            review_stars = re.search(RE_STARS, get_data(review_stars))
            if review_stars:
                review_stars = review_stars.group(1)
            else:
                review_stars = 0
            review_helpful = review.xpath('div/div/div[contains(@class, "review-comments")]/div'
                                          '/span[@data-hook="review-voting-widget"]/div[1]'
                                          '/span[@data-hook="helpful-vote-statement"]//text()')
            review_helpful = re.search(RE_HELPFUL, get_data(review_helpful))
            if review_helpful:
                review_helpful = int(review_helpful.group(1))
            else:
                review_helpful = 0
            if self.count == 1:
                if int(review_stars) > BAD_STARS:
                    self.nice_review_num += 1
                else:
                    review_row['type'] = 2
                    review_row['href'] = self.get_review_details_url(review_href)
                    review_row['helpful'] = review_helpful
            elif self.count == 2 or self.count == 4:
                if int(review_stars) < BAD_STARS:
                    review_row['type'] = 2
                    review_row['href'] = self.get_review_details_url(review_href)
                    review_row['helpful'] = review_helpful
            elif self.count == 3:
                if int(review_stars) > BAD_STARS:
                    self.nice_review_num += 1
                    review_row['type'] = 1
                    review_row['href'] = self.get_review_details_url(review_href)
                    review_row['helpful'] = review_helpful
                else:
                    review_row['type'] = 2
                    review_row['href'] = self.get_review_details_url(review_href)
                    review_row['helpful'] = review_helpful
            if review_row:
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
            if value == get_data(param) and key == 'CN':
                return True
        return False

    def is_next_page(self):
        next_page = self.selector.xpath('//li[contains(@class, "a-last")]/@class')
        if next_page:
            return False if 'a-disabled' in next_page else True
        else:
            return False

    def get_review_details_url(self, data):
        return '%s%s' % (AMAZON_DOMAIN[self.country.upper()], get_data(data)) if data else ''


class AmazonFollowDispose:
    def __init__(self, data):
        self.selector = etree.HTML(data)

    def dispose(self):
        follow_offer = []
        seller_data = self.selector.xpath('//div[contains(@class, "olpSellerColumn")]')
        for seller in seller_data:
            seller_url = seller.xpath('h3[contains(@class, "olpSellerName")]/span/a/@href')
            seller_name = seller.xpath('h3[contains(@class, "olpSellerName")]/span/a//text()')
            if seller_url:
                data = {'seller_id': self.get_seller(seller_url), 'seller_name': get_data(seller_name)}
                follow_offer.append(data)
        return follow_offer

    def is_next_page(self):
        next_page = self.selector.xpath('//li[contains(@class, "a-last")]/@class')
        if next_page:
            return False if 'a-disabled' in next_page else True
        else:
            return False

    def get_next_page(self):
        if self.is_next_page():
            next_page = self.selector.xpath('//li[contains(@class, "a-last")]/a/@href')
            return get_data(next_page)

    def get_selector(self):
        return self.selector

    @staticmethod
    def get_seller(data):
        params = parse.parse_qs(parse.urlparse(get_data(data)).query)
        return get_data(params['seller'])
