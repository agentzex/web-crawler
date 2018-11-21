import requests
from BeautifulSoup import BeautifulSoup
import traceback
from web_crawler import WebCrawler



class FoxNews(WebCrawler):
    def __init__(self):
        super(FoxNews, self).__init__()
        self.main_url = u"http://www.foxnews.com"
        self.dir_path = "fox_news"


    def download_url(self):
        # This function downloads all the data from FOX website, parses to check if there is data, and adds it to a list
        # Currenly, only zones 1-4 work, so to save time, I'm limiting the GETs to only those. This of course can be changed in the future
        print "Fetching main page from www.foxnews.com"
        r = requests.get(self.main_url).text
        bs = BeautifulSoup(r)
        bs = bs.find("body")
        articles = bs.findAll('article')
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
        print "Downloading and saving " + str(len(self.articles_list)) + " new articles from www.foxnews.com"
        for article in self.articles_list:
            try:
                self.extract_article_from_html(article)
            except Exception, e:
                tb = traceback.format_exc()
                # I did this since I had issues because of sending too many GET requests in a short period of time
                print "Exception while downloading article. Exception was: " + tb
