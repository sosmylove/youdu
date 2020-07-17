# coding=utf-8
import requests
import time
import random
import time

class sendRequest(object):
    def __init__(self):
        self.flag = True
        self.ua_list = [
                   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1); ",
                   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ",
                   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; MyIE2) ",
                   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; FDM; ",
                   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1 ",
                   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; MyIE2) ",
                   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; BrowserBob) ",
                   "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0 ",
                   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Alexa Toolbar) ",
                   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; TencentTraveler) ",
                   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; zh-cn) Opera 8.0 ",
                   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; zh-cn) Opera 8.01 ",
                   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; zh-cn) Opera 8.50 ",
                   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322) ",
                   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.0.3705) ",
                   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 2.0.40607) ",
                   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322) ",
                   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; DFO-MPO Internet Explorer 6.0) ",
                   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; HCI0449; .NET CLR 1.0.3705) ",
                   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; i-NavFourF; .NET CLR 1.1.4322) ",
                   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Maxthon; ",
                   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Maxthon; .NET CLR 1.1.4322) ",
                   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; MyIE2; .NET CLR 1.1.4322) ",
                   "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322) ",
                   "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; SV1) ",
                   "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1) ",
                   "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.6) Gecko/20040113 ",
                   "Mozilla/5.0 (Windows; U; Windows NT 5.1; rv:1.7.3) Gecko/20040913 Firefox/0.10 ",
                   "Mozilla/5.0 (Windows; U; Windows NT 5.1; rv:1.7.3) Gecko/20041001 Firefox/0.10.1 ",
                   "Mozilla/5.0 (Windows; U; Windows NT 5.1; ja-JP; rv:1.6) Gecko/20040206 Firefox/0.8 ",
                   "Mozilla/5.0 (Windows; U; Windows NT 5.1; ja-JP; rv:1.7) Gecko/20040614 Firefox/0.9 ",
                   "Mozilla/5.0 (Windows; U; Windows NT 5.1; ja-JP; rv:1.7) Gecko/20040707 Firefox/0.9.2 ",
                   "Mozilla/5.0 (Windows; U; Windows NT 5.1; ja-JP; rv:1.7) Gecko/20040803 Firefox/0.9.3 ",
                   "Mozilla/5.0 (Windows; U; Windows NT 5.1; de-DE; rv:1.7.5) Gecko/20041107 Firefox/1.0 ",
                   "Mozilla/5.0 (Windows; U; Windows NT 5.1; de-DE; rv:1.7.5) Gecko/20041108 Firefox/1.0 ",
                   "Mozilla/5.0 (Windows; U; Windows NT 5.1; de-DE; rv:1.7.5) Gecko/20041122 Firefox/1.0 ",
                   "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.7.5) Gecko/20041110 Firefox/1.0 ",
                   "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.5) Gecko/20041107 Firefox/1.0 ",
                   "Mozilla/5.0 (Windows; U; Windows NT 5.1; es-ES; rv:1.7.5) Gecko/20041210 Firefox/1.0 ",
                   "Mozilla/5.0 (Windows; U; Windows NT 5.1; fr-FR; rv:1.7.5) Gecko/20041108 Firefox/1.0 ",
                   "Mozilla/5.0 (Windows; U; Windows NT 5.1; nl-NL; rv:1.7.5) Gecko/20041202 Firefox/1.0 ",
                   "Mozilla/5.0 (Windows; U; Windows NT 5.1; sv-SE; rv:1.7.5) Gecko/20041108 Firefox/1.0 ",
                   "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8b) Gecko/20050118 Firefox/1.0+ ",
                   "Mozilla/5.0 (Windows NT 5.1; rv:2.1.1) Gecko/20110415 Firefox/4.0.2pre Fennec/4.0.1 ",
                   "Mozilla/5.0 (Windows NT 5.1; rv:2.1) Gecko/20110318 Firefox/4.0b13pre Fennec/4.0 ",
                   "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1 ",
                   "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1 ",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110622 Firefox/6.0a2 ",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1 ",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre ",
        ]
        self.s = requests.Session()
        # proxyHost = "u2637.b5.t.16yun.cn"
        # proxyPort = "6460"
        # proxyUser = "16LGVHDV"
        # proxyPass = "760436"

        # proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        #    "host": proxyHost,
        #    "port": proxyPort,
        #    "user": proxyUser,
        #    "pass": proxyPass,
        # }
        # print("【代理地址是】:",proxyMeta)
        # self.proxy = {
        #     "http": proxyMeta,
        #     "https": proxyMeta,
        # }
        self.headers = {
           "User-Agent": random.choice(self.ua_list),
        }
        
    def send_request(self, url, *args):
        try:
            if args:
                response = self.s.post(url, data=args[0], headers=self.headers, timeout=30, verify=False)
                if response.status_code == 200:
                    return response.text
                elif response.status_code == 404 or response.status_code == 400 or response.status_code == 500:
                    return False
                else:
                    raise Exception("[INFO]:请求异常", response.status_code)
            else:
                response = self.s.get(url, headers=self.headers, timeout=30, verify=False)
                if response.status_code == 200:
                    return response
                elif response.status_code == 404 or response.status_code == 400 or response.status_code == 500:
                    return False
                else:
                    raise Exception("[INFO]:请求异常", response.status_code)

        except Exception as e:
            print("程序出现异常信息,需要处理~!", e)
            FLAG = False
            if FLAG is False:
                for i in range(1, 7):
                    print('%s 请求超时，进行第 %s 次重复请求' % (url, i))
                    if i == 2:
                        print("[INFO]请求缓存中～")
                        time.sleep(3)
                    if i == 3:
                        print("[INFO]再次请求中,请稍等~~")
                        time.sleep(7)
                    if i == 6:
                        print("[INFO]最后一次请求发送中")
                        time.sleep(15)

                    try:
                        print('[INFO]正在请求_', url)
                        if args:
                            response = self.s.post(url, data=args[0], headers=self.headers, timeout=30,verify=False)
                            if response.status_code == 200:
                                return response.text
                            elif response.status_code == 404 or response.status_code == 400:
                                return False
                            else:
                                raise Exception("[INFO]:请求异常", response.status_code)
                        else:
                            response = self.s.get(url, headers=self.headers, timeout=30,verify=False)
                            if response.status_code == 200:
                                return response
                            elif response.status_code == 404 or response.status_code == 400 or response.status_code == 500:
                                return False
                            else:
                                raise Exception("[INFO]: 请求异常！", response.status_code)
                    except:
                        print(f"[DEBUG]第:{i} 次请求失败_{url}")
                        continue