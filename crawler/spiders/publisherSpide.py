import scrapy
import re
from PostgreSQL.database import database

class publisherSpide(scrapy.Spider):
    '''
        Scrapy web crawler that extracts publisher introduction and credibility score
    '''
    name = "publisher"


    def __init__(self, **kw):
        super(publisherSpide, self).__init__(**kw)
        self.id = kw.get('id')  # id used for this data in PostgreSQL
        self.profile = kw.get('profile') # profile of crawler for this website
        self.database = database() # get Database to store data


    def start_requests(self):
        '''
        Scrapy built-in method to start crawling by calling parse
        '''

        yield scrapy.Request(url=self.profile["NewsGuard"], callback=self.parse)

    def parse(self, response):
        '''
        Scrapy built-in method for scraping pages
        Please do not use this parse function. Scrapy will use it automatically
        :param response: a HTML response from URL
        '''

        # get publisher information from Profile
        publisher_name = self.profile["name"]

        # extract publisher information from NewsGuard Page
        # TODO: Ameliorate this system
        publisher_introduction = response.css(self.profile["undefined_intro"])
        publisher_score = response.css(self.profile["undefined_score"])

        # store information in PostgreSQL authors Table
        self.database.insert_publisher(self.id, publisher_name, publisher_introduction, publisher_score)



