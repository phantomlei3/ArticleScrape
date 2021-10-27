'''

The final work of article filter based on all available models deisgned and generated
It will utilize all models in classification folders to classify all paragraphs in "paragraphs.csv"
    and generate classification results in one csv file as well as evaluation metrix in another csv files.

'''
import pandas as pd
import os.path

from sklearn.metrics import precision_score, recall_score, f1_score
from proc_annotation import load_paragraph_annotations

# all available models

# logistic regression
from classification.baseline import wrapped_logisitic_regression_model
# native bayes
from classification.naive_bayes import wrapped_naive_bayes_model
# svm
from classification.svm import wrapped_svm_model
# gradient boosting
from classification.gradient_boosting import wrapped_gradient_boosting_model

def read_from_paragraphs_csv(corpus_path):
    '''
    helper function

    read pargraphs.csv files in corpus
        the fields of pargraphs.csv:
            publisher_name, url, article_title, paragraph_id, paragraph_content, author_name, published_time

    :return: paragraph_contents as observations, X
    '''

    df = pd.read_csv(corpus_path)
    paragraph_cotents = df["paragraph_content"]

    return [str(each) for each in paragraph_cotents.to_list()]


def update_paragraphs_classification_csv(corpus_path, previous_output_path, model_name, predictions):
    '''
    helper function

    update the corresponding file in corpus: add the new model and its predictions into the file
    "corpus/paragraphs_w_class.csv"

    :param model_name, the name of model used for classification, a string
                        will be the column name for the model
    :param predictions, the prediction results, a list of floats that represents probability of binary class
                        in the order of "paragraph.csv" input
    '''
    # if previous_output_path file exists, add the prediction of new model as the new column
    try:
        df = pd.read_csv(previous_output_path)
    except:
        df = pd.read_csv(corpus_path)

    df[model_name] = predictions
    df.to_csv(output_path, sep=',', index=False)


def update_evaluation_csv(model_name, precision, recall, f1):
    '''
    helper function

    :param model_name: the name of model used for classification, a string
    :param precision: the precision score of the model on testing data
    :param recall: the recall score of the model on testing data
    :param f1_score: the f1_score of the model on testing data
    :return:
    '''
    df = None
    if not os.path.isfile('corpus/evaluation_matrix.csv'):
        data = {'model_name': [],
                'precision': [],
                'recall': [],
                'f1_score': []}
        df = pd.DataFrame(data)
    else:
        df = pd.read_csv('corpus/evaluation_matrix.csv')

    # add the evaluation of new model on testing data
    new_row = {'model_name': model_name, 'precision': precision, 'recall': recall, 'f1_score': f1}
    df_updated = df.append(new_row, ignore_index=True)
    df_updated.to_csv('corpus/evaluation_matrix.csv', sep=',', index=False)



def evaluate_model(model):
    '''
    helper function

    :param model: wrapped class of model that contains one function predict
    '''
    test_annotations = load_paragraph_annotations("test")
    #  extract paragraph content and its annotations
    #   from (paragraph_id, publisher_name, article_url, paragraph_content, content_annotation)
    test_paragraph_contents = [str(each[3]) for each in test_annotations]
    y_true = [each[4] for each in test_annotations]

    # get predictions from model and evaluation
    y_pred = model.predict(test_paragraph_contents)
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    update_evaluation_csv(model.model_name, precision, recall, f1)



def generate_predictions(corpus_path, previous_output_path, model):
    '''

    main function to generate predcitions and store it in "corpus/paragraphs_w_class.csv"

    :param model: wrapped class of model that contains one function predict
    '''
    # generate evaluation first
    evaluate_model(model)

    # generate classification(probabilit score) of the model for the corpus
    corpus = read_from_paragraphs_csv(corpus_path)
    proba_predictions = model.predict_proba(corpus)
    update_paragraphs_classification_csv(corpus_path, previous_output_path, model.model_name, proba_predictions)


if __name__ == '__main__':
    # logistic regression unigram frequencies
    model = wrapped_logisitic_regression_model()

    # svm unigram tf-idf
    # model = wrapped_svm_model()

    # gradient boosting
    # model =wrapped_gradient_boosting_model()

    # naive bayes unigram tf-idf
    # model = wrapped_naive_bayes_model()

    corpus_path = 'corpus/paragraphs.csv'
    previous_output_path = 'corpus/paragraphs_w_class.csv'

    generate_predictions(corpus_path, previous_output_path, model)