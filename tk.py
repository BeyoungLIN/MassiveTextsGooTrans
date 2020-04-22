import json
import os
from time import sleep

import execjs  # 必须，需要先用pip 安装，用来执行js脚本
import requests

from cndm.read import seq_gen


class Py4Js():
    def __init__(self):
        self.ctx = execjs.compile(""" 
    function TL(a) { 
    var k = ""; 
    var b = 406644; 
    var b1 = 3293161072;       
    var jd = "."; 
    var $b = "+-a^+6"; 
    var Zb = "+-3^+b+-f";    
    for (var e = [], f = 0, g = 0; g < a.length; g++) { 
        var m = a.charCodeAt(g); 
        128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023), 
        e[f++] = m >> 18 | 240, 
        e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224, 
        e[f++] = m >> 6 & 63 | 128), 
        e[f++] = m & 63 | 128) 
    } 
    a = b; 
    for (f = 0; f < e.length; f++) a += e[f], 
    a = RL(a, $b); 
    a = RL(a, Zb); 
    a ^= b1 || 0; 
    0 > a && (a = (a & 2147483647) + 2147483648); 
    a %= 1E6; 
    return a.toString() + jd + (a ^ b) 
  };      
  function RL(a, b) { 
    var t = "a"; 
    var Yb = "+"; 
    for (var c = 0; c < b.length - 2; c += 3) { 
        var d = b.charAt(c + 2), 
        d = d >= t ? d.charCodeAt(0) - 87 : Number(d), 
        d = b.charAt(c + 1) == Yb ? a >>> d: a << d; 
        a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d 
    } 
    return a 
  } 
 """)

    def getTk(self, text):
        return self.ctx.call("TL", text)


def buildUrl(text, tk):
    baseUrl = 'https://translate.google.cn/translate_a/single'
    baseUrl += '?client=t&'
    baseUrl += 's1=auto&'
    baseUrl += 't1=zh-CN&'
    baseUrl += 'h1=zh-CN&'
    baseUrl += 'dt=at&'
    baseUrl += 'dt=bd&'
    baseUrl += 'dt=ex&'
    baseUrl += 'dt=ld&'
    baseUrl += 'dt=md&'
    baseUrl += 'dt=qca&'
    baseUrl += 'dt=rw&'
    baseUrl += 'dt=rm&'
    baseUrl += 'dt=ss&'
    baseUrl += 'dt=t&'
    baseUrl += 'ie=UTF-8&'
    baseUrl += 'oe=UTF-8&'
    baseUrl += 'otf=1&'
    baseUrl += 'pc=1&'
    baseUrl += 'ssel=0&'
    baseUrl += 'tsel=0&'
    baseUrl += 'kc=2&'
    baseUrl += 'tk=' + str(tk) + '&'
    baseUrl += 'q=' + text
    return baseUrl


js = Py4Js()


def translate(text):
    header = {
        'authority': 'translate.google.cn',
        'method': 'GET',
        'path': '',
        'scheme': 'https',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': '',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)  AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
        'x-client-data': 'CIa2yQEIpbbJAQjBtskBCPqcygEIqZ3KAQioo8oBGJGjygE='
    }
    url = buildUrl(text, js.getTk(text))
    res = ''
    try:
        r = requests.get(url,
                         headers=header
                         )
        result = json.loads(r.text)
        if result[7] != None:
            # 如果我们文本输错，提示你是不是要找xxx的话，那么重新把xxx正确的翻译之后返回
            try:
                correctText = result[7][0].replace('<b><i>', ' ').replace('</i></b>', '')
                print(correctText)
                correctUrl = buildUrl(correctText, js.getTk(correctText))
                correctR = requests.get(correctUrl)
                newResult = json.loads(correctR.text)
                res = newResult[0][0][0]
            except Exception as e:
                print(e)
                res = ""
                for r in result[0]:
                    if r[0] is not None:
                        res += r[0]
                # res=result[0][0][0]
        else:
            res = ""
            for r in result[0]:
                if r[0] is not None:
                    res += r[0]
            # res=result[0][0][0]
    except Exception as e:
        res = ''
        print(url)
        print("翻译" + text + "失败")
        print("错误信息:")
        print(e)
    finally:
        return res


if __name__ == '__main__':
    js = Py4Js()
    # file_object = open('cnn.txt')
    # try:
    #     file_context = file_object.read()  # file_context是一个string，读取完后，就失去了对test.txt的文件引用
    #     # file_context = open(file_object).read().splitlines() #file_context是一个list，每行文本内容是list中的一个元素
    # finally:
    #     file_object.close() # 除了以上方法，也可用with、contextlib都可以打开文件，且自动关闭文件，

    # fp=r"cndm/data/'Edtech' boom transforms learning - World - Chinadaily.com.cn.txt"
    # #
    # fp=r'cndm/cnn.txt'

    fd = "cndm/data"

    for f in os.listdir(fd):
        print(f)
        fn = fd + os.sep + f
        tmp = []
        for s in seq_gen(fn, 4900):
            print(s)
            print(len(s))
            print()
            print('-' * 10)
            res = translate(s)
            sleep(1.5)
            tmp.append(res)
        transed = ''.join(tmp)
        print(transed)
        print("=" * 20)
        if not os.path.exists('transed/'):
            os.mkdir('transed/')
        with open('transed/' + f + 'transed.txt', mode='w', encoding='utf-8') as f:
            f.write(transed)
