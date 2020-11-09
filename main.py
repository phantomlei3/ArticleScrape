import json
import hashlib
import sys
from multiprocessing import Process
from PostgreSQL.database import database

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def thread_article_crawl(id, url, profile):
    '''
    A helper thread function for article crawl
    :param profile: a profile of publisher website that this article belongs to
    :param conn_string: a psycopg2 connection setup string
    '''
    process = CrawlerProcess(get_project_settings())
    process.crawl('articles', id=id, url=url, profile=profile)
    process.start()

def output_article_to_txt(db, article_id):
    '''
    output the article information from article database by article id
    '''

    # (article_title, article_content, publisher_name, author_name)
    article = db.lookup_article(article_id)
    with open("test_article.txt", "w", encoding="utf-8") as output:
        output.write("Article Title: " + article[0]+"\n")
        output.write("Publisher: " + article[2]+"\n")
        output.write("Author: " + article[3]+"\n")
        output.write("\n")
        output.write(article[1])



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    article_profiles = json.load(open("website_profiles/profiles.json"))
    url = "https://vaxxter.com/chilling-ingredient-in-covid19-vaccine/"
    article_id = str(hashlib.md5(url.encode()).hexdigest())


    # check if article exists in the database
    db = database()
    article_info = db.lookup_article(article_id)
    if article_info is None:
        # get article website profile
        url_domain = url.split("/")[2].strip()
        if url.split("/")[2].strip() in article_profiles:
            profile = article_profiles[url_domain]
            # crawl article information
            p = Process(target=thread_article_crawl, args=(article_id, url, profile))
            p.start()
            p.join()

    ### TODO: NULL value issue in the article database
    output_article_to_txt(db, article_id)

