import json
import time
import random
from setting import AMAZON_DOMAIN, REQUEST_STATUS


def get_amazon_domain(country):
    return AMAZON_DOMAIN[country.upper()]


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False


def is_robot(selector):
    robot = selector.xpath('//form[@action="/errors/validateCaptcha"]')
    return True if robot else False


def request_message(response, mode):
    print(response.status_code)
    if response.status_code != 200:
        return None
    if mode == 'json':
        return response.json()
    elif mode == 'txt':
        return response.text


def wait():
    random_time = random.randint(1, 3)
    print('等待时间 %s' % random_time)
    time.sleep(random_time)


def result(code, data=None):
    res = {'code': code, 'result': 'err'}
    if data:
        res['result'] = data
    for item in REQUEST_STATUS:
        if item['code'] == code:
            res['msg'] = item['msg']
    return json.dumps(res)