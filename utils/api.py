# 用户个人主页
USER_URL = '{domain}/gp/profile/amzn1.account.{directedId}/ref=cm_cr_dp_d_gw_tr'

# 评论接口
REVIEWS_URL = '{domain}/profilewidget/timeline/visitor'

# 评论链接
REVIEWS = '{domain}/gp/customer-reviews/{externalId}?ref=pf_vv_at_pdctrvw_srp'

user_header = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,\
              application/signed-exchange;v=b3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'upgrade-insecure-requests': '1',
    'user-agent': ''
}

reviews_header = {
    'accept': '*/*',
    'user-agent': '',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'x-requested-with': 'XMLHttpRequest'
}

USER_PARAM = {
    'ie': 'UTF*'
}


# 所有评论入口
ALL_REVIEWS_URL = '{domain}/product-reviews/{asin}/ref=cm_cr_arp_d_viewopt_srt'

all_review_param = {
    'ie': 'UTF8',
    'reviewerType': 'all_reviews',
    'sortBy': 'helpful',
    'pageNumber': '',
    'filterByStar': ''
}

all_reviews_header = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;'
              'q=0.8,application/signed-exchange;v=b3',
    'user-agent': '',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'upgrade-insecure-requests': '1'
}

# asin 跟卖信息
AMAZON_ADDRESS = '{domain}/gp/delivery/ajax/address-change.html'

address_data = {
    'locationType': 'LOCATION_INPUT',
    'zipCode': '',
    'storeContext': 'generic',
    'deviceType': 'web',
    'pageType': 'Gateway',
    'actionSource': 'glow'
}

address_header = {
    'accept': 'text/html,*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'x-requested-with': 'XMLHttpRequest',
    'user-agent': ''
}

ASIN_FOLLOW_OFFER = '{domain}/gp/offer-listing/{asin}'

ASIN_FOLLOW_OFFER_NEXT = '{domain}{next_url}'

product_details_header = asin_follow_offer_header = review_header = black_list_header = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,'
              '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': ''
}

# 黑名单
REVIEWS_BLACK_LIST = 'https://mjzj.com/ce-ping-bao-guang-tai/sou-suo?field={field}&query={query}'
