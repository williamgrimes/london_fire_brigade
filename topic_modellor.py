"""
This module provides functions for applying Non-negative Matrix Factorization
and Latent Dirichlet Allocation on a corpus of documents and
extract additive models of the topic structure of the corpus.
The output is a list of topics, each represented as a list of terms
(weights are not shown).
"""

import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation


def get_top_words(vector, model, n_top_words):
    """get top word and value tuple for each topic as list of zipped"""
    topics = []
    for topic_idx, topic in enumerate(model.components_):
        words = [vector.get_feature_names()[i] for i in topic.argsort()[:-n_top_words - 1:-1]]
        values = (np.sort(model.components_[topic_idx,:])[-n_top_words:])[::-1]
        top_words = list(zip(words, values))
        topics.append(top_words)
    return topics

def print_top_words(vector, model, n_top_words):
    """print top words from each topic"""
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % (topic_idx + 1))
        print(" ".join([vector.get_feature_names()[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()

def model_vectorizer(vectorizer, n_features):
    """convert text corpus to tf or tfifd vectors"""
    if vectorizer == 'tfidf':
        vectorized = TfidfVectorizer(
            max_features=n_features,
            max_df=0.95,
            min_df=2,
            stop_words='english'
        )
    if vectorizer == 'tf':
        vectorized = CountVectorizer(
            max_features=n_features,
            max_df=0.95,
            min_df=2,
            stop_words='english'
        )
    return vectorized

def topic_modelling(model, vectorization, n_features, corpus, n_topics):
    """use NMF or LDA to model topics in corpus"""
    vectorized = model_vectorizer(vectorization, n_features)
    vectorized_fit = vectorized.fit_transform(list(corpus))
    if model == 'NMF':
        model = NMF(
            n_components=n_topics,
            random_state=1,
            alpha=.1,
            l1_ratio=.5
        ).fit(vectorized_fit)
    if model == 'LDA':
        model = LatentDirichletAllocation(
            n_topics=n_topics,
            max_iter=50,
            learning_method='online',
            learning_offset=50.,
            random_state=0
        ).fit(vectorized_fit)
    return vectorized, vectorized_fit,  model

def classify_model_topics(model, vector_fit):
    """from model classify free text topics by maximum likelihood"""
    topic_probability = model.transform(vector_fit)
    #topic_probability = np.delete(topic_probability, 10, axis=1)
    topic_classified = pd.Series(np.argmax(topic_probability, 1) + 1)
    return topic_classified

def get_topic_probabilities(model, vector_fit):
    """return all probabilities as dataframe"""
    topic_probability = model.transform(vector_fit)
    topic_probability = pd.DataFrame(topic_probability)
    return topic_probability
