'''
This design is created to filter out all vaccination-related articles among all article we scraped


Meeting mintues:

Freeziness: Point wise mutual information Probability of
General Corpus
Background Corpus:

random sampling on 44% of articles are not related: do a manual labeling

Date when the article is published:
- need multiple source of proving the article's published date

'''
import math
import random
import hashlib
from PostgreSQL.database import database
import pandas as pd
from main import scrape_articles

# TF-IDF from sklearn
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# DF model from gensim
from gensim.corpora import Dictionary
from gensim.test.utils import datapath, get_tmpfile
from gensim.corpora import WikiCorpus, MmCorpus

# progress bar
from tqdm import tqdm

def get_wiki_dictionary():
    '''
    return a dictionary that contains {"tokens": document frequency} in wikipedia corpus
    '''

    # Unpack Wiki dump
    # wiki = WikiCorpus('wikicorpus/enwiki-20201120-pages-articles-multistream1.xml-p1p41242.bz2', lemmatize=False)
    # MmCorpus.serialize("wikicorpus/wiki-corpus.mm", wiki)

    # create documents to save wiki articles
    # documents = list()
    # for i, text in enumerate(wiki.get_texts()):
    #     documents.append(text)

    # Dictionary of document frequencies
    dct = Dictionary.load_from_text("wikicorpus/wiki_dictionary")

    # the document size of wiki corpus is 21126
    wiki_document_size = 21126

    # return dictionary
    df_dictionary = dict()

    # for each word, the p(word) = document frequency / N, where N is the size of documents in this corpus
    id2token = {v: k for k, v in dct.token2id.items()}
    for token_id, document_frequency in dct.dfs.items():
        # Katz smoothing to handle zero occurrences in wiki-corpus
        df_dictionary[id2token[token_id]] = (document_frequency+1) / wiki_document_size

    return df_dictionary


def get_anti_vax_dictionary(corpus):
    '''
    return a dictionary that contains {"tokens": document frequency} in anti_vax corpus
    '''

    # get the size of documents in corpus
    document_size = len(corpus)

    # remove stopwords
    stop_words = set(stopwords.words('english'))
    # tokenize
    tokenizer = RegexpTokenizer(r'[a-zA-Z]{2,}')
    tokenized_articles = list()
    for article in corpus:
        tokenized_articles.append([word for word in tokenizer.tokenize(article.lower()) if word.lower() not in stop_words])

    # return dictionary
    df_dictionary = dict()

    # Dictionary of document frequencies
    dct = Dictionary(tokenized_articles)
    dct.save_as_text("antivax_corpus/200tests")

    # for each word, the p(word) = document frequency / N, where N is the size of documents in this corpus
    id2token = {v: k for k, v in dct.token2id.items()}
    for token_id, document_frequency in dct.dfs.items():
        df_dictionary[id2token[token_id]] = document_frequency / document_size

    return df_dictionary

def generate_df_dictionary(wiki, anti_vax):
    '''

    :param wiki: wiki df dictionary
    :param anti_vax: anti-vax df dictionary
    :return: a new dictionary that contains {"word": df score}
                for each word, df score = df score in anti_vax / (df score in wiki + 1)
    '''

    # the document size of wiki corpus is 21126
    wiki_document_size = 21126

    df_score_dict = dict()
    for word, anti_vax_df in anti_vax.items():
        # Katz smoothing to handle zero occurrences in wiki-corpus
        wiki_df = 1/21126
        if word in wiki.keys():
            wiki_df = wiki[word]
        df_score = anti_vax_df * math.log(anti_vax_df / wiki_df)
        df_score_dict[word] = df_score
    return df_score_dict

def get_article_contents(db, sampling_url):
    '''

    get a list of article contents as corpus
    :return: corpus, a list of article contents
    '''
    corpus = list()
    for i in tqdm(range(len(sampling_url))):
        url = sampling_url[i]
        article_id = str(hashlib.md5(url. encode()).hexdigest())
        result = db.lookup_article(article_id)
        if result is None:
            continue
        article_content = result[1]
        corpus.append(article_content)

    return corpus

def get_all_article_contents(db):
    '''

    get a list of article contents as corpus
    :return: corpus, a list of article contents
    '''
    corpus = db.get_all_article_contents()

    return corpus

def filter_out_by_dictionary_for_all(db):
    '''


    :return: a list of all related article in table Article
                by checking if specific words in vaccine_related_dictionary is in the article title/content
    '''
    related_article = list()
    all_article = db.get_all_articles()
    for article in all_article:
        # (publisher_name, article_url, article_title, article_id, article_content, author_name, published_time)
        article_content = article[4]
        # filtering by dictionary
        relevance = False
        for word in vaccine_related_dictionary:
            if word in article_content:
                relevance = True
                break
        if relevance:
            related_article.append(article)

    return related_article

