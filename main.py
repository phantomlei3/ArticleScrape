import json
import hashlib
import sys
from multiprocessing import Process
from PostgreSQL.database import database

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# progressbar
from tqdm import tqdm


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

def scrape_articles(db, urls):
    '''

    scraping articles from given URLs. ALl results store in articles Table
    :param urls: a list of article URLs
    '''

    article_profiles = json.load(open("website_profiles/profiles.json"))

    for i in tqdm(range(len(urls))):
        url = urls[i]
        article_id = str(hashlib.md5(url.encode()).hexdigest())
        ### TODO: NULL value issue in the article database
        # check if article exists in the database
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




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    db = database()
    urls = ["https://thinkingmomsrevolution.com/dear-governor-brown-i-am-a-pro-vaccine-parent-who-strongly-opposes-sb-277/"]
    article_id = str(hashlib.md5(urls[0].encode()).hexdigest())
    article_info = db.lookup_article(article_id)
    print(article_info[1])
    # scrape_articles(db, urls)





