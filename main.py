import threading
from queue import Queue
from spider import Spider
from domain import *
from file_utils import *

FOLDER_NAME = 'simple_py_web_crawler'
WEBSITE = 'http://dantri.com.vn/'
DOMAIN_NAME = get_domain_name(WEBSITE)
NUMBER_OF_THREADS = 1


# Create worker threads (will die when main exits)
def create_worker_threads():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=do_in_background)
        t.daemon = True
        t.start()


# Do the next job in the frontier
def do_in_background():
    while True:
        url = frontier.get()
        Spider.fetch_page(threading.current_thread().name, url)
        frontier.task_done()


# Each queued link is a new job
def create_jobs():
    for link in file_to_set(FRONTIER_FILE_NAME):
        frontier.put(link)
    frontier.join()
    start_crawl()


# Check if there are items in the frontier, if so start_crawl them
def start_crawl():
    frontier_links = file_to_set(FRONTIER_FILE_NAME)
    if len(frontier_links) > 0:
        print("We have " + str(len(frontier_links)) + ' links in the frontier')
        create_jobs()


print(" ----- Simple Py Web Crawler ----- ")
website = input("Input your website to start_crawl: ")
if not website == "":
    WEBSITE = website
    FOLDER_NAME = get_sub_domain_name(WEBSITE)
    DOMAIN_NAME = get_domain_name(WEBSITE)
FRONTIER_FILE_NAME = FOLDER_NAME + '/frontier.txt'
FETCHED_FILE_NAME = FOLDER_NAME + '/fetched.txt'
frontier = Queue()
Spider(FOLDER_NAME, WEBSITE, DOMAIN_NAME)
create_worker_threads()
start_crawl()
