class CorpusExtractor(object):
    """methods for the extraction of a text corpus from a data frame"""

    def extract_entire_corpus(data_frame, text_columns):
        """Return text corpus from columns of data frame."""
        corpus = data_frame[text_columns]
        corpus = corpus.dropna(how='all')
        corpus = corpus.fillna('')
        corpus = corpus.applymap(str)
        corpus = corpus[text_columns].apply(lambda x: ''.join(x), axis=1)
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
        entire_corpus = CorpusExtractor.extract_entire_corpus(
            data_frame, text_columns)
        key_word_boolean = CorpusExtractor.is_key_word_index(
            key_word, entire_corpus)
        key_word_data_frame = data_frame[key_word_boolean]
        return key_word_data_frame

    def extract_key_word_corpus(data_frame, text_columns, key_word):
        """Return corpus containing the key word."""
        entire_corpus = CorpusExtractor.extract_entire_corpus(
            data_frame, text_columns)
        key_word_boolean = CorpusExtractor.is_key_word_index(
            key_word, entire_corpus)
        corpus = entire_corpus[key_word_boolean]
        return corpus
