from core.ProxyParser import ProxyParser
import requests
from concurrent.futures import ThreadPoolExecutor
from core.ResultsWriter import ResultsWriter

s = requests.Session()

proxies = ProxyParser().read_proxies().queue

def check_proxy(proxy):
     try:
         s.get('http://httpbin.org/anything', proxies=proxy)
     except:
         return False
     return proxy


def prepare_good_proxies(proxy):
    goods = []
    for p in proxy:
        if p:
            goods.append(p['https'].split('//')[1])
    return goods


with ThreadPoolExecutor(max_workers=300) as e:
    results = e.map(check_proxy, proxies)

goods = prepare_good_proxies(results)

results_writer = ResultsWriter()

for g in goods:
    results_writer.write_to_file(g)