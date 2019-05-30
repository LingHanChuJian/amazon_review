import threading
from queue import Queue
from flask import Flask, request
from requests.exceptions import ConnectTimeout
from urllib3.exceptions import ConnectTimeoutError, MaxRetryError

from utils.utils import wait, result
from main import AmazonMain, AmazonReviewsMain


app = Flask(__name__)


# 获取个人主页对应asin评论
@app.route('/api/user_review', methods=['post'])
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
            wait()
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
    except [ConnectTimeout, ConnectTimeoutError, MaxRetryError]:
        return result(-4)


# 首页无差评达成条件
@app.route('/api/not_bad_review', methods=['post'])
def app_not_bad_review():
    try:
        data = {
            'review_id': request.form['review_id'],
            'country': request.form['country'],
            'asin': request.form['asin']
        }
        q = Queue()
        t = threading.Thread(target=start_all_review_download, args=(data, q))
        t.setDaemon(True)
        t.start()
        res = q.get()
        if type(res) == int:
            return result(res)
        return result(200, res)
    except KeyError as e:
        print(e)
        return result(-1)
    except (ConnectTimeout, ConnectTimeoutError, MaxRetryError) as e:
        print(e)
        return result(-4)


def start_download(item, q):
    review_main = AmazonMain(item)
    review_data = review_main.start()
    if not review_data:
        review_data = {'review_order_id': item['review_order_id']}
    q.put(review_data)


def start_all_review_download(data, q):
    all_review_main = AmazonReviewsMain(data)
    all_review_data = all_review_main.start()
    q.put(all_review_data)


if __name__ == '__main__':
    app.run(threaded=True)
