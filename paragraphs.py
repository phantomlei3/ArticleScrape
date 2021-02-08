
'''

 (1) Take a look at the longest paragraphs, see if you can find any patterns.
 Motivate how we could split these into multiple paragraphs.
 It might be easy to split a 1500-word paragraph into 15 sentences,
 but let's see if we can retain the fact that they are paragraphs somehow.
 Maybe evenly distribute the character count by strategically choosing which sentences to append?

 (2) I'll send you a separate message regarding the backend to the annotation platform.

Goal: FInd a pattern to split the longest paragraph
1. Look into the longest paragraph
2. Create a spread sheet to find the pattern


'''
from PostgreSQL.database import database
from related_articles import filter_out_by_dictionary_for_all
import pandas as pd
import hashlib
from tqdm import tqdm
import collections
import matplotlib.pyplot as plt
import random
import math

# tokenization
from nltk.tokenize import sent_tokenize
from nltk.tokenize import RegexpTokenizer



def shorter_md5_hexdigest(md5_hexdigest):
    '''

    :param md5_hexdigest: a md5 hexdigest string: 32 chars
    :return: a 12 chars hexdigest string
    '''
    short_md5 = ""
    for i in range(0, 24, 2):
        short_md5 += md5_hexdigest[i]
    return short_md5

def split_articles_into_clean_paragraphs(article_contents):
    '''

    helper function that split article_content into a list of paragraphs

    :param article_contents: a string
    :return: a list of paragraphs split from article content
    '''

    paragraphs = list()
    raw_paragraphs = article_contents.split("\n")
    for raw_paragraph in raw_paragraphs:
        # clean redundant space and \n
        clean_paragraph = raw_paragraph.strip("\n").strip()
        # ignore all paragraphs after "acknowledgement" or "reference" as subtitles
        if len(clean_paragraph) <= 20 and ("acknowledgement" in clean_paragraph.lower() or "reference" in clean_paragraph.lower()):
            break
        if len(clean_paragraph) >= 1:
            paragraphs.append(clean_paragraph)

    return paragraphs

def add_new_paragraphs(article, article_id, paragraph_index, article_paragraph, paragraphs_dataframe):
    '''

    helper function for generate_filtered_paragraphs

    '''
    paragraphs_dataframe['publisher_name'].append(article[0])
    paragraphs_dataframe['url'].append(article[1])
    paragraphs_dataframe['article_title'].append(article[2])
    paragraphs_dataframe['paragraph_id'].append(article_id + str(paragraph_index).zfill(3))
    ## TODO: fix the ' issues at the end of every paragraph, quick fix: remove it here
    fixed_article_paragraph = article_paragraph.replace("'", "")
    paragraphs_dataframe['paragraph_content'].append(fixed_article_paragraph)
    paragraphs_dataframe['author_name'].append(article[5])
    paragraphs_dataframe['published_time'].append(article[6])

def split_paragraph(one_parargaph, max_words_len):
    '''

    split one paragraph into multiple paragraphs if # sentences >= 3 and # words >= max_words_len
    # paragraphs split is based on the floor(# words / max_words_len)

    :param one_parargaph: string
    :param max_words_len: the maximum number of words (references for splitting)
    :return: a list of paragraph content
    '''

    tokenizer = RegexpTokenizer(r'[a-zA-Z]{2,}')
    paragraph_in_sentences = sent_tokenize(one_parargaph)
    word_count = len([word for word in tokenizer.tokenize(one_parargaph.lower())])

    # return the original paragraphs in one list
    if word_count <= max_words_len or len(paragraph_in_sentences) <= 3:
        return [one_parargaph]

    # find suitable number of paragraph split
    split_num = min(len(paragraph_in_sentences), math.ceil((word_count+0.0)/max_words_len))
    suitable_max_word_len = math.floor((word_count+0.0) / split_num)
    paragraph_split = list()

    cumulative_words_len = 0
    current_paragraph = ""
    for i in range(len(paragraph_in_sentences)):
        sentence = paragraph_in_sentences[i]
        # count the number of words in each sentence from this paragraphs
        sentence_word_len = len([word for word in tokenizer.tokenize(sentence.lower())])
        current_paragraph += sentence + " "
        cumulative_words_len += sentence_word_len
        # check if reach the split condition or it is the last sentence
        if cumulative_words_len >= suitable_max_word_len or i == len(paragraph_in_sentences) - 1:
            paragraph_split.append(current_paragraph.strip())
            cumulative_words_len = 0
            current_paragraph = ""

    return paragraph_split

