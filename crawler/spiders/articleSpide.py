import scrapy
import re
import psycopg2
import psycopg2.extras
from PostgreSQL.database import database


class articleSpide(scrapy.Spider):
    '''
        Scrapy web crawler that extracts article title/content, author, and publisher from one article URL
    '''
    name = "articles"


    def __init__(self, **kw):
        super(articleSpide, self).__init__(**kw)
        self.id = kw.get('id')  # id used for this data in PostgreSQL
        self.url = kw.get('url')  # one URL from user input
        self.database = database()
        self.profile = kw.get('profile') # profile of crawler for this website


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
        :returns Article title, article content, author name, author page and publisher name
                will be saved in article Table (PostgreSQL) with id
                if the given url does not have website profile, None will be stored in table
        '''

        '''
        Extract article title, article content, author name, author page and publisher name from one URL
        '''

        # article title and content
        article_title = response.css(self.profile["article_title"]+"::text").get().strip()  # tested
        raw_article_content = response.css(self.profile["article_content"]).extract()
        clean_paragraphs = self.get_clean_article_contents(raw_article_content)
        article_content = "'\n\n".join(clean_paragraphs) #tested

        # publisher information
        publisher_name = self.profile["name"] # tested

        # author information
        author_name = response.css(self.profile["author_name"]+"::text").get() # tested

        # store information in PostgreSQL articles Table
        self.database.insert_article(self.id, article_title, article_content,
                                             publisher_name, author_name)

        ## TODO: CITIATION MODE: OFF
        # if citations is required to check, store citation information
        # citations = self.get_citations(raw_article_content)
        # self.database.insert_citation(self.id, clean_paragraphs, citations)



    def get_clean_article_contents(self, article_content_html):
        '''
        extract all article content from HTML response

        :param article_content_html: HTML response of article contents
        :return: pure article content without any html tags
        '''
        article_paragraphs = list()

        for paragraph in article_content_html:
            # remove html tags
            clean_paraggraph = re.sub(r'<.*?>', '', paragraph).strip()
            # remove &nbsp
            clean_paraggraph = clean_paraggraph.replace(u'\xa0', u' ')

            if clean_paraggraph != "":
                article_paragraphs.append(clean_paraggraph)


        return article_paragraphs


    def get_citations(self, paragraphs):
        '''
        extract all citations in article content
        :param paragraphs, a list of paragraph string from article content
            eg. ["None", "www.google.com", "None", ...]
            each one corresponds to each paragraph
        :return:
        '''

        # create tags for regex and get the cited words
        citation_tag = re.compile(r'<a.*?href=\"(.*?)\".*?>.*?</a>')

        # create citations list to store all citations link for each paragraph
        citations = list()


        for paragraph in paragraphs:
            potential_citations = re.findall(citation_tag, paragraph)
            # no citations in this paragraph
            if len(potential_citations) == 0:
                citations.append("None")
            else:
                # use the first citation for the whole paragraph for convenience
                # TODO: advance multiple citations in one paragraph
                citations.append(potential_citations[0])

        return citations


