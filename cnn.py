import requests
from BeautifulSoup import BeautifulSoup
import json
import traceback
import time
from web_crawler import WebCrawler



class Cnn(WebCrawler):
    def __init__(self):
        super(Cnn, self).__init__()
        self.htmls = []
        self.main_url = u"http://cnn.com"
        self.dir_path = "cnn"


    def download_url(self):
        # This function downloads all the data from CNN's CDNs, parses to check data exists (in json format), and adds it to a list
        # Currenly, only zones 1-4 work, so to save time, I'm limiting the GETs to only those. This of course can be changed in the future
        print "Fetching main page from www.cnn.com"
        for i in range(1, 5):
            item = requests.get(r"http://cnn.com/data/ocs/section/index.html:intl_homepage1-zone-" + str(i) + r"/views/zones/common/zone-manager.izl").text
            # Some of the time the output from CNN CDNs is not json, and just outpus 404, if this happens we just continue to next zone
            try:
                item_json = json.loads(item)
                if item_json["izlData"] is not None:
                    self.htmls.append(item_json["html"])
            except Exception, e:
                continue
        self.parse_html()


    def parse_html(self):
        # This function parses the list of html data from download_url() to receive a list of articles urls from
        # their 'href' tags
        print "Collecting all articles from the main page"
        if self.htmls:
            for html in self.htmls:
                parsed = BeautifulSoup(html)
                articles = parsed.findAll('article')
                for item in articles:
                    try:
                        i = item.find('a', href=True)["href"]
                        # Some of the fetched links are already FQDN, so no need to add the website domain
                        if i.startswith("http"):
                            self.articles_list.append(i)
                        else:
                            self.articles_list.append(self.main_url + i)
                    except Exception, e:
                        pass
            # Removing duplicates if there are
            self.articles_list = list(set(self.articles_list))


    def download_and_save_articles(self):
        # Downloads and saves new articles to website path
        if len(self.articles_list) == 0:
            print "No new articles have been found!"
            return
        print "Downloading and saving " + str(len(self.articles_list)) + " new articles from www.cnn.com"
        for article in self.articles_list:
            try:
                self.extract_article_from_html(article)
            except Exception, e:
                tb = traceback.format_exc()
                # I did this since I had issues because of sending too many GET requests in a short period of time
                print "Exception while downloading article. Exception was: " + tb
                print "Probably got 'connection refused' from server. Retrying in 5 seconds"
                time.sleep(5)
                try:
                    self.extract_article_from_html(article)
                except:
                    continue
