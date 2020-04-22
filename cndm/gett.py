import os
import random
from time import sleep, time

import requests
from bs4 import BeautifulSoup

from cndm.read import seq_gen
from tk import translate

url_base = r'http://www.chinadaily.com.cn/world/asia_pacific/page_{page}.html'

# urls = [url_base.format(page=i) for i in range(1, 10)]
urls = [url_base.format(page=i) for i in range(1, 3)]

urls_css = r'#left > div > span > h4 > a'

# mkdirs
if not os.path.exists('transed'):
    os.mkdir('transed')
if not os.path.exists('data'):
    os.mkdir('data')


def get_base(url):
    r = requests.get(url)
    # print(r.text)
    soup = BeautifulSoup(r.text, "lxml")

    a = soup.select(urls_css)

    # #left > div > span > h4 > a
    sub_urls = ['http:' + aa.get('href') for aa in a]
    yield sub_urls


# sub_urls = []
#
# for u in urls:
#     sub_urls.extend(get_base(u))


def get_sub(url, show=True):
    print('-' * 20)
    # print('Getting news:', url)

    # get news
    t0 = time()
    r = requests.get(url)
    # print(r.text)
    soup = BeautifulSoup(r.text, "lxml")
    title = soup.select_one('head > title').text
    # //*[@id="Content"]/p[1]
    content = [c.text + '\n' for c in soup.select('#Content lengths> p')]
    title = title.split('-')[0][:-1]
    with open('data/{}.txt'.format(title), 'w', encoding='utf-8') as f:
        f.writelines(content)
    # control the speed
    # sleep(random.randint(0, 1))
    t1 = time()
    sleep(random.randint(0, 1))
    t20 = time()
    # translate
    tmp = []
    trans_cnt = 0
    for s in seq_gen('data/{}.txt'.format(title), 4900):
        if show:
            print(s)
            print(len(s))
            print()
            print('-' * 10)
        res = translate(s)
        sleep(1.5)
        trans_cnt += 1
        tmp.append(res)
    t2 = time()
    transed = ''.join(tmp)
    if show:
        print(transed)
        print("=" * 20)
    with open('transed/{}.transed.txt'.format(title), mode='w', encoding='utf-8') as f:
        f.write(transed)
    # t2 = time()
    t_news = t1 - t0
    t_trans = t2 - t20 - 1.5 * trans_cnt
    return t_news, t_trans


def get_data(page_count, end=None):
    if end is not None:
        r = range(page_count, end)
    else:
        r = range(1, page_count + 1)
    t_a_n, t_a_t = 0, 0
    for page in r:
        print('*' * 10, 'Getting base page:', page, '*' * 10, )
        for sub_urls in get_base(url_base.format(page=page)):
            for news_url in sub_urls:
                tn, tt = get_sub(news_url, show=False)
                t_a_n += tn
                t_a_t += tt
                # print(tn, tt)
                print(
                    '   Current: News: {:10.3f}s, Trans: {:10.3f}s\nTime total:\tNews: {:10.3f}s, Trans: {:10.3f}s'.format(
                        tn, tt,
                        t_a_n,
                        t_a_t,
                    ))
                sleep(random.randint(1, 5))
        sleep(random.randint(2, 5))


get_data(1, 11)
