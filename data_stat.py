from PostgreSQL.database import database
from related_articles import filter_out_by_dictionary_for_all
from statistics import mean

# tokenization
from nltk.tokenize import RegexpTokenizer

def get_clength_limit_paragraphs(clength_limit, upperbound, articles):
    '''

    :param clength_limit: the char minimum limit for a paragraph to filter out
    :param articles: a list of articles
    :return: a list of paragraphs
    '''


    paragraphs = list()
    for article in articles:
        article_paragraphs = article.split("\n")
        for raw_paragraph in article_paragraphs:
            paragraph = raw_paragraph.strip('\n').strip()
            if clength_limit <= len(paragraph) <= upperbound and len(paragraph) != 0:
                paragraphs.append(paragraph)
    return paragraphs

def get_wlength_limit_paragraphs(wlength, articles):

    # get 0 word limit paragraphs
    paragraphs = get_clength_limit_paragraphs(0, articles)

    # tokenize
    tokenizer = RegexpTokenizer(r'[a-zA-Z]{2,}')
    tokenized_paragraphs = list()
    for paragraph in paragraphs:
        tokenized_paragraph = [word for word in tokenizer.tokenize(paragraph.lower())]
        if len(tokenized_paragraph) >= wlength and len(tokenized_paragraph) != 0:
            tokenized_paragraphs.append(tokenized_paragraph)

    return tokenized_paragraphs

def get_paragraph_average(articles):
    counts = list()
    for article in articles:
        article_paragraphs = article.split("\n")
        count = 0
        for raw_paragraph in article_paragraphs:
            paragraph = raw_paragraph.strip('\n').strip()
            if len(paragraph) != 0:
                count += 1
        counts.append(count)

    return mean(counts)
if __name__ == '__main__':
    db = database()
    all_articles = filter_out_by_dictionary_for_all(db)

    # character limit
    # paragraphs = get_clength_limit_paragraphs(0, all_articles)
    # print(len(max(paragraphs, key=len)))

    # word limit
    # paragraphs = get_wlength_limit_paragraphs(0, all_articles)
    # print(len(paragraphs))
    # print(len(min(paragraphs, key=len)))

    # get average
    # print(get_paragraph_average(all_articles))

    paragraphs = get_clength_limit_paragraphs(0, 3600, all_articles)
    print(max(paragraphs, key=len))