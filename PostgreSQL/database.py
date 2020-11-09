
import psycopg2
import psycopg2.extras

class database:
    '''
    Mediator Design Pattern
    database class functions as mediator to control all execution function for all tables
    database class rely on one connection from psycogn2
    '''


    def __init__(self):
        self.conn = psycopg2.connect("host='161.35.62.103' port='5432' dbname='scrape' user='lei' password='nlp'")
        self.cursor = self.conn.cursor()


    def insert_article(self, article_id, article_title, article_content, publisher_name, author_name):
        '''

        insert one new article into articles table

        '''
        insert_command = "INSERT INTO articles(ARTICLE_ID, ARTICLE_TITLE, ARTICLE_CONTENT, PUBLISHER_NAME, AUTHOR_NAME) " \
                         "VALUES (%s, %s, %s, %s, %s)"

        # store information in PostgreSQL articles Table
        self.cursor.execute(insert_command, [article_id, article_title, article_content,
                                             publisher_name, author_name])
        self.conn.commit()

    def lookup_article(self, article_id):
        '''

        :param article_id, a stirng that is the primary key in articles table (md5 value)
        :return:
            if article_id exists in article table:
            return a tuple (article_title, article_content, publisher_name, author_name)
            if not existed:
            return None
        '''
        select_command = "SELECT article_title, article_content, publisher_name, author_name FROM articles " \
                         "WHERE article_id = %s"
        self.cursor.execute(select_command, [article_id])
        result = self.cursor.fetchall()
        if len(result) == 1:
            return result[0]
        else:
            return None


    def insert_author(self, author_id, author_name, author_introduction, author_article_list):
        '''

        insert one new author into authors table

        '''

        insert_command = "INSERT INTO authors(author_id, author_name, author_intro, author_article_list) " \
                         "VALUES (%s, %s, %s, %s) ON CONFLICT (author_id) DO UPDATE SET author_article_list=EXCLUDED.author_article_list"

        self.cursor.execute(insert_command, [author_id, author_name, author_introduction, author_article_list])
        self.conn.commit()

    def lookup_author(self, author_id):
        '''

        :param author_id, a stirng that is the primary key in author table (md5 value)
        :return:
            if author_id exists in authors table:
            return a tuple (author_name, author_intro, author_article_list)
            if not existed:
            return None
        '''
        select_command = "SELECT author_name, author_intro, author_article_list FROM authors WHERE author_id = %s"
        self.cursor.execute(select_command, [author_id])
        result = self.cursor.fetchall()
        if len(result) == 1:
            return result[0]
        else:
            return None


    def insert_publisher(self, publisher_id, publisher_name, publisher_introduction, publisher_credibility_score):
        '''

        insert one new publisher into publisher table

        '''

        insert_command = "INSERT INTO publishers(publisher_id, publisher_name, publisher_intro, publisher_reliability_score) " \
                         "VALUES (%s, %s, %s, %s)"

        self.cursor.execute(insert_command, [publisher_id, publisher_introduction, publisher_credibility_score])
        self.conn.commit()

    def lookup_publisher(self, publisher_id):
        '''

        :param publisher_id, a string that is the primary key in publisher table (md5 value)
        :return:
            if publisher_id exists in publisher table:
            return a tuple (publisher_intro, publisher_reliability_score)
            if not existed:
            return None
        '''
        select_command = "SELECT publisher_intro, publisher_reliability_score FROM publishers WHERE publisher_id = %s"
        self.cursor.execute(select_command, [publisher_id])
        result = self.cursor.fetchall()
        if len(result) == 1:
            return result[0]
        else:
            return None

    def insert_citation(self, article_id, article_paragraphs, citations_links):
        '''

        insert one new publisher into publisher table

        '''
        insert_command = "INSERT INTO citations(article_id, article_paragraphs, citation_links) " \
                         "VALUES (%s, %s, %s)"

        self.cursor.execute(insert_command, [article_id, article_paragraphs, citations_links])
        self.conn.commit()

    def lookup_citation(self, article_id):
        '''

        :param article_id, a string that is the primary key in citations table (md5 value)
        :return:
            if article_id exists in citations table:
            return a tuple (article_paragraphs, citation_links)
            if not existed:
            return None
        '''
        select_command = "SELECT article_paragraphs, citation_links FROM citations WHERE article_id = %s"
        self.cursor.execute(select_command, [article_id])
        result = self.cursor.fetchall()
        if len(result) == 1:
            return result[0]
        else:
            return None

