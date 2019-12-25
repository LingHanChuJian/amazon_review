import threading
from queue import Queue
from flask import Flask, request

from requests.exceptions import ConnectTimeout
from urllib3.exceptions import ConnectTimeoutError, MaxRetryError

from utils.utils import wait, result
from main import *


app = Flask(__name__)


# 获取评论链接的评论数据
@app.route('/api/review', methods=['post'])
def app_review():
    try:
        url = request.form['url']
        q = Queue()
        t = threading.Thread(target=start_review_download, args=(url, q))
        t.setDaemon(True)
        t.start()
        res = q.get()
        if type(res) == int:
            return result(res)
        return result(200, res)
    except KeyError as e:
        print(e)
        return result(-1)


# 获取个人主页对应asin评论
@app.route('/api/user_review', methods=['post'])
def app_user_review():
    try:
        review = eval(request.form['review'])
        thread_list = list()
        q = Queue()
        for item in review:
            t = threading.Thread(target=start_user_review_download, args=(item, q))
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
    except (ConnectTimeout, ConnectTimeoutError, MaxRetryError):
        return result(-4)


# 首页无差评达成条件
@app.route('/api/not_bad_review', methods=['post'])
def app_not_bad_review():
    try:
        data = {
            'country': request.form['country'],
            'asin': request.form['asin'],
            'count': int(request.form['count'])
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


@app.route('/api/asin_follow_offer', methods=['post'])
def app_asin_follow_offer():
    try:
        data = {
            'country': request.form['country'],
            'asin': request.form['asin']
        }
        q = Queue()
        t = threading.Thread(target=start_follow_offer_download, args=(data, q))
        t.setDaemon(True)
        t.start()
        res = q.get()
        if type(res) == int:
            return result(res)
        return result(200, res)
    except KeyError as e:
        print(e)
        return result(-1)


@app.route('/api/product_details', methods=['post'])
def app_product_details():
    try:
        url = request.form['url']
        q = Queue()
        t = threading.Thread(target=start_product_details_download, args=(url, q))
        t.setDaemon(True)
        t.start()
        res = q.get()
        if type(res) == int:
            return result(res)
        return result(200, res)
    except KeyError as e:
        print(e)
        return result(-1)


def start_user_review_download(item, q):
    review_main = AmazonMain(item)
    review_data = review_main.start()
    if not review_data:
        review_data = {'review_order_id': item['review_order_id']}
    q.put(review_data)


def start_all_review_download(data, q):
    try:
        all_review_main = AmazonReviewsMain(data)
        all_review_data = all_review_main.start()
        print('差评')
        print(all_review_data)
        if all_review_data and data['count'] == 3:
            all_review_main.set_bad(False)
            all_review_data = all_review_main.start()
            print('好评')
            print(all_review_data)
        q.put(all_review_data)
    except Exception as e:
        print(e)
        q.put(-4)


def start_follow_offer_download(data, q):
    # try:
    follow_offer_main = AmazonFollowMain(data)
    follow_offer_data = follow_offer_main.start()
    print(follow_offer_data)
    q.put(follow_offer_data)
    # except Exception as e:
    #     print(e)
    #     q.put(-4)


def start_product_details_download(data, q):
    product_details_main = AmazonProductDetailsMain(data)
    product_details_data = product_details_main.start()
    q.put(product_details_data)


def start_review_download(data, q):
    review_main = AmazonReviewMain(data)
    review_data = review_main.start()
    q.put(review_data)


if __name__ == '__main__':
    app.run(threaded=True)
