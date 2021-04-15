import requests
import re
import urllib.parse
import urllib.request
import base64
import re
from tlds import tld_set
from email_scraper import scrape_emails


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
                response = self.session.get(self.target_url).content
                print(scrape_emails(response))
                self.crawl(link)

    def run(self):
        http = self.session.post("http://192.168.0.171/dvwa/login.php", data={'username': "admin", 'password': "password", 'Login': 'submit'})
        if http.url == 'http://192.168.0.171/dvwa/index.php':
            self.crawl()
        else:
            print("Nu merge")


target = "http://192.168.0.171/dvwa"

scrap = Scraper(target)
scrap.run()
