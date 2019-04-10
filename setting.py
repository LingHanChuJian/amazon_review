import os

BASH_DIR = os.path.dirname(os.path.abspath(__file__))

# 请求状态 status
REQUEST_STATUS = ({
    'code': -1,
    'msg': 'review未获取到值'
}, {
    'code': -2,
    'msg': 'review不是一个 list 数据'
}, {
    'code': 200,
    'msg': '请求成功'
})

# amazon domain
AMAZON_DOMAIN = {
    "CN": "https://www.amazon.cn",
    "JP": "https://www.amazon.co.jp",
    "US": "https://www.amazon.com",
    "UK": "https://www.amazon.co.uk",
    "FR": "https://www.amazon.fr",
    "DE": "https://www.amazon.de",
    "ES": "https://www.amazon.es",
    "IT": "https://www.amazon.it",
    "CA": "https://www.amazon.ca",
    "IN": "https://www.amazon.in",
    "AU": "https://www.amazon.com.au",
    "GB": "https://www.amazon.co.uk"
}

# 获取token
RE_TOKEN = r'token":"(.*?)"'

# 获取types
RE_TYPE = r'enabledContributionTypes":(\[.*?\])'

# 获取name
RE_NAME = r'"nameHeaderData":{"name":"(.*?)"'
