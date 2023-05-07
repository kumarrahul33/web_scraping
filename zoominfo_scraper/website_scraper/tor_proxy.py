import time
from datetime import datetime, timedelta
from stem import Signal
import requests
from stem.control import Controller

class NotIndexedError(Exception):
    pass

class TorProxy:
    def __init__(self):
        self.last_ip_renewal = datetime.now()
        self.startTorSession()
        # print(type(self.session))

    def startTorSession(self):
        self.session = requests.session()
        # print(self.get_ip())
        # Tor uses the 9050 port as the default socks port
        self.session.proxies = {'http':  'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050'}

    # signal TOR for a new connection 
    def renew_connection(self):
        # if datetime.now() - self.last_ip_renewal < timedelta(seconds=3):
            # return
        self.session = None
        
        remain_time = (datetime.now()-self.last_ip_renewal).total_seconds()
        if remain_time < 3:
            time.sleep(3-remain_time)


        with Controller.from_port(port = 9051) as controller:
            controller.authenticate(password="rahul")
            controller.signal(Signal.NEWNYM)
        self.startTorSession()
        self.last_ip_renewal = datetime.now()


    def get(self,url, rotate=False, delay=1e-3):
        time.sleep(delay)
        if rotate:
            self.renew_connection()
        return self.session.get(url)

    # def get_ip(self):
    #     try:
    #         ip_page = self.session.get("http://icanhazip.com") 
    #         latest_proxy = ip_page.content.decode('utf-8').strip()
    #     except:
    #         latest_proxy = "ip-not-available"
    #     return latest_proxy


class Retriever:
    def __init__(self):
        self.proxy = TorProxy()
    
    def renew(self):
        self.proxy.renew_connection()
        # print(type(self.proxy))

    def get_ip(self):
        try:
            ip_page = self.proxy.get("http://icanhazip.com") 
            latest_proxy = ip_page.content.decode('utf-8').strip()
        except:
            latest_proxy = "ip-not-available"
        return latest_proxy

    def get(self, url):
        # try:
        #     print(self.proxy.get_ip())
        #     print("hello")
        # except Exception as e:
        #     print("this is retriever exception")
        #     print(e)
        try:
            page = self.proxy.get(url)
            if page.status_code == 404:
                print("site-not-indexed")
                raise NotIndexedError
                # return "" 
            if page.status_code != 200:
                print("renewing ip")
                print(page.status_code)
                print(self.get_ip())
                try:
                    # self.proxy.renew_connection()
                    self.renew()
                except Exception as e:
                    print("error here")
                    print(e)
                return self.get(url)
        except Exception as e:
            print(e)
        # time.sleep(3)
        return page


# p = TorProxy()
# print(p.get_ip())
    
