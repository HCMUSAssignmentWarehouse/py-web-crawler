from urllib.request import urlopen
from finder import LinkFinder
from domain import *
from file_utils import *


class WebSpider:
    folder_name = ''
    base_url = ''
    domain_name = ''
    frontier_file = ''
    fetched_file = ''
    frontier = set()
    fetched = set()

    def __init__(self, project_name, base_url, domain_name):
        WebSpider.folder_name = project_name
        WebSpider.base_url = base_url
        WebSpider.domain_name = domain_name
        WebSpider.frontier_file = WebSpider.folder_name + '/frontier.txt'
        WebSpider.fetched_file = WebSpider.folder_name + '/downloadList.txt'
        self.init()
        self.fetch_page('First spider', WebSpider.base_url)

    # Creates directory and files for project on first run and starts the spider
    @staticmethod
    def init():
        create_project_directory(WebSpider.folder_name)
        create_data_files(WebSpider.folder_name, WebSpider.base_url)
        WebSpider.frontier = file_to_set(WebSpider.frontier_file)
        WebSpider.fetched = file_to_set(WebSpider.fetched_file)

    # Updates user display, fills frontier and updates files
    @staticmethod
    def fetch_page(thread_name, page_url):
        if page_url not in WebSpider.fetched:
            print(thread_name + ' now crawling ' + page_url)
            print('Frontier ' + str(len(WebSpider.frontier)) + ' page(s) | Fetched ' + str(len(WebSpider.fetched)) + " page(s).")
            links = WebSpider.gather_links(page_url, len(WebSpider.fetched))  # Parse html and Gather links first
            WebSpider.add_links_to_queue(links, False)  # Then add to frontier
            WebSpider.frontier.remove(page_url)
            WebSpider.fetched.add(page_url)
            WebSpider.update_files()

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
                write_file_in_folder(WebSpider.folder_name, str(file_index + 1) + ".html", html_string, True)
            finder = LinkFinder(WebSpider.base_url, page_url)
            finder.feed(html_string)
        except Exception as e:
            print(str(e))
            return set()
        return finder.page_links()  # bring to inside try catch

    # Saves frontier data to project files
    @staticmethod
    def add_links_to_queue(links, is_crawl_other_sites):
        for url in links:
            if (url in WebSpider.frontier) or (url in WebSpider.fetched):
                continue
            if WebSpider.domain_name != get_domain_name(url) and not is_crawl_other_sites:
                continue
            WebSpider.frontier.add(url)

    @staticmethod
    def update_files():
        set_to_file(WebSpider.frontier, WebSpider.frontier_file)
        set_to_file(WebSpider.fetched, WebSpider.fetched_file)
