import datetime
import urllib

tod = datetime.datetime.now()
d = datetime.timedelta(days = 1)
a = tod - d
# print(int(d))
print(a)


print(tod.strftime('%Y-%m-%dT%H:%M:%SZ'))



import time

timestamp = int(time.time()*1000)
url = "http://www.myurl.com/question?timestamp=%d" % timestamp
print(url)

import urllib.parse
print(urllib.parse.quote_plus(tod.strftime('%Y-%m-%dT%H:%M:%SZ')))
