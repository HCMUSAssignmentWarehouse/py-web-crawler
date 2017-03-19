from urllib.parse import urlparse
from urllib.parse import urlsplit
#https://docs.python.org/3/library/urllib.parse.html

# Get domain name (example.com)
def get_domain_name(url):
    try:
        results = get_sub_domain_name(url).split('.')
        return results[-2] + '.' + results[-1] #negative indices
        #parsed_uri = urlparse('http://dantri.com.vn/the-gioi.htm')
        #domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        #return domain
    except:
        return ''


# Get sub domain name (name.example.com)
def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc
    except:
        return ''