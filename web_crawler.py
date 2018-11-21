import requests
from requests.utils import quote, unquote
from BeautifulSoup import BeautifulSoup
import os
import re
from HTMLParser import HTMLParser



class WebCrawler(object):
    def __init__(self):
        self.instances = []
        self.articles_list = []
        self.html_parser = HTMLParser()
        self.create_dirs()

    def download_url(self):
        raise NotImplementedError("Subclass must implement download_url()")

    def download_and_save_articles(self):
        raise NotImplementedError("Subclass must implement download_and_save_articles()")


    def download_all(self):
        for i in self.instances:
            i.download_url()
            i.check_before_download()
            i.download_and_save_articles()


    def search_all(self, string_to_search, exact_match=True):
        found_paths = []
        for i in self.instances:
            found = i.search_string_in_article(string_to_search, exact_match)
            found_paths = found_paths + found
        return found_paths


    def create_dirs(self):
        if not os.path.exists("cnn"):
            os.makedirs("cnn")
        if not os.path.exists("fox_news"):
            os.makedirs("fox_news")


    def add_instances(self, instaces):
        # Appends a list of given instances of requested websites to download articles from. Used for download_all() & search_all()
        for i in instaces:
            self.instances.append(i)


    def check_before_download(self):
        # This function checks the latest articles from the websites against the local repository
        # If an article already exists locally, then we won't download it again
        print "Crossing current articles URLs with the already saved articles on the file system"
        final_urls = []
        existing_urls = self.get_current_articles()
        if existing_urls:
            for article in self.articles_list:
                if article not in existing_urls:
                    final_urls.append(article)
            self.articles_list = final_urls


    def get_current_articles(self):
        # This function returns the current list of existing articles URLs, saved on the file system
        existing_urls = []
        for url in os.listdir(self.dir_path):
            existing_urls.append(unquote(url))
        return existing_urls


    def search_line(self, line, string_to_search, exact_match):
        if exact_match:
            if re.search(r'\b' + string_to_search + r'\b', line, re.IGNORECASE):
                return True
        else:
            if re.search(string_to_search, line, re.IGNORECASE):
                return True
        return False


    def search_string(self, string_to_search, exact_match):
        # searching, in a case insensitive manner, the requested string, in each line. If  the string was found,
        # the path to the article is returned.
        # If 'exact_match' is True, the string is searched as a whole word.
        # Otherwise, the string will be searched in substrings as well

        articles = [article for article in os.listdir(self.dir_path)]
        found_articles = []
        for article in articles:
            with open(self.dir_path + os.sep + article, "r") as file:
                for line in file:
                    if self.search_line(line, string_to_search, exact_match):
                        found_articles.append(article)
                        break

        return found_articles


    def print_found_articles(self, found_articles):
        if found_articles:
            for article in found_articles:
                print "The requested string was found at path: " + os.getcwd() + os.sep + self.dir_path + os.sep + article
                print "URL for this article is: " + unquote(article) + "\n*"
        else:
            print "The requested string wasn't found in any of the existing articles"


    def search_string_in_article(self, string_to_search, exact_match=True):
        found_articles = self.search_string(string_to_search, exact_match)
        self.print_found_articles(found_articles)
        return found_articles


    def extract_article_from_html(self, article):
        # GETs an article and extract its tags
        r = requests.get(article).text
        file_name = quote(article, safe="")
        bs = BeautifulSoup(r)
        bs = bs.find("body")
        # Getting all possible actual text from the article, including all the html tags below:
        bs = bs.findAll(["h1", "h2", "h3", "h4", "h5", "h6", "p", "div"])
        with open(self.dir_path + os.sep + file_name, "w") as file:
            for line in bs:
                # this code handles all end cases of special characters coming from html, before saving them to disk.
                # Solving things like quote marks appearing as ' &#x ' on text
                line = self.html_parser.unescape(line.getText())
                file.write(line.encode('utf-8') + "\n")
