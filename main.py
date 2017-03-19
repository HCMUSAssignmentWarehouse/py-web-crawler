import threading
from queue import Queue
from spider import Spider
from domain import *
from file_utils import *

PROJECT_NAME = 'simple_py_web_crawler'
HOMEPAGE = 'http://dantri.com.vn/'
DOMAIN_NAME = ""
NUMBER_OF_THREADS = 1
QUEUE_FILE = ""
CRAWLED_FILE = ""



# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# Each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


# Check if there are items in the queue, if so crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()


print(" ----- Simple Py Web Crawler ----- ")
website = input("Input your website to crawl: ")
if not website == "":
    HOMEPAGE = website
    PROJECT_NAME = get_sub_domain_name(HOMEPAGE)
    DOMAIN_NAME = get_domain_name(HOMEPAGE)
    QUEUE_FILE = PROJECT_NAME + '/queue.txt'
    CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)
create_workers()
crawl()
