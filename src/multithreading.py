import Queue
import threading
import urllib2
import time

# called by each thread
def get_url(q, url):
    time.sleep(20)
    q.put(urllib2.urlopen(url).read())

theurls = ["http://google.com", "http://yahoo.com",
"http://google.com", "http://yahoo.com",
"http://google.com", "http://yahoo.com",
]

q = Queue.Queue()

for u in theurls:
    t = threading.Thread(target=get_url, args = (q,u))
    t.daemon = True
    print('starting thread')
    t.start()

s = q.get()
print (s)
