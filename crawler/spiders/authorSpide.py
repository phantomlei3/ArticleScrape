import scrapy
import unidecode
import re
import psycopg2
import psycopg2.extras
from PostgreSQL.database import database

class authorSpide(scrapy.Spider):
    '''
        Scrapy web crawler that extracts author introduction and author recent article URL list from author page
    '''
    name = "authors"


    def __init__(self, **kw):
        super(authorSpide, self).__init__(**kw)
        self.id = kw.get('id')  # id used for this data in PostgreSQL
        self.url = kw.get('author_page_link')  # the URL of author page
        self.author_name = kw.get('author_name')
        self.profile = kw.get('profile') # profile of crawler for this website
        self.database = database() # get Database to store data


    def start_requests(self):
        '''
        Scrapy built-in method to start crawling by calling parse
        '''

        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        '''
        Scrapy built-in method for scraping pages
        Please do not use this parse function. Scrapy will use it automatically
        :param response: a HTML response from URL
        :returns author name, author introduction, and a list of recent articles written by author stored in TABLE authors with id
        '''

        '''
        Extract article title, article content, author name, author page and publisher name from one URL
        Update author author_article_list if exist conflict
        '''

        # extract author introduction
        author_introduction = "None"
        if self.profile["author_intro"] != "None":
            author_introduction = response.css(self.profile["author_intro"]+"::text").extract() # tested
            # combine and clear up introduction
            author_introduction = self.get_clean_author_introduction(author_introduction)

        # extract recent article link from this author
        author_article_list = response.css(self.profile["author_article_list"]).extract() # tested

        # if URLs in article list does not have domain name, add domain name
        new_author_article_list = list()
        if author_article_list is not None:
            for article_link in author_article_list:
                if self.profile["domain"] not in article_link:
                    new_author_article_list.append(self.add_domain_to_article_link(article_link))
                else:
                    new_author_article_list.append(article_link)

        # convert python string list to PostgreSQl text array
        # postgreSQL_article_array = self.article_list_to_postgreSQL(author_article_list)

        # store information in PostgreSQL authors Table
        self.database.insert_author(self.id, self.author_name, author_introduction, new_author_article_list)




    def get_clean_author_introduction(self, author_introduction):
        '''
        author_introduction might contain multiple paragraphs

        :param author_introduction: HTML response of author introduction
        :return: pure author introduction content without any html tags
        '''
        clean_author_introduction = ""
        for paragraph in author_introduction:
            clean_paraggraph = re.sub(r'<.*?>', '', paragraph).strip()
            # separate paragraphs by spaces because introduction is supposed to be short
            if clean_paraggraph != "":
                clean_author_introduction += clean_paraggraph + " "
        return clean_author_introduction.strip()

    def add_domain_to_article_link(self, URL):
        '''
        Add domain to one article URLsbecause they do not have complete URLs

        :param article_link: one article URL that require to add domain
        :return: one article URL that have domain
        '''
        test_domain = self.profile['domain'].replace("www.", "")
        return "https://"+self.profile['domain']+"/"+URL.strip("/")

    def article_list_to_postgreSQL(self, article_lists):
        '''

        :param article_lists: a list of article URLs
        :return: a string that represents TEXT ARRAY in postgreSQL
        '''
        return '{' + ','.join(article_lists) + '}'

