from django.db import models
import os
import argparse
import numpy as np
import scipy
import sklearn.pipeline
from pathlib import Path
from typing import List, Any
from lime.lime_text import LimeTextExplainer
from tqdm import tqdm
import spacy
from django.conf import settings
from django.conf.urls.static import static
import ast
import datetime
import collections
import re, string
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
METHODS = {
    'textblob': {
        'class': "TextBlobExplainer",
        'file': None
    },
    'vader': {
        'class': "VaderExplainer",
        'file': None
    },
    'logistic': {
        'class': "LogisticExplainer",
        'file': "data/sst/sst_train.txt"
    },
    'svm': {
        'class': "SVMExplainer",
        'file': "data/sst/sst_train.txt"
    },
    'fasttext': {
        'class': "FastTextExplainer",
        'file': "models/fasttext/sst5_hyperopt.ftz"
    },
    'flair': {
        'class': "FlairExplainer",
        'file': "models/flair/best-model-elmo.pt"
    },
    'transformer': {
        'class': "TransformerExplainer",
        'file': "models/transformer"
    }
}


def tokenizer(text: str) -> str:
    "Tokenize input string using a spaCy pipeline"
    nlp = spacy.blank('en')
    nlp.add_pipe(nlp.create_pipe('sentencizer'))  # Very basic NLP pipeline in spaCy
    doc = nlp(text)
    tokenized_text = ' '.join(token.text for token in doc)
    return tokenized_text


def remove_noise(text, stop_words = ()):



    for token, tag in pos_tag(text):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        nlp = spacy.blank('en')
        nlp.add_pipe(nlp.create_pipe('sentencizer'))  # Very basic NLP pipeline in spaCy
        doc = nlp(token)
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            tokenized_text = ' '.join(token.text for token in doc)
    return tokenized_text




def explainer_class(method:str, filename: str) -> Any:
    "Instantiate class using its string name"
    classname = METHODS[method]['class']
    class_ = globals()[classname]
    return class_(filename)


class VaderExplainer:
    """Class to explain classification results of Vader.
       Although VADER compound scores are in the range [-1.0, 1.0], we `simulate` the
       probabilities that the model predicts using 5 equally-sized bins in this interval.
       and using a normal distribution to artificially create class probabilities.

       For example:
       If Vader predicts a float sentiment score of 0.6834, this translates to an
       integer-scaled class prediction of 4, assuming equally-sized bins for 5 classes.
       We take this value and generate a normal distribution PDF with exactly 5 values.
       The PDF is used as a simulated probability of classes that we feed to the LIME explainer.
    """
    def __init__(self, model_file: str = None) -> None:
        from nltk.sentiment.vader import SentimentIntensityAnalyzer
        self.vader = SentimentIntensityAnalyzer()
        self.classes = np.array([1, 2, 3, 4, 5])

    def score(self, text: str) -> float:
        return self.vader.polarity_scores(text)['compound']

    def predict(self, texts: List[str]) -> np.array([float, ...]):
        probs = []
        for text in texts:

            # First, offset the float score from the range [-1, 1] to a range [0, 1]
            offset = (self.score(text) + 1) / 2.
            # Convert float score in [0, 1] to an integer value in the range [1, 5]
            binned = np.digitize(5 * offset, self.classes) + 1
            # Similate probabilities of each class based on a normal distribution
            simulated_probs = scipy.stats.norm.pdf(self.classes, binned, scale=0.5)
            probs.append(simulated_probs)
        return np.array(probs)


def explainer(
        method: str,
        path_to_file: str,
        text: str,
        num_samples: int) -> LimeTextExplainer:


        """Run LIME explainer on provided classifier"""

        model = explainer_class(method, path_to_file)
        predictor = model.predict

        # Create a LimeTextExplainer
        explainer = LimeTextExplainer(
            # Specify split option
            split_expression=lambda x: x.split(),
            # Our classifer uses bigrams or contextual ordering to classify text
            # Hence, order matters, and we cannot use bag of words.
            bow=False,
            # Specify class names for this case
            class_names=["very_neg", "negative", "neutral", "positive", "very_pos"]
        )

        # Make a prediction and explain it:
        exp = explainer.explain_instance(
            text,
            classifier_fn=predictor,
            top_labels=1,
            num_features=20,
            num_samples=num_samples,
        )

        return exp








