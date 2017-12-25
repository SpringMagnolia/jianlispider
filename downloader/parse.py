# coding=utf-8
from retrying import retry
import requests

headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"}

@retry(stop_max_attempt_number=3)
def _parse_url(url):
    response = requests.get(url,headers=headers,timeout=5)
    assert response.status_code == 200
    return response


def parse_url(url):
    try:
        response = _parse_url(url)
    except Exception as e:
        print(e)
        response = None
    return response

if __name__ == '__main__':
    resposne = parse_url("http://www.baidu.com")
    print(resposne)