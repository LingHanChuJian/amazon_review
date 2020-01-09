import time
import requests
from setting import MAX_PROXY_NUM, PROXY_PACK
from utils.utils import request_message

proxy_url = 'http://webapi.http.zhimacangku.com/getip?num={num}&type=2&pro=&city=0&yys=0&port=1&pack={pack}' \
            '&ts=1&ys=0&cs=1&lb=1&sb=0&pb=4&mr=2&regions='

proxies_mate = 'http://{host}:{port}'


class Proxy:
    def __init__(self):
        self.agents = []

    def agent_pool(self):
        if self.agents:
            return self.agents.pop()
        response = requests.get(proxy_url.format(num=MAX_PROXY_NUM, pack=PROXY_PACK), timeout=20)
        response.encoding = 'utf-8'
        response = request_message(response, 'json')
        print(response)
        if 'success' in response and response['success']:
            self.agents.extend(response['data'])
            return self.agents.pop()
        else:
            time.sleep(3)
            return self.agent_pool()

    def get_proxies(self):
        agent = self.agent_pool()
        return {
            'http': proxies_mate.format(host=agent['ip'], port=agent['port']),
        }