def filter_out_by_dictionary_from_sampling(db, sampling_url):
    '''

    :return: a list of related article from given sampling_url
                by checking if specific words in vaccine_related_dictionary is in the article title/content
    '''
    related_article = list()
    count = 0
    for url in sampling_url:
        article_id = str(hashlib.md5(url.encode()).hexdigest())
        result = db.lookup_article(article_id) # (article_title, article_content, publisher_name, author_name, published_time)
        if result is None:
            continue
        count += 1
        article_title = result[0]
        article_content = result[1]
        publisher_name = result[2]
        published_time = result[4]

        # filtering by dictionary
        relevance = False
        for word in vaccine_related_dictionary:
            if word in article_title or word in article_content:
                relevance = True
                break
        if relevance:
            related_article.append([url, article_title, article_content, publisher_name, published_time])

    return related_article


'''
All vaccine_related words that are possible in a article from KL
'''
vaccine_related_dictionary = ["vaccine", "autism", "vaccines", "vaccination",
                              "vaccinated", "health", "vaccinations", "vaccinate",
                              "immune", "unvaccinated", "immunization", "autistic",
                              "pharmaceutical", "pharma", "mmr", "pharma", "flu",
                              "medical", "amp", "disease"]

def sampling_article_urls(db, sampling_num):
    '''

    :return: a list of all article urls contain in articleurls throught random sampling
    '''
    all_urls = db.get_all_article_urls()
    sampling_urls = random.sample(all_urls, sampling_num)
    return sampling_urls

def get_urls_from_specific_website(db, website_url):
    '''

    :return: a list of all article urls for one specific website
    '''
    urls = db.return_article_urls(website_url)

    return urls

def generate_csv(related_articles):
    '''
    :param related_article, a list of articles as the following
    [[url, article_title, article_content, publisher_name, published_time]..]

    :return: a file of csv contain all articles in the following format
    [url, article_title, article_content, publisher_name, published_time]
    '''
    # convert related article to panda dataframe format
    ''' example:
    ({'name': ['Raphael', 'Donatello'],
                   'mask': ['red', 'purple'],
                   'weapon': ['sai', 'bo staff']})
    '''

    article_dataframe = dict()
    article_dataframe['url'] = list()
    article_dataframe['article_title'] = list()
    article_dataframe['article_content'] = list()
    article_dataframe['publisher_name'] = list()
    article_dataframe['published_time'] = list()

    for article in related_articles:
        article_dataframe['url'].append(article[0])
        article_dataframe['article_title'].append(article[1])
        article_dataframe['article_content'].append(article[2])
        article_dataframe['publisher_name'].append(article[3])
        article_dataframe['published_time'].append(article[4])

    df = pd.DataFrame(article_dataframe)
    df.to_csv('anti-vax_articles.csv', index=False)


if __name__ == '__main__':

    db = database()

    # get vaxxter.com
    # urls = get_urls_from_specific_website(db, "vaxxter.com")

    # get www.greenmedinfo.com
    # urls = get_urls_from_specific_website(db, "www.greenmedinfo.com")articles

    # get www.ageofautism.com
    # urls = get_urls_from_specific_website(db, "www.ageofautism.com")

    # get modernalternativemama.com
    # urls = get_urls_from_specific_website(db, "modernalternativemama.com")

    # get thinkingmomsrevolution.com
    # urls = get_urls_from_specific_website(db, "thinkingmomsrevolution.com")

    # get avn.org.au
    # urls = get_urls_from_specific_website(db, "avn.org.au")

    # get thevaccinereaction.org
    # urls = get_urls_from_specific_website(db, "thevaccinereaction.org")

    # get kellybroganmd.com
    # urls = get_urls_from_specific_website(db, "kellybroganmd.com")

    # GET www.livingwhole.org"
    # urls = get_urls_from_specific_website(db, "www.livingwhole.org")

    # Get www.momsacrossamerica.com
    # urls = get_urls_from_specific_website(db, "www.momsacrossamerica.com")

    # Get vactruth.com
    # urls = get_urls_from_specific_website(db, "vactruth.com")

    # Get www.focusforhealth.org
    # urls = get_urls_from_specific_website(db, "www.focusforhealth.org")

    # Get info.cmsri.org
    # urls = get_urls_from_specific_website(db, "info.cmsri.org")

    #

    # scraping articles
    scrape_articles(db, urls)




    # filter out the vaccine-related articles based on the dictionary
    # related_articles = filter_out_by_dictionary(db, sampling_urls)
    # related_articles = filter_out_by_dictionary_for_all(db)
    # print(len(related_articles))


    # # wiki document frequency dictionary
    # wiki_df_dictionary = get_wiki_dictionary()
    #
    # # get the article contents of all articles
    # corpus = get_all_article_contents(db)
    # anti_vax_dictionary = get_anti_vax_dictionary(corpus)
    #
    # # df score dictionary
    # df_score_dictionary = generate_df_dictionary(wiki_df_dictionary, anti_vax_dictionary)
    #
    # # print top 50 words with the highest scores
    # sort_orders = sorted(df_score_dictionary.items(), key=lambda x: x[1], reverse=True)
    # for i in sort_orders[:50]:
    #     print(i[0], i[1])
