# 查找最大页数
MAX_PAGE = 5

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
    'msg': '请求amazon主頁数据失败'
}, {
    'code': -6,
    'msg': '机器人验证'
}, {
    'code': -7,
    'msg': '地址更换失败'
}, {
    'code': -8,
    'msg': '获取代理失败'
}, {
    'code': -9,
    'msg': '请求頁面数据失败'
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
    'AE': 'AE',
    'CN': 'CN',
    'JP': 'JP',
    'US': 'UM',
    'UK': 'GB',
    'FR': 'FR',
    'DE': 'DE',
    'ES': 'ES',
    'IT': 'IT',
    'CA': 'CA',
    'IN': 'IN',
    'AU': 'AU',
    'GB': 'GB',
    'MX': 'MX',
    'BR': 'BR'
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

# 获取链接里面的ASIN
RE_URL_ASIN = r'\/(dp|product)\/((.*)\/|.*)'

# 获取价格
RE_PRICE = RE_PRODUCT_STAR = RE_PRODUCT_REVIEW = r'([0-9,.]+)'

# 替换指定字符串
RE_IMAGE_URL = r'_(.*)_'

# 个人主页视频处理
RE_VIDEOS = r'\[\[VIDEOID:.*\]\]'

# 语言
LANG_CODE = {
    'CN': 'zh_CN',
    'US': 'en_US'
}

FR_MONTH = {
    "janvier": "January",
    "février": "February",
    "mars": "March",
    "avril": "April",
    "mai": "May",
    "juin": "June",
    "juillet": "July",
    "août": "August",
    "septembre": "September",
    "octobre": "October",
    "novembre": "November",
    "décembre": "December"
}

MX_MONTH = ES_MONTH = {
    "enero": "January",
    "febrero": "February",
    "marzo": "March",
    "abril": "April",
    "mayo": "May",
    "junio": "June",
    "julio": "July",
    "agosto": "August",
    "septiembre": "September",
    "octubre": "October",
    "noviembre": "November",
    "diciembre": "December"
}

IT_MONTH = {
    "gennaio": "January",
    "febbraio": "February",
    "marzo": "March",
    "aprile": "April",
    "maggio": "May",
    "giugno": "June",
    "luglio": "July",
    "agosto": "August",
    "settembre": "September",
    "ottobre": "October",
    "novembre": "November",
    "dicembre": "December"
}

DE_MONTH = {
    "Januar": "January",
    "Februar": "February",
    "März": "March",
    "April": "April",
    "Mai": "May",
    "Juni": "June",
    "Juli": "July",
    "August": "August",
    "September": "September",
    "Oktober": "October",
    "November": "November",
    "Dezember": "December"
}

TIME_CODE = {
    'US': {'format': '%B%d,%Y', 'replace': 'Reviewed in the United States on'},
    'AE': '%B%d,%Y',
    'CN': '%Y年%m月%d日',
    'JP': {'format': '%Y年%m月%d日', 'replace': 'に日本でレビュー済み'},
    'UK': {'format': '%d%B%Y', 'replace': 'Reviewed in the United Kingdom on'},
    'FR': {'MapMonth': FR_MONTH, 'format': '%d%B%Y', 'replace': 'Commenté en France le'},
    'DE': {'MapMonth': DE_MONTH, 'format': '%d.%B%Y', 'replace': 'Rezension aus Deutschland vom'},
    'ES': {'MapMonth': ES_MONTH, 'format': '%d%B%Y', 'replace': ['Revisado en España el', 'de']},
    'IT': {'MapMonth': IT_MONTH, 'format': '%d%B%Y', 'replace': 'Recensito in Italia il'},
    'CA': {'format': '%B%d,%Y', 'replace': 'Reviewed in Canada on'},
    'IN': {'format': '%d%B%Y', 'replace': 'Reviewed in India on'},
    'AU': {'format': '%d%B%Y', 'replace': 'Reviewed in Australia on'},
    'GB': {'format': '%d%B%Y', 'replace': 'Reviewed in the United Kingdom on'},
    'MX': {'MapMonth': MX_MONTH, 'format': '%d%B%Y', 'replace': ['Revisado en México el', 'de']}
    # 'SG': 'https://www.amazon.com.sg'
}

STANDARD_TIME = ''

MAX_PROXY_REQUESTS_NUM = 3

MAX_PROXY_POOL_NUM = {
    'AE': 0,
    'CN': 0,
    'JP': 0,
    'US': 0,
    'UK': 0,
    'FR': 0,
    'DE': 0,
    'ES': 0,
    'IT': 0,
    'CA': 0,
    'IN': 0,
    'AU': 0,
    'GB': 0,
    'MX': 0,
    'BR': 0
    # 'SG': 'https://www.amazon.com.sg'
}

# MAX_PROXY_POOL_NUM = {
#     'AE': 0,
#     'CN': 0,
#     'JP': 0,
#     'US': 1,
#     'UK': 0,
#     'FR': 0,
#     'DE': 0,
#     'ES': 0,
#     'IT': 0,
#     'CA': 0,
#     'IN': 0,
#     'AU': 0,
#     'GB': 0,
#     'MX': 0,
#     'BR': 0
#     # 'SG': 'https://www.amazon.com.sg'
# }

# 60秒扫描代理一次
SCANNING_TIME = 60

# PROXY_PACK = 80427
