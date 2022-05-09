import os
from queue import Queue


class ProxyParser:
    maindir_path = os.path.dirname(os.path.split(__file__)[0])

    def read_http_proxies(self):
        result = list()
        path = os.path.join(self.maindir_path, 'proxies', 'http.txt')
        with open(path, 'r', encoding='utf-8') as f:
            strings = f.readlines()
        for proxy in strings:
            proxy = proxy.strip()
            proxy = proxy.replace('\n', '')
            result.append(dict(http='http://' + proxy, https='https://' + proxy))
        return result

    def read_socks5_proxies(self):
        result = list()
        path = os.path.join(self.maindir_path, 'proxies', 'socks5.txt')

        with open(path, 'r', encoding='utf-8') as f:
            strings = f.readlines()
        for proxy in strings:
            proxy = proxy.strip()
            proxy = proxy.replace('\n', '')
            result.append(dict(http='socks5h://' + proxy, https='socks5h://' + proxy))
        return result

    def read_socks4_proxies(self):
        result = list()
        path = os.path.join(self.maindir_path, 'proxies', 'socks4.txt')

        with open(path, 'r', encoding='utf-8') as f:
            strings = f.readlines()
        for proxy in strings:
            proxy = proxy.strip()
            proxy = proxy.replace('\n', '')
            result.append(dict(http='socks4a://' + proxy, https='socks4a://' + proxy))
        return result

    def read_proxies(self):
        result = Queue()
        try:
            http_proxies = self.read_http_proxies()
        except:
            http_proxies = None

        try:
            socks4_proxies = self.read_socks4_proxies()
        except:
            socks4_proxies = None

        try:
            socks5_proxies = self.read_socks5_proxies()
        except:
            socks5_proxies = None

        if http_proxies:
            for i in http_proxies:
                result.put_nowait(i)
        if socks4_proxies:
            for i in socks4_proxies:
                result.put_nowait(i)
        if socks5_proxies:
            for i in socks5_proxies:
                result.put_nowait(i)

        return result


if __name__ == '__main__':
    print(ProxyParser().read_proxies().queue)