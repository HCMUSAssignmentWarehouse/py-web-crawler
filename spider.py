from urllib.request import urlopen
from link_finder import LinkFinder
from domain import *
from file_utils import *


class Spider:
    folder_name = ''
    base_url = ''
    domain_name = ''
    frontier_file = ''
    fetched_file = ''
    frontier = set()
    fetched = set()

    def __init__(self, project_name, base_url, domain_name):
        Spider.folder_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.frontier_file = Spider.folder_name + '/frontier.txt'
        Spider.fetched_file = Spider.folder_name + '/downloadList.txt'
        self.init()
        self.fetch_page('First spider', Spider.base_url)

    # Creates directory and files for project on first run and starts the spider
    @staticmethod
    def init():
        create_project_directory(Spider.folder_name)
        create_data_files(Spider.folder_name, Spider.base_url)
        Spider.frontier = file_to_set(Spider.frontier_file)
        Spider.fetched = file_to_set(Spider.fetched_file)

    # Updates user display, fills frontier and updates files
    @staticmethod
    def fetch_page(thread_name, page_url):
        if page_url not in Spider.fetched:
            print(thread_name + ' now crawling ' + page_url)
            print('Frontier ' + str(len(Spider.frontier)) + ' page(s) | Fetched ' + str(len(Spider.fetched)) + " page(s).")
            links = Spider.gather_links(page_url, len(Spider.fetched))  # Parse html and Gather links first
            Spider.add_links_to_queue(links, False)  # Then add to frontier
            Spider.frontier.remove(page_url)
            Spider.fetched.add(page_url)
            Spider.update_files()

    # Converts raw response data into readable information and checks for proper html formatting
    @staticmethod
    def gather_links(page_url, file_index):
        html_string = ''
        try:
            response = urlopen(page_url)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
                # Write to file
                write_file_in_folder(Spider.folder_name, str(file_index + 1) + ".html", html_string, True)
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)
        except Exception as e:
            print(str(e))
            return set()
        return finder.page_links()  # bring to inside try catch

    # Saves frontier data to project files
    @staticmethod
    def add_links_to_queue(links, is_crawl_other_sites):
        for url in links:
            if (url in Spider.frontier) or (url in Spider.fetched):
                continue
            if Spider.domain_name != get_domain_name(url) and not is_crawl_other_sites:
                continue
            Spider.frontier.add(url)

    @staticmethod
    def update_files():
        set_to_file(Spider.frontier, Spider.frontier_file)
        set_to_file(Spider.fetched, Spider.fetched_file)
