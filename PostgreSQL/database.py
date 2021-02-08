
import psycopg2
import psycopg2.extras
import hashlib


'''
Reconfiguration function to fill up the missing urls in articles
'''
def fill_up_missing_urls():
    conn = psycopg2.connect("host='161.35.62.103' port='5432' dbname='scrape' user='lei' password='nlp'")
    cursor = conn.cursor()

    select_command = "SELECT article_url FROM articleurls"
    update_command = "UPDATE articles SET article_url = %s WHERE article_id = %s"

    cursor.execute(select_command)
    results = cursor.fetchall()

    for result in results:
        url = result[0]
        article_id = str(hashlib.md5(url.encode()).hexdigest())
        cursor.execute(update_command, [url, article_id])

    conn.commit()


class database:
    '''
    Mediator Design Pattern
    database class functions as mediator to control all execution function for all tables
    database class rely on one connection from psycogn2
    '''


    def __init__(self):
        self.conn = psycopg2.connect("host='161.35.62.103' port='5432' dbname='scrape' user='lei' password='nlp'")
        self.cursor = self.conn.cursor()


    def insert_article(self, article_id, article_title, article_content, publisher_name, author_name, published_time, article_url):
        '''

        insert one new article into articles table

        '''
        insert_command = "INSERT INTO articles(ARTICLE_ID, ARTICLE_TITLE, ARTICLE_CONTENT, PUBLISHER_NAME, AUTHOR_NAME, PUBLISHED_TIME, ARTICLE_URL) " \
                         "VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (ARTICLE_ID) DO NOTHING"

        # store information in PostgreSQL articles Table
        self.cursor.execute(insert_command, [article_id, article_title, article_content,
                                             publisher_name, author_name, published_time, article_url])
        self.conn.commit()

    def lookup_article(self, article_id):
        '''

        :param article_id, a stirng that is the primary key in articles table (md5 value)
        :return:
            if article_id exists in article table:
            return a tuple (article_title, article_content, publisher_name, author_name, published_time, article_url)
            if not existed:
            return None
        '''
        select_command = "SELECT article_title, article_content, publisher_name, author_name, published_time, article_url FROM articles " \
                         "WHERE article_id = %s"
        self.cursor.execute(select_command, [article_id])
        result = self.cursor.fetchall()
        if len(result) == 1:
            return result[0]
        else:
            return None

    def get_all_articles(self):
        '''

        :return: the all articles in the following format (publisher_name, article_url, article_title, article_id, article_content, author_name, published_time)
        '''
        select_command = "SELECT publisher_name, article_url, article_title, article_id, article_content, author_name, published_time FROM articles"
        self.cursor.execute(select_command)
        result = self.cursor.fetchall()
        return result

    def get_all_article_contents(self):
        '''

        :return: the article content of all articles in articles in a list
        '''
        select_command = "SELECT article_content FROM articles"
        self.cursor.execute(select_command)
        result = [i[0] for i in self.cursor.fetchall()]
        return result

    def insert_article_url(self, article_url, website_name, website_url):
        '''

        insert one new article url into articleurls table
            repetitive URLs will be ignored by the system when inserted

        '''
        insert_command = "INSERT INTO articleurls(article_url, website_name, website_url)" \
                         "VALUES (%s, %s, %s) ON CONFLICT (article_url) DO NOTHING;"

        # store information in PostgreSQL articles Table
        self.cursor.execute(insert_command, [article_url, website_name, website_url])
        self.conn.commit()

    def get_all_article_urls(self):
        '''

        :return: all article urls in a list i.e. [www.google.com, www.gmail.com]
        '''
        select_command = "SELECT article_url from articleurls"

        self.cursor.execute(select_command)
        result = self.cursor.fetchall()

        # clean up unnecessary tuples
        result = [item[0] for item in result]

        return result

    def return_article_urls(self, website_url):
        '''

        :param website_url, the website domain URL in website profiles
        :return:
            if website_url exists in articleurls table:
            return a list of tuples (article_url)
            if not existed:
            return None
        '''
        select_command = "SELECT article_url from articleurls Where website_url = %s"

        self.cursor.execute(select_command, [website_url])
        result = self.cursor.fetchall()
        if len(result) >= 1:
            # clean up unnecessary tuples
            result = [item[0] for item in result]

            return result
        else:
            return None

    def insert_paragraph(self, publisher_name, url, article_title, paragraph_id, paragraph_content, author_name, published_time):
        '''

        insert one paragraph into paragraphs table

        '''
        insert_command = "INSERT INTO paragraphs(publisher_name, url, article_title, paragraph_id, paragraph_content, author_name, published_time)" \
                         "VALUES (%s, %s, %s, %s, %s, %s, %s);" # ON CONFLICT (paragraph_id) DO NOTHING
        self.cursor.execute(insert_command, [publisher_name, url, article_title, paragraph_id, paragraph_content, author_name, published_time])
        self.conn.commit()