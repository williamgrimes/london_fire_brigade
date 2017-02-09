from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
import pandas as pd


class CorpusExtractor(object):
    """methods for the extraction of a text corpus from a data frame"""

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

    def extract_entire_corpus(data_frame, text_columns):
        """Return text corpus from text columns of data frame."""
        corpus = data_frame[text_columns]
        corpus = corpus.dropna(how='all')
        corpus = corpus.fillna('')
        corpus = corpus.applymap(str)
        for index, row in corpus.iterrows():
            similarity_score = CorpusExtractor.text_similarity_measure(row[0], row[1])
            if similarity_score > 0.5:
                if len(row[0]) >= len(row[1]):
                    row[1] = ''
                else:
                    row[0] = ''
        corpus = corpus[text_columns].apply(lambda x: ' '.join(x), axis=1)
        corpus = corpus.str.lower()
        return corpus

    def is_key_word_index(key_word, corpus):
        """Return indicies of corpus rows containing key word."""
        key_word_boolean = []
        for item in corpus.iteritems():
            item_list = str(item).split()
            key_word_boolean.append(key_word in item_list)
        return key_word_boolean

    def extract_key_word_data_frame(data_frame, text_columns, key_word):
        """Return dataframe  containing the key word."""
        entire_corpus = CorpusExtractor.extract_entire_corpus(data_frame,
                                                              text_columns)
        key_word_boolean = CorpusExtractor.is_key_word_index(key_word,
                                                             entire_corpus)
        key_word_data_frame = data_frame[key_word_boolean]
        return key_word_data_frame

    def extract_key_word_corpus(data_frame, text_columns, key_word):
        """Return corpus containing the key word."""
        entire_corpus = CorpusExtractor.extract_entire_corpus(data_frame,
                                                              text_columns)
        key_word_boolean = CorpusExtractor.is_key_word_index(key_word,
                                                             entire_corpus)
        corpus = entire_corpus[key_word_boolean]
        return corpus


class TopicModelling(object):
    """
    This class provides methods for applying Non-negative Matrix Factorization
    and Latent Dirichlet Allocation on a corpus of documents and
    extract additive models of the topic structure of the corpus.
    The output is a list of topics, each represented as a list of terms
    (weights are not shown).
    """

    def get_top_words(vector, model, n_top_words):
        """get top words from each topic"""
        topics = []
        for topic_idx, topic in enumerate(model.components_):
            topics.append([['topic ' + str(topic_idx)],
                           [vector.get_feature_names()[i] for i in
                            topic.argsort()[:-n_top_words - 1:-1]]])
        return topics

    def print_top_words(vector, model, n_top_words):
        """print top words from each topic"""
        for topic_idx, topic in enumerate(model.components_):
            print("Topic #%d:" % topic_idx)
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
        vectorized = TopicModelling.model_vectorizer(vectorization, n_features)
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
                max_iter=5,
                learning_method='online',
                learning_offset=50.,
                random_state=0
            ).fit(vectorized_fit)
        return vectorized, model
