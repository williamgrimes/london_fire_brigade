import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

import textacy
import re
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer

from nltk.stem.porter import PorterStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import SnowballStemmer


additional_stop_words = ['smoke', 'floor', 'flat', 'attended',
                         'property', 'room', 'alarm', 'crews', 'ground',
                         'building', 'brigade', 'house', 'damage',
                         'extinguished', 'floors', 'occurred', 'fitted',
                         'incident', 'appliances', 'using', 'area', 'kitchen',
                         'safety', 'small', 'flats', 'bedroom', 'removed',
                         'used', 'persons', 'damaged']


def preprocess_corpus_nltk(corpus):
    """Remove stop words, lemmatize and tokenizing"""
    stop_words = stopwords.words("english")
    #stop_words = stop_words + additional_stop_words
    lemmatizer = nltk.stem.WordNetLemmatizer()
    for index, row in corpus.iteritems():
        sentence = row.lower()
        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(sentence)
        filtered_words = [w for w in tokens if not w in stop_words]
        lemmatized_words = [lemmatizer.lemmatize(w) for
                            w in filtered_words]
        corpus.loc[index] = " ".join(lemmatized_words)

def preprocess_corpus_textacy(corpus):
    """Remove numbers, whitespace, punctuation and make lower case"""
    preprocessed = corpus.copy()
    for index, row in preprocessed.iteritems():
        preprocessed[index] = re.sub(r'\w*\d\w*', '', preprocessed[index]).strip() #remove numbers
        preprocessed[index] = textacy.preprocess.normalize_whitespace(preprocessed[index])
        preprocessed[index] = textacy.preprocess_text(preprocessed[index], lowercase=True, no_punct=True)
    print('preprocessed corpus')
    return preprocessed

def text_similarity_measure(doc1, doc2):
    """Return the similarity between two tokenized sets of strings"""
    tokenize = lambda doc: doc.lower().split(" ")
    doc1 = set(tokenize(doc1))
    doc2 = set(tokenize(doc2))
    word_intersection = doc1.intersection(doc2)
    if len(doc1) >= len(doc1):
        words = doc2
    else:
        words = doc1
    similarity_measure = len(word_intersection)/len(words)
    return similarity_measure

def is_key_word_index(key_word, corpus):
    """Return indicies of corpus rows containing key word."""
    key_word_boolean = []
    for item in corpus.iteritems():
        item_list = str(item).split()
        key_word_boolean.append(key_word in item_list)
    return key_word_boolean

class CorpusExtractor(object):
    """methods for the extraction of a text corpus from a data frame"""

    def __init__(self):
        self.text_columns = ['BriefDescriptionOfFire','FurtherInformation']
        self.similarity_score = 0.5

    def extract_corpus(self, data_frame):
        """Return text corpus from text columns of data frame. Using free text
        columns. If the columns have a word set similarity greater than the
        similarity score then the shorter text field is deleted to avoid
        replication of text.
        """
        print('extracting corpus')
        corpus = data_frame[self.text_columns]
        corpus = corpus.dropna(how='all')
        corpus = corpus.fillna('')
        corpus = corpus.applymap(str)
        for index, row in corpus.iterrows():
            similarity_score = text_similarity_measure(row[0], row[1])
            row[0] = ' '.join(row[0].split()) # remove excess whitespace
            row[1] = ' '.join(row[1].split())
            if similarity_score > self.similarity_score:
                if len(row[0]) >= len(row[1]):
                    row[1] = ''
                else:
                    row[0] = ''
        corpus = corpus[self.text_columns].apply(lambda x: ' '.join(x), axis=1)
        return corpus

    def extract_documents_longer_than(self, corpus, word_count):
        """Return corpus only containing documents longer than word_count."""
        number_of_words = corpus.str.split().str.len()
        corpus = corpus[number_of_words > word_count]
        return corpus

    def extract_documents_shorter_than(self, corpus, word_count):
        """Return corpus only containing documents shorter than word_count."""
        number_of_words = corpus.str.split().str.len()
        corpus = corpus[number_of_words < word_count]
        return corpus

    def extract_key_word_corpus(self, data_frame, key_word):
        """Return corpus containing the key word."""
        entire_corpus = CorpusExtractor.extract_corpus(self, data_frame)
        key_word_boolean = is_key_word_index(key_word, entire_corpus)
        corpus = entire_corpus[key_word_boolean]
        return corpus

    def extract_key_word_data_frame(self, data_frame, key_word):
        """Return dataframe containing the key word."""
        corpus = CorpusExtractor.extract_key_word_corpus(self,
                                                         data_frame,
                                                         key_word)
        key_word_data_frame = data_frame.ix[corpus.index]
        return key_word_data_frame

    def extract_free_text_only_data_frame(self, data_frame):
        """Return dataframe containing only free text data."""
        data_frame_free_text = data_frame.iloc[data_frame[self.text_columns].dropna(how='all').index]
        data_frame_free_text.reset_index()
        return data_frame_free_text