# Create your models here.


class EnglishProcessing(models.Model):



    def main(self,text: str,num_samples: str) -> None:
        # Get list of available methods:


        path_to_file = METHODS['vader']['file']

        # Run explainer function

        text = tokenizer(text)  # Tokenize text using spaCy before explaining
        

        exp = explainer('vader', path_to_file, text, int(num_samples))

        # Output to HTML
        #output_filename = settings.STATIC_ROOT +'/temp/ '+"{}-explanation-{}.html".format('example','vader')
        #print(output_filename)
        #exp.save_to_file(output_filename)

        classification = exp.top_labels

        return classification[0]

    def explanation_plotter(self,text: str) -> None:
        # Get list of available methods:


        path_to_file = METHODS['vader']['file']

        # Run explainer function
        text = tokenizer(text)  # Tokenize text using spaCy before explaining

        exp = explainer('vader', path_to_file, text, num_samples = 2)

        # Output to HTML
        output_filename = settings.STATIC_ROOT +'/temp/'+"{}-explanation-{}.html".format('example','vader')

        #exp.save_to_file(output_filename)
        #exp.show_in_notebook(text=True)
        return exp

    def dictionaries_among_one_category(self,category,comment_classifier):

        pure_emoji_dic=ast.literal_eval(comment_classifier.pure_emoji_dic)
        emoji_pure_arabic_dic = ast.literal_eval(comment_classifier.emoji_pure_arabic_dic)
        emoji_pure_english_dic = ast.literal_eval(comment_classifier.emoji_pure_english_dic)
        emoji_mixed_lang_dic = ast.literal_eval(comment_classifier.emoji_mixed_lang_dic)
        emoji_arabic_with_others_dic=ast.literal_eval(comment_classifier.emoji_arabic_with_others_dic)
        emoji_english_with_others_dic =ast.literal_eval(comment_classifier.emoji_english_with_others_dic)
        emoji_ar_en_dic=ast.literal_eval(comment_classifier.emoji_ar_en_dic)
        emoji_exceptions_dic = ast.literal_eval(comment_classifier.emoji_exceptions_dic)
        emoji_other_language_dic =ast.literal_eval(comment_classifier.emoji_other_language_dic)
        emoji_useless_comment_dic=ast.literal_eval(comment_classifier.emoji_useless_comment_dic)
        pure_arabic_dic = ast.literal_eval(comment_classifier.pure_arabic_dic)
        pure_english_dic = ast.literal_eval(comment_classifier.pure_english_dic)
        mixed_lang_dic = ast.literal_eval(comment_classifier.mixed_lang_dic)
        exceptions_dic = ast.literal_eval(comment_classifier.exceptions_dic)
        other_language_dic =ast.literal_eval(comment_classifier.other_language_dic)
        useless_comment_dic=ast.literal_eval(comment_classifier.useless_comment_dic)
        arabic_with_others_dic=ast.literal_eval(comment_classifier.arabic_with_others_dic)
        english_with_others_dic =ast.literal_eval(comment_classifier.english_with_others_dic)
        ar_en_dic=ast.literal_eval(comment_classifier.ar_en_dic)
        dictionaries = {}
        if category == 'English':

            dictionaries.update(emoji_pure_english_dic)
            dictionaries.update(pure_english_dic)
            dictionaries.update(emoji_english_with_others_dic)
            dictionaries.update(english_with_others_dic)
            dic = {
            'emoji_pure_english_dic' :len(emoji_pure_english_dic) ,
            'pure_english_dic': len(pure_english_dic) ,
            'emoji_english_with_others_dic':len(emoji_english_with_others_dic) ,
            'english_with_others_dic': len(english_with_others_dic)
            }
            print("dictionay_length_pairs created successfully")
            return dic, dictionaries
        if category == 'pure_emoji':
            dictionaries.update(pure_emoji_dic)
            dic = {
            'pure_emoji' : len(pure_emoji_dic),
            }
            print("dictionay_length_pairs created successfully")
            return dic, dictionaries
        if category == 'Arabic':
            dictionaries.update(emoji_pure_arabic_dic)
            dictionaries.update(arabic_with_others_dic)
            dictionaries.update(pure_arabic_dic)
            dictionaries.update(emoji_arabic_with_others_dic)
            dic = {
            'emoji_pure_arabic_dic' : len(emoji_pure_arabic_dic) ,
            'arabic_with_others_dic' : len(arabic_with_others_dic) ,
            'pure_arabic_dic' : len(pure_arabic_dic) ,
            'emoji_arabic_with_others_dic' : len(emoji_arabic_with_others_dic)
            }
            print("dictionay_length_pairs created successfully")
            return dic, dictionaries
        if category == 'Mix':
            dictionaries.update(emoji_mixed_lang_dic)
            dictionaries.update(mixed_lang_dic)
            dictionaries.update(ar_en_dic)
            dictionaries.update(emoji_ar_en_dic)
            dic = {
            'emoji_mixed_lang_dic' : len(emoji_mixed_lang_dic) ,
            'mixed_lang_dic' :len(mixed_lang_dic) ,
            'ar_en_dic' : len(ar_en_dic) ,
            'emoji_ar_en_dic' :len(emoji_ar_en_dic)
            }
            print("dictionay_length_pairs created successfully")
            return dic, dictionaries
        if category == 'Others':
            dictionaries.update(other_language_dic)
            dictionaries.update(emoji_other_language_dic)

            dic = {
            'other_language_dic' : len(other_language_dic) ,
            'emoji_other_language_dic': len(emoji_other_language_dic)
            }
            print("dictionay_length_pairs created successfully")
            return dic, dictionaries
        if category == 'useless_and_exceptions':
            dictionaries.update(emoji_exceptions_dic)
            dictionaries.update(emoji_useless_comment_dic)
            dictionaries.update(useless_comment_dic)
            dictionaries.update(exceptions_dic)
            dic = {
            'emoji_exceptions_dic' :   len(emoji_exceptions_dic) ,
            'emoji_useless_comment_dic' :   len(emoji_useless_comment_dic) ,
            'useless_comment_dic'  :  len(useless_comment_dic) ,
            'exceptions_dic' :    len(exceptions_dic),
            }
            print("dictionay_length_pairs created successfully")
            return dic, dictionaries

    def dictionary_among_one_category(self,category,comment_classifier):

        pure_emoji_dic=ast.literal_eval(comment_classifier.pure_emoji_dic)
        emoji_pure_arabic_dic = ast.literal_eval(comment_classifier.emoji_pure_arabic_dic)
        emoji_pure_english_dic = ast.literal_eval(comment_classifier.emoji_pure_english_dic)
        emoji_mixed_lang_dic = ast.literal_eval(comment_classifier.emoji_mixed_lang_dic)
        emoji_arabic_with_others_dic=ast.literal_eval(comment_classifier.emoji_arabic_with_others_dic)
        emoji_english_with_others_dic =ast.literal_eval(comment_classifier.emoji_english_with_others_dic)
        emoji_ar_en_dic=ast.literal_eval(comment_classifier.emoji_ar_en_dic)
        emoji_exceptions_dic = ast.literal_eval(comment_classifier.emoji_exceptions_dic)
        emoji_other_language_dic =ast.literal_eval(comment_classifier.emoji_other_language_dic)
        emoji_useless_comment_dic=ast.literal_eval(comment_classifier.emoji_useless_comment_dic)
        pure_arabic_dic = ast.literal_eval(comment_classifier.pure_arabic_dic)
        pure_english_dic = ast.literal_eval(comment_classifier.pure_english_dic)
        mixed_lang_dic = ast.literal_eval(comment_classifier.mixed_lang_dic)
        exceptions_dic = ast.literal_eval(comment_classifier.exceptions_dic)
        other_language_dic =ast.literal_eval(comment_classifier.other_language_dic)
        useless_comment_dic=ast.literal_eval(comment_classifier.useless_comment_dic)
        arabic_with_others_dic=ast.literal_eval(comment_classifier.arabic_with_others_dic)
        english_with_others_dic =ast.literal_eval(comment_classifier.english_with_others_dic)
        ar_en_dic=ast.literal_eval(comment_classifier.ar_en_dic)

        if category == 'English':

            dic = {
            'emoji_pure_english_dic' :len(emoji_pure_english_dic) ,
            'pure_english_dic': len(pure_english_dic) ,
            'emoji_english_with_others_dic':len(emoji_english_with_others_dic) ,
            'english_with_others_dic': len(english_with_others_dic)
            }
            print("dictionay_length_pairs created successfully")
            return dic
        if category == 'pure_emoji':
            dic = {
            'pure_emoji' : len(pure_emoji_dic),
            }
            print("dictionay_length_pairs created successfully")
            return dic
        if category == 'Arabic':
            dic = {
            'emoji_pure_arabic_dic' : len(emoji_pure_arabic_dic) ,
            'arabic_with_others_dic' : len(arabic_with_others_dic) ,
            'pure_arabic_dic' : len(pure_arabic_dic) ,
            'emoji_arabic_with_others_dic' : len(emoji_arabic_with_others_dic)
            }
            print("dictionay_length_pairs created successfully")
            return dic, dictionaries
        if category == 'Mix':
            dic = {
            'emoji_mixed_lang_dic' : len(emoji_mixed_lang_dic) ,
            'mixed_lang_dic' :len(mixed_lang_dic) ,
            'ar_en_dic' : len(ar_en_dic) ,
            'emoji_ar_en_dic' :len(emoji_ar_en_dic)
            }
            print("dictionay_length_pairs created successfully")
            return dic, dictionaries
        if category == 'Others':
            dic = {
            'other_language_dic' : len(other_language_dic) ,
            'emoji_other_language_dic': len(emoji_other_language_dic)
            }
            print("dictionay_length_pairs created successfully")
            return dic, dictionaries
        if category == 'useless_and_exceptions':
            dic = {
            'emoji_exceptions_dic' :   len(emoji_exceptions_dic) ,
            'emoji_useless_comment_dic' :   len(emoji_useless_comment_dic) ,
            'useless_comment_dic'  :  len(useless_comment_dic) ,
            'exceptions_dic' :    len(exceptions_dic),
            }
            print("dictionay_length_pairs created successfully")

            return dic

        # comments over time
    def comments_over_time_for_one_dic(self,dic):
        dates = list()

        for item in dic:
            date = dic[item]['date']
            date = date.replace("T", " ")
            date = date.replace("Z", "")
            date = date.strip()

            date_time_obj = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            date =  date_time_obj.date()

            dates.append(date)



        dates.sort()
        dates = [datetime.datetime.strftime(ts, "%Y-%m-%d") for ts in dates]

        counter=collections.Counter(dates)

        return counter.most_common()

    def polarity_decision_for_one_dic(self, polarity_dic):
        terms = ['very_negative','negative','neutral','positive','very_positive']

        very_negative = 1
        negative = 2
        neutral = 3
        positive = 4
        very_positive = 5
        score = 0
        overall_comments = 0

        for key ,item in polarity_dic.items():
            if key == 'positive':
                overall_comments += item
                temp = item * positive
                score += temp
                print('score for positive : ', temp)
            elif key == 'negative':
                overall_comments += item
                temp = item * negative
                score += temp
                print('score for negative : ', temp)
            elif key == 'very_positive':
                overall_comments += item
                temp = item * very_positive
                score += temp
                print('score for very_positive : ', temp)
            elif key == 'very_negative':
                overall_comments += item
                temp = item * very_negative
                score += temp
                print('score for very_negative : ', temp)
            else:
                overall_comments += item
                temp = item * neutral
                score += temp
                print('score for neutral : ', temp)
        try:
            print(score / overall_comments)
            given_value = score / overall_comments
            score_list = [1, 2, 3, 4, 5]
            index = min(score_list, key=lambda x:abs(x-given_value))
            print('the polarity for this video is :',terms[index-1])
            return terms[index-1]
        except :
            return "None"
