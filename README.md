## amazon_review
爬取 amazon个人主页指定评论

花了点个把小时, 做了一个到amazon个人主页爬出指定asin的评论

## 使用方法

1. 本项目采用 pipenv 作为 python 虚拟环境和依赖管理工具

2. 执行一下命令运行本项目

```
pipenv install
pipenv shell
python app_review.py
```

3.执行post请求

### 查找个人主页指定asin的评论

http://127.0.0.1:5000/api/user_review

### 达成产品首页无差评条件

http://127.0.0.1:5000/api/not_bad_review

### 爬取跟卖店铺信息
http://127.0.0.1:5000/api/asin_follow_offer

### 抓取产品详情信息
http://127.0.0.1:5000/api/product_details

## user_review 参数

`review` string类型的JSON数组
> [{'review_order_id': '', 'amazon_buyer_url': '', 'country': '', 'asin': ''}]

> review_order_id  用来标识的唯一 id , 随便填写

> amazon_buyer_url  amazon 上 directedId 需要去掉 amzn1.account.

> 例子: https://www.amazon.com/gp/profile/amzn1.account.AHP3GBGMQ7HBYZCJWUJG72JFR22A?ie=UTF8&ref_=ya_d_l_profile

> amazon_buyer_url 为 AHP3GBGMQ7HBYZCJWUJG72JFR22A

> country 国家简码 US CN 等等

> asin amazon产品 id

## not_bad_review 参数

`country`   国家简码

`asin`      amazon产品 id

`count`     获取次数

## asin_follow_offer 参数

`country`   国家简码

`asin`      amazon产品 id

## product_details 参数
`url`       amazon产品链接

## 展示

![review](https://github.com/LingHanChuJian/amazon_review/blob/master/img/review.png)

![not_bad_review](https://github.com/LingHanChuJian/amazon_review/blob/master/img/bad_review.png)

![asin_follow_offer](https://github.com/LingHanChuJian/amazon_review/blob/master/img/follow_offer.png)

![product_details](https://github.com/LingHanChuJian/amazon_review/blob/master/img/product_details.png)