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
},{
    'code': -4,
    'msg': '连接超时'
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
    'MX': 'https://www.amazon.com.mx'
    # 'SG': 'https://www.amazon.com.sg'
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