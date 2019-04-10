import time
import json
import random
import threading
from queue import Queue
from flask import Flask, request

from main import AmazonMain
from setting import REQUEST_STATUS

app = Flask(__name__)


@app.route('/api', methods=['post'])
def app_review():
    try:
        review = eval(request.form['review'])
        thread_list = list()
        q = Queue()
        for item in review:
            t = threading.Thread(target=start_download, args=(item, q))
            t.setDaemon(True)
            t.start()
            thread_list.append(t)
            random_time = random.randint(5, 10)
            print('等待时间 %s' % random_time)
            time.sleep(random_time)
        else:
            review_list = list()
            for thread in thread_list:
                thread.join()
            for _ in range(len(thread_list)):
                review_list.append(q.get())
            else:
                return result(200, review_list)
    except KeyError:
        return result(-1)
    except SyntaxError and NameError:
        return result(-2)


def result(code, data=None):
    res = {'code': code, 'result': 'err'}
    if data:
        res['result'] = data
    for item in REQUEST_STATUS:
        if item['code'] == code:
            res['msg'] = item['msg']
    return json.dumps(res)


def start_download(item, q):
    review_main = AmazonMain(item)
    review_data = review_main.start()
    if not review_data:
        review_data = {'review_order_id': item['review_order_id']}
    q.put(review_data)


if __name__ == '__main__':
    app.run(threaded=True)