def combine_paragraph(article_paragraphs, min_words_len):
    '''

    if a paragraph is < (min_words_len) words, add it to the next paragraph
    if the next paragraph is <(min_words_len) words on it's own (without the previous paragraph added), add the total to the next paragraph

    :param article_paragraphs: a list of paragraphs from article content
    :param min_words_len: the minimum len for checking if paragraph needs combination
    :return a list of combined paragraphs
    '''
    tokenizer = RegexpTokenizer(r'[a-zA-Z]{2,}')
    combined_paragraphs_list = list()
    combined_paragraph = ""
    for i in range(len(article_paragraphs)):
        paragraph = article_paragraphs[i]
        word_count = len([word for word in tokenizer.tokenize(paragraph.lower())])
        if word_count < min_words_len and i != len(article_paragraphs) - 1:
            # add "." at the end of this paragraph so it can be treated as one sentence
            combined_paragraph += paragraph.strip(".")+"."+"\n"
        # the current paragraph does not need any combination
        else:
            # Append in the previous combined paragraphs if not empty
            if combined_paragraph != "":
                combined_paragraph += paragraph
                combined_paragraphs_list.append(combined_paragraph.strip("\n"))
                combined_paragraph = ""
            else:
                combined_paragraphs_list.append(paragraph)

    return combined_paragraphs_list

def generate_filtered_paragraphs_csv(db):
    '''
    publisher_name, url, article_title, paragraph_id, paragraph_content, author_name, published_time

    generate a csv files in the current path

    :param db: database class that provides access for database
    :return: paragraphs_dataframe, dictionary that contains filtered paragraphs
    '''

    ''' example:
    ({'name': ['Raphael', 'Donatello'],
                   'mask': ['red', 'purple'],
                   'weapon': ['sai', 'bo staff']})
    '''

    # create dataframe for paragraphs
    paragraphs_dataframe = dict()
    paragraphs_dataframe['publisher_name'] = list()
    paragraphs_dataframe['url'] = list()
    paragraphs_dataframe['article_title'] = list()
    paragraphs_dataframe['paragraph_id'] = list()
    paragraphs_dataframe['paragraph_content'] = list()
    paragraphs_dataframe['author_name'] = list()
    paragraphs_dataframe['published_time'] = list()

    # filter out unrelated articles by using keyword filtering method in related_articles.py
    all_articles = filter_out_by_dictionary_for_all(db)

    for i in tqdm(range(len(all_articles))):
        article = all_articles[i]
        # dataframe in article
        # (publisher_name, article_url, article_title, article_id, article_content, author_name, published_time)

        # split article contents into paragraphs and ignore paragraphs after reference
        article_paragraphs = split_articles_into_clean_paragraphs(article[4])
        paragraph_index = 1
        # shorter 12-char-long md5 hexdigest
        article_id = shorter_md5_hexdigest(hashlib.md5(article[1].encode()).hexdigest())

        for article_paragraph in article_paragraphs:
            add_new_paragraphs(article, article_id, paragraph_index, article_paragraph, paragraphs_dataframe)
            # TODO: OPTIONAL: insert data into paragraphs TABLE
            # db.insert_paragraph(article[0], article[1], article[2], article_id+str(paragraph_index).zfill(3),
            #                     article_paragraph, article[5], article[6])
            paragraph_index += 1

    # dataframe in paragraph
    # (publisher_name, url, article_title, paragraph_id, paragraph_content, author_name, published_time)

    df = pd.DataFrame(paragraphs_dataframe)
    df.to_csv('complete_paragraphs.csv', sep=',', index=False)

    return paragraphs_dataframe


