import time
import requests
from setting import MAX_PROXY_NUM, MAX_PROXY_REQUESTS_NUM
from utils.utils import request_message

proxy_url = 'http://http.tiqu.alicdns.com/getip3?num={num}&type=2&pro=&city=0&yys=0&port=11&time=1&ts=1&ys=0&cs=0' \
            '&lb=1&sb=0&pb=4&mr=2&regions=&gm=4'

proxies_mate = 'https://{host}:{port}'


class Proxy:
    def __init__(self):
        self.agents = []
        self.requests_num = 0

    def agent_pool(self):
        if self.agents:
            return self.agents.pop()
        response = requests.get(proxy_url.format(num=MAX_PROXY_NUM), timeout=20)
        response.encoding = 'utf-8'
        response = request_message(response, 'json')
        if 'success' in response and response['success']:
            self.agents.extend(response['data'])
            return self.agents.pop()
        else:
            self.requests_num += 1
            if self.requests_num < MAX_PROXY_REQUESTS_NUM:
                time.sleep(3)
                return self.agent_pool()
            else:
                return None

    def get_proxies(self):
        agent = self.agent_pool()
        proxies = {
            'http': proxies_mate.format(host=agent['ip'], port=agent['port']),
            'https': proxies_mate.format(host=agent['ip'], port=agent['port'])
        } if agent else None
        print(proxies)
        return proxies
