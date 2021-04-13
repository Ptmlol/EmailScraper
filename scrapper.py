import requests
import re
import urllib.parse
import urllib.request
import base64
import re
from tlds import tld_set


EMAIL_REGEX = '([%(local)s][%(local)s.]+[%(local)s]@[%(domain)s.]+\\.(?:%(tlds)s))(?:[^%(domain)s]|$)' % {
    'local': 'A-Za-z0-9!#$%&\'*+\\-/=?^_`{|}~',
    'domain': 'A-Za-z0-9\-',
    'tlds': '|'.join(tld_set)
}

HIDDEN_AT_SYM = (" (at) ", " [at] ", " (@) ", " [@] ", " @ ")
HIDDEN_DOT_SYM = (" (dot) ", " [dot] ", " (.) ", " [.] ", " . ")
HIDDEN_REGEX = [
    '(\w+({0})\w+({1})\w+)'.format(
        at.replace("(", r"\(").replace(")", r"\)").replace("[", r"\[").replace("]", r"\]"),
        dot.replace("(", r"\(").replace(")", r"\)").replace("[", r"\[").replace("]", r"\]"),
    )
    for at, dot in zip(HIDDEN_AT_SYM, HIDDEN_DOT_SYM)
]


class Scraper:
    def __init__(self, target_url):
        self.target_url = target_url
        self.session = requests.Session()
        self.target_links = []

    def extract_links_from(self, url):
        response = self.session.get(url)
        return re.findall('(?:href=")(.*?)"', str(response.content))

    def crawl(self, url=None):
        if url is None:
            url = self.target_url
        href_links = self.extract_links_from(str(url))
        for link in href_links:
            link = urllib.parse.urljoin(url, link)

            if "#" in link:
                link = link.split("#")[0]

            if self.target_url in link and link not in self.target_links:
                self.target_links.append(link)
                response = self.session.get(self.target_url)
                self.crawl(link)


    def run(self):
        self.crawl()


target = "http://192.168.108.128/dvwa/"

scrap = Scraper(target)
scrap.run()