def generate_filtered_split_combined_paragraphs_csv(db, max_word_num):
    '''

    extended function from generate_filtered_paragraphs_csv
    split one paragraph into multiple paragraphs according to the max_word_num limit

    generate a csv files in the current path

    :return: (optional) paragraphs_dataframe, dictionary that contains filtered paragraphs
    '''
    # create dataframe for paragraphs
    paragraphs_dataframe = dict()
    paragraphs_dataframe['publisher_name'] = list()
    paragraphs_dataframe['url'] = list()
    paragraphs_dataframe['article_title'] = list()
    paragraphs_dataframe['paragraph_id'] = list()
    paragraphs_dataframe['paragraph_content'] = list()
    paragraphs_dataframe['author_name'] = list()
    paragraphs_dataframe['published_time'] = list()

    # filter out unrelated articles by using keyword filtering method in related_articles.py
    all_articles = filter_out_by_dictionary_for_all(db)

    for i in tqdm(range(len(all_articles))):
        article = all_articles[i]
        # dataframe in article
        # (publisher_name, article_url, article_title, article_id, article_content, author_name, published_time)

        # split article contents into paragraphs and ignore paragraphs after reference
        article_paragraphs = split_articles_into_clean_paragraphs(article[4])
        paragraph_index = 1
        # shorter 12-char-long md5 hexdigest
        article_id = shorter_md5_hexdigest(hashlib.md5(article[1].encode()).hexdigest())

        # combine short paragraphs with the configuration of min_word_len
        combined_article_paragraphs = combine_paragraph(article_paragraphs, min_words_len=10)

        for article_paragraph in combined_article_paragraphs:
            # check if need split paragraphs
            new_paragraph = split_paragraph(article_paragraph, max_word_num)
            for paragraph in new_paragraph:
                add_new_paragraphs(article, article_id, paragraph_index, paragraph, paragraphs_dataframe)
                paragraph_index += 1

    df = pd.DataFrame(paragraphs_dataframe)
    df.to_csv('split_paragraphs.csv', sep=',', index=False)

    return paragraphs_dataframe


def tokenized_paragraphs(paragraph_contents):
    '''

    take paragraph_contents into tokenized words

    :param paragraph_contents: a list of paragraphs
    :return: a list of tokenized words
    '''

    # tokenize
    tokenizer = RegexpTokenizer(r'[a-zA-Z]{2,}')
    paragraphs_in_words = list()

    for paragraph in paragraph_contents:
        tokenized_paragraph = [word for word in tokenizer.tokenize(paragraph.lower())]
        paragraphs_in_words.append(tokenized_paragraph)

    return paragraphs_in_words


def plot_paragraphs_words(paragraph_contents):
    '''

    give the plot of x: the number of words per paragraphs
                    y: the number of paragraphs that have such # of words

    :param paragraph_contents:
    :return:
    '''
    # tokenize
    tokenizer = RegexpTokenizer(r'[a-zA-Z]{2,}')
    paragraph_word_counting = list()

    for paragraph in paragraph_contents:
        tokenized_paragraph = [word for word in tokenizer.tokenize(paragraph.lower())]
        if len(tokenized_paragraph) != 0:
            paragraph_word_counting.append(len(tokenized_paragraph))

    counter = collections.Counter(paragraph_word_counting)
    plt.bar(list(counter.keys()), list(counter.values()))
    plt.xlabel('the number of words')
    plt.ylabel('paragraphs with such words')
    plt.show()

def sampling_short_paragraphs(paragraphs_dataframe, short_num, sampling_num):
    '''

    print # sampling_num of short paragraphs
    '''
    paragraph_contents = paragraphs_dataframe["paragraph_content"]
    paragraphs_in_words = tokenized_paragraphs(paragraph_contents)
    short_paragraphs = list()



    for i in range(len(paragraphs_in_words)):
        paragraph = paragraphs_in_words[i]
        if len(paragraph) <= short_num and len(paragraph) != 0:
            short_paragraphs.append((" ".join(paragraph), paragraphs_dataframe["url"][i]))

    print(len(short_paragraphs))
    # sample_short_paragraphs = random.sample(short_paragraphs, sampling_num)

    # print(len(short_paragraphs))
    # for short_paras, url in sample_short_paragraphs:
    #     print(short_paras, url)






if __name__ == '__main__':
    db = database()
    paragraphs_dataframe = generate_filtered_paragraphs_csv(db)
    print(paragraphs_dataframe["paragraph_id"].index("425439079815057001"))



    # sampling_short_paragraphs(paragraphs_dataframe, 5, 100)

    # paragraphs_dataframe = generate_filtered_split_combined_paragraphs_csv(db, max_word_num=80)


    # plot_paragraphs_words(paragraphs_dataframe["paragraph_content"])

    # print(sampling_short_paragraphs(paragraphs_dataframe, 9, 100))











