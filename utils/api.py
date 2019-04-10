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
