# 查找最大页数
MAX_PAGE = 2

# 判断差评
BAD_STARS = 3

# 首页无差评条件 好评要达到
NICE_REVIEW_NUM = 10

# 请求状态 status
REQUEST_STATUS = ({
    'code': -1,
    'msg': '参数不对'
}, {
    'code': -2,
    'msg': 'review不是一个 list 数据'
}, {
    'code': -3,
    'msg': '首页无差评条件达成失败'
}, {
    'code': -4,
    'msg': '连接超时'
}, {
    'code': -5,
    'msg': '请求数据失败'
}, {
    'code': -6,
    'msg': '机器人验证'
}, {
    'code': -7,
    'msg': '地址更换失败'
}, {
    'code': 200,
    'msg': '请求成功'
})

# amazon domain
AMAZON_DOMAIN = {
    'AE': 'https://www.amazon.ae',
    'CN': 'https://www.amazon.cn',
    'JP': 'https://www.amazon.co.jp',
    'US': 'https://www.amazon.com',
    'UK': 'https://www.amazon.co.uk',
    'FR': 'https://www.amazon.fr',
    'DE': 'https://www.amazon.de',
    'ES': 'https://www.amazon.es',
    'IT': 'https://www.amazon.it',
    'CA': 'https://www.amazon.ca',
    'IN': 'https://www.amazon.in',
    'AU': 'https://www.amazon.com.au',
    'GB': 'https://www.amazon.co.uk',
    'MX': 'https://www.amazon.com.mx',
    'BR': 'https://www.amazon.com.br'
    # 'SG': 'https://www.amazon.com.sg'
}

AMAZON_ZIPCODE = {
    'AE': 'Fujairah',
    'CN': '615299',
    'JP': '922-0337',
    'US': '60616',
    'UK': 'EC1A 1HQ',
    'FR': '97460',
    'DE': '01731',
    'ES': '28039',
    'IT': '00144',
    'CA': 'T0H 4E0',
    'IN': '110034',
    'AU': '2060',
    'GB': 'EC1A 1HQ',
    'MX': '02860',
    'BR': '40301-110'
    # 'SG': ''
}

# 获取token
RE_TOKEN = r'token":"(.*?)"'

# 获取types
RE_TYPE = r'enabledContributionTypes":(\[.*?\])'

# 获取name
RE_NAME = r'"nameHeaderData":{"name":"(.*?)"'

# 获取排名
RE_RANK = r'"rank":"(.*?)"'

# 获取评论
RE_STARS = r'(\d+)'

# 获取点赞数
RE_HELPFUL = r'(\d+)'

# 语言
LANG_CODE = {
    'CN': 'zh_CN',
    'US': 'en_US'
}