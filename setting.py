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

# 获取链接里面的ASIN
RE_URL_ASIN = r'\/dp\/((.*)\/|.*)'

# 获取价格
RE_PRICE = r'([0-9,.]+)'

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
    'US': '%B%d,%Y',
    'AE': '%B%d,%Y',
    'CN': '%Y年%m月%d日',
    'JP': '%Y年%m月%d日',
    'UK': '%d%B%Y',
    'FR': {'MapMonth': FR_MONTH, 'format': '%d%B%Y'},
    'DE': {'MapMonth': DE_MONTH, 'format': '%d.%B%Y'},
    'ES': {'MapMonth': ES_MONTH, 'format': '%d%B%Y', 'replace': 'de'},
    'IT': {'MapMonth': IT_MONTH, 'format': '%d%B%Y'},
    'CA': '%B%d,%Y',
    'IN': '%d%B%Y',
    'AU': '%d%B%Y',
    'GB': '%d%B%Y',
    'MX': {'MapMonth': MX_MONTH, 'format': '%d%B%Y', 'replace': 'de'}
    # 'SG': 'https://www.amazon.com.sg'
}

STANDARD_TIME = ''

MAX_PROXY_NUM = 1

PROXY_PACK = 80427
