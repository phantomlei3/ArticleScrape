from PostgreSQL.database import database
import numpy as np
import random
import pandas as pd
from glob2 import glob


import paragraphs
import keyword_filter

'''
1. use PostgreSQL database to extract article data
article id, article publisher, article url
2. select 20 articles from each publishers
3. extract data into csv and write down annotation in .csv file
4. import csv files into PostgreSQL database

'''

def select_articles_from_publisher(db, num_articles, publisher_name, csv=True):
    '''

    randomly sample certain number of articles from specific publisher

    :param db, the access class to PostgreSQL database
    :param num_articles: int, the number of articles sampled from this publisher
    :param publisher_name:  string, the name of publisher
    :return: a list of articles in the following tuple form
    (article_id, publisher_name, article_url)
    if csv = true, generate a csv file to contain this information as well, file name is article_annotations.csv

    '''

    # (0 publisher_name, 1 article_url, 2 article_title, 3 article_id, 4 article_content, 5 author_name, 6 published_time)
    all_articles = db.get_all_articles()
    # sampled article: ('article_id', 'publisher_name', 'article_url')
    selected_articles = [(article[3], article[0], article[1]) for article in all_articles if article[0] == publisher_name]

    sampled_articles = random.sample(selected_articles, num_articles)

    if csv:
        column_names = ['article_id', 'publisher_name', 'article_url']
        data = np.array(sampled_articles)
        df = pd.DataFrame(data, columns=column_names)
        df.to_csv('annotations10.csv')

    return sampled_articles


def selected_paragraphs_from_publisher(db, num_articles, publisher_name, csv=True):
    '''

    create a csv files that contains paragraphs from selected articles for annotation.
    randomly selected articles from filtered articles by checking the existence of keywords (read keyword_filter.py)
    Each paragraph in articles

    :param db, the access class to PostgreSQL database
    :param num_articles: int, the number of articles sampled from this publisher
    :param publisher_name:  string, the name of publisher

    '''

    # (0 publisher_name, 1 article_url, 2 article_title, 3 article_id, 4 article_content, 5 author_name, 6 published_time)
    all_articles = keyword_filter.filter_out_by_dictionary_for_all(db)
    selected_articles = [(article[3], article[0], article[1]) for article in all_articles if
                         article[0] == publisher_name]
    # sampled article: ('article_id', 'publisher_name', 'article_url')
    sampled_articles = random.sample(selected_articles, num_articles)

    # find the corresponding paragraphs by the article_id of sampled articles
    # keys in dataframe: (publisher_name, article_url, article_title, paragraph_id, paragraph_content, author_name, published_time)
    paragraphs_df = paragraphs.generate_filtered_paragraphs_csv(db)

    column_names = ['paragraph_id', 'publisher_name', 'article_url', 'paragraph_content']
    selected_paragraphs_df = pd.DataFrame([], columns=column_names)

    for article in sampled_articles:
        article_id = str(article[0])
        article_paragraphs = paragraphs_df[paragraphs_df['paragraph_id'].str.contains(article_id)][column_names]
        selected_paragraphs_df = selected_paragraphs_df.append(article_paragraphs)

    if csv:
        selected_paragraphs_df.to_csv('annotations2.csv')

def load_annotations():
    '''

    :return: a list of tuples in the following form
    (article_id, publisher_name, article_url, title_annotation, content_annotation)
    '''
    annotations = list()
    for filepath in glob("article_annotations/*.xlsx"):
        df = pd.read_excel(filepath, index_col=0)
        records = df.to_records(index=False)
        annotations += list(records)
    return annotations

def stats_title_annotations(annotations):
    stats_dict = dict()
    for annotation in annotations:
        publisher_name = annotation[1]
        title_annotation = annotation[-2]
        if publisher_name not in stats_dict.keys():
            stats_dict[publisher_name] = 0
        stats_dict[publisher_name] += int(title_annotation)
    return stats_dict


def stats_content_annotations(annotations):
    stats_dict = dict()
    for annotation in annotations:
        publisher_name = annotation[1]
        content_annotation = annotation[-1]
        if publisher_name not in stats_dict.keys():
            stats_dict[publisher_name] = 0
        stats_dict[publisher_name] += int(content_annotation)
    return stats_dict




if __name__ == '__main__':
    db = database()

    # Notes:
    # predicate-level blocking
    # not just keyword-based model
    #

    # article_annotations = load_annotations()

    # titles = stats_title_annotations(article_annotations)
    # contents = stats_content_annotations(article_annotations)

    # print_dict(contents)

    # Age of Autism 1
    # select_articles_from_publisher(db, 25, "Age of Autism")

    # Australian Vaccination-risks Network 2
    # select_articles_from_publisher(db, 25, "Australian Vaccination-risks Network")

    # Focus For Health (0/25 is anti-vaccination) 3
    # select_articles_from_publisher(db, 25, "Focus For Health")

    # Green Med Info (2/25 is anti-vaccination) 4
    # select_articles_from_publisher(db, 25, "Green Med Info")

    # Kelly Brogan MD 5
    # select_articles_from_publisher(db, 25, "Kelly Brogan MD")

    # Mom across America 6 (1/25 is anti-vaccination)
    # select_articles_from_publisher(db, 25, "Mom across America")

    # The Thinking Mom's Revolution 7
    # select_articles_from_publisher(db, 25, "The Thinking Mom's Revolution")

    # VacTruth 8
    # select_articles_from_publisher(db, 25, "VacTruth")


    # The Vaccine Reaction 1
    # selected_paragraphs_from_publisher(db, 25, "The Vaccine Reaction")

    # Vaxxter 2
    selected_paragraphs_from_publisher(db, 25, "Vaxxter")
