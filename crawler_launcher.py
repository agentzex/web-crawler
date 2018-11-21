from cnn import Cnn
from fox_news import FoxNews
from web_crawler import WebCrawler



if __name__ == '__main__':
    print "** Starting crawler **"

    # You can create specific instance for cnn or fox news to download new articles,
    # or use WebCrawler instance to download or search from both of them, with download_all() & search_all()
    cnn = Cnn()
    # fox_news = FoxNews()
    #
    # crawler = WebCrawler()
    # # Adding the websites instances to WebCrawler class in order to use download_all() & search_all()
    # crawler.add_instances([cnn, fox_news])
    # crawler.download_all()
    #
    # # To search a string, give it below as input. Set'exact_match' to 'True' to match whole word. Set to False to search
    # # the requested string as a substring as well. The return value is a list of paths, where the string was found.
    # found_paths = crawler.search_all("trump")


    # Below is the same flow, but for specific instance

    cnn.download_url()
    cnn.check_before_download()
    cnn.download_and_save_articles()
    found_paths = cnn.search_string_in_article("trump", exact_match=False)

    print "** Crawler has finished running **"
