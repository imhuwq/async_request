from loop import start_loop
from request import Request

url = 'http://imhuwq.com'

req1 = Request()
req1.get(url)
req2 = Request()
req2.get(url + '/blog/')
start_loop()
