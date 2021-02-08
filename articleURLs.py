import json
import hashlib
import sys
from multiprocessing import Process
from PostgreSQL.database import database

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def thread_articleURLs_crawl(website_url, category_url, profile):
    '''
    A helper thread function for articleURLs crawl
    '''
    process = CrawlerProcess(get_project_settings())
    process.crawl('articleURLs', website_url=website_url, category_url=category_url, profile=profile)
    process.start()

def crawl_one_category_page(category_url):
    '''

    Helper function for crawl_all_category_page
    Extract all article URLs on one category page given category ur and save them in articleurls Table
    :param category_url: one category url on a website such as "https://vaxxter.com/page/3/"
    '''
    article_profiles = json.load(open("website_profiles/profiles.json"))
    # get article website profile
    website_domain = category_url.split("/")[2].strip()
    if website_domain in article_profiles:
        profile = article_profiles[website_domain]
        # crawl article information
        p = Process(target=thread_articleURLs_crawl, args=(website_domain, category_url, profile))
        p.start()
        p.join()
    else:
        return

def crawl_all_category_pages(base_category_url, start_page, end_page):
    '''

     Extract all article URLs on multiple category page from start_page to end_page

    :param base_category_url: a base url for the category_url such as "https://vaxxter.com/page/"
    :param start_page: the number of start page on this base category url
    :param end_page: the number of end page on this base category url
    '''
    for i in range(start_page, end_page+1):
        category_url = base_category_url+str(i)
        crawl_one_category_page(category_url)

if __name__ == '__main__':

    '''
        Comment off: Finished
        
        Website List:
        - Vaxxter
        - Modernalternativemama
        - Green Med Info
        - Vactruth
        - The Thinking Mom's Revolution
    '''

    # vaxxter
    # vaxxter_base = "https://vaxxter.com/page/"
    # crawl_all_category_pages(vaxxter_base, 1, 99)

    # modernalternativemama
    # modern_native_mama_base = "https://modernalternativemama.com/page/"
    # crawl_all_category_pages(modern_native_mama_base, 1, 180)

    # Green Med Info
    # green_med_info_base = "https://www.greenmedinfo.com/gmi-blogs?page="
    # crawl_all_category_pages(green_med_info_base, 0, 52)

    # Vactruth
    # Vactruth_base = "https://vactruth.com/news/page/"
    # crawl_all_category_pages(Vactruth_base, 1, 75)

    # The Thinking Mom's Revolution
    # Thinking_Mom_base = "https://thinkingmomsrevolution.com/read-the-blog-here/page/"
    # crawl_all_category_pages(Thinking_Mom_base, 1, 118)


    # Age of Autism
    # Age_of_Autism_base = "https://www.ageofautism.com/page/"
    # crawl_all_category_pages(Age_of_Autism_base, 1, 215)


    # Australian Vaccination-risks Network
    # AVN_base = "https://avn.org.au/blog/page/"
    # crawl_all_category_pages(AVN_base, 1, 30)

    # The Vaccine Reaction
    # The_vaccine_reaction_base = "https://thevaccinereaction.org/vaccination/page/"
    # crawl_all_category_pages(The_vaccine_reaction_base, 1, 32)

    # Kelly Brogan MD
    # Kelly_Brogan_MD_base = "https://kellybroganmd.com/health-topics/page/"
    # crawl_all_category_pages(Kelly_Brogan_MD_base, 1, 100)

    # Living Whole
    # Living_whole_base = "https://www.livingwhole.org/blog/page/"
    # crawl_all_category_pages(Living_whole_base, 1, 15)

    # Mom Across America
    # mom_across_america_base = "https://www.momsacrossamerica.com/blog?page="
    # crawl_all_category_pages(mom_across_america_base, 1, 38)

    # Focus For Health
    # focus_for_health_base = "https://www.focusforhealth.org/blog/page/"
    # crawl_all_category_pages(focus_for_health_base, 1, 19)

    # CMSRI
    # CMRSI_base = "http://info.cmsri.org/the-driven-researcher-blog/page/"
    # crawl_all_category_pages(CMRSI_base, 1, 5)

    # Fearless Parent
    # By Archive.org: https://web.archive.org/web/20201113192302/https://fearlessparent.org/
    fearless_parent_base = "https://web.archive.org/web/20201114134126/https://fearlessparent.org/page/"
    crawl_all_category_pages(fearless_parent_base, 2, 4)

    # The Healthy Home Economist
