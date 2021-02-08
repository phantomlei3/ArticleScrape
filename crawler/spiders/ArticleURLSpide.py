import scrapy
import re
from PostgreSQL.database import database



class articleURLSpide(scrapy.Spider):
    '''
        Scrapy web crawler that extracts article URL from a given website category page
    '''
    name = "articleURLs"


    def __init__(self, **kw):
        super(articleURLSpide, self).__init__(**kw)
        self.website_url = kw.get('website_url') # website domain
        self.category_url = kw.get('category_url')  # one URL from user input
        self.database = database()
        self.profile = kw.get('profile') # profile of crawler for this website


    def start_requests(self):
        '''
        Scrapy built-in method to start crawling by calling parse
        '''

        yield scrapy.Request(url=self.category_url, callback=self.parse)

    def parse(self, response):
        '''
        Scrapy built-in method for scraping pages
        Please do not use this parse function. Scrapy will use it automatically
        :param response: a HTML response from URL
        :returns Website name and Article URL
                will be saved in article URL Table (PostgreSQL)
                if the given url does not have website profile, None will be stored in table
        '''
        # a list of article URLs on this category page
        article_URLs = response.css(self.profile["article_urls"]).extract()

        # get website name
        website_name = self.profile["name"]

        # store information in PostgreSQL articles Table
        for i in range(len(article_URLs)):
            if self.website_url not in article_URLs[i]:
                article_URLs[i] = self.complete_article_url(article_URLs[i])
            self.database.insert_article_url(article_URLs[i], website_name, self.website_url)

    def complete_article_url(self, article_url):
        '''
        helper function to return complete article urls for a given URL without website domain
        '''
        return "https://"+self.website_url+article_url




