'''

Aggregating the prediction results from multiple paragraphs and from multiple models
    into one single relevance score for one article

'''

import numpy as np
import pandas as pd
from glob2 import glob

# the name of models as key and its f1 performance as value
MODELS = {"logisitic_regression_unigram_frequencies": 0.8663101604278076,
          "svm_unigram_tfidf": 0.8651488616462347,
          "naive_bayes_model_unigram_tfidf": 0.8211508553654743,
          "gradient_boosting_unigram_tfidf": 0.9283276450511946}

class ArticleRelevance:
    def __init__(self, all_paragraphs_df):
        '''
        :param all_paragraphs_info: pandas dataframe that at least contain the following columns
        publisher_name,article_url,article_title,paragraph_id,paragraph_content,author_name,published_time, (model_predictions)
        '''

        # extract article id from paragraph_id and get its prediction results from its all paragraphs( in a list)
        self.article_predictions_dict = dict()
        for _, paragraph in all_paragraphs_df.iterrows():
            article_id = paragraph['paragraph_id'][:-3]
            if article_id not in self.article_predictions_dict:
                self.article_predictions_dict[article_id] = dict()
                for model_name in MODELS.keys():
                    self.article_predictions_dict[article_id][model_name] = list()

            for model_name in MODELS.keys():
                self.article_predictions_dict[article_id][model_name].append(paragraph[model_name])

        # saved variable


    def generate_relevance_score(self, article_id):
        '''

        The relevance score function for one article based on the f1 scores of models

        '''
        # f1 weight for one model = model's f1 score
        # prediction score of one article from one model  = model's normalized weight * avg(model's prediction results of article's paragraphs)
        # relevance scores for one article = sum of prediction score from all models
        relevance_score = 0
        for model_name in MODELS.keys():
            relevance_score += MODELS[model_name] * np.average(self.article_predictions_dict[article_id][model_name])
        return relevance_score

    def get_article_relevance(self):
        '''

        :return: a dictionary {article id: relevance score}
        '''

        article_relevance = dict()
        for article_id in self.article_predictions_dict.keys():
            article_relevance[article_id] = self.generate_relevance_score(article_id)
        return article_relevance.copy()


if __name__ == '__main__':
    corpus_path = 'corpus/paragraphs_w_class.csv'
    df = pd.read_csv(corpus_path)

    print(ArticleRelevance(df))