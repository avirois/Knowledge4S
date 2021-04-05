import re
from math import sqrt
from modules.stop_words import stopwords
from modules.util import Singleton

punctuation = re.compile(r"([\[\"$%&\'@!#()*+,-./\\:?;<=>\[\]^_`{|}~])|([.])")
pattern = re.compile(r"\w+")


def tokenize(text):
    """Our tokenizer."""
    text = text.lower()
    matches = pattern.finditer(text)
    tokens = []
    for match in matches:
        start = match.start()
        end = match.end()
        tokens.append(text[start:end])
    return tokens


def remove_panctuation(text):
    """Remove panctuations from text."""
    return re.sub(punctuation, "", text)


def cosine_similarity(v1, v2):
    "compute cosine similarity of v1 to v2: (v1 dot v2)/{||v1||*||v2||)"
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]
        y = v2[i]
        sumxx += x * x
        sumyy += y * y
        sumxy += x * y
    return sumxy / sqrt(sumxx * sumyy)


class FreeTextSearchEngine(metaclass=Singleton):
    """Eager initialization singeton free search engine."""

    def __init__(self, documents_text: dict[str, str]) -> None:
        """
        Create instance.

        Create FreeTextSearchEngine instance
        and initialze the term frequency of given documents.
        """
        self.term_frequency: dict[str, list[float]] = {}
        self.word_to_index: dict[str, int] = {}
        self.free_index = 0
        self.stopwords = stopwords
        for doc_id, text in documents_text.items():
            self.add_document(doc_id, text)

    def add_document(self, doc_id, document_text):
        """Calculate and save given document tf."""
        vector: list[float] = [0 for _ in range(self.free_index)]
        processed_tokens = self.__preprocess(document_text)
        number_of_terms = len(processed_tokens)
        unique_words = set(processed_tokens)
        for word in unique_words:
            index = None
            if word in self.word_to_index.keys():
                # case known word
                index = self.word_to_index[word]
            else:
                # case new word
                index = self.free_index
                self.free_index += 1
                self.word_to_index[word] = index
                for id_ in self.term_frequency.keys():
                    self.term_frequency[id_].append(0)
                vector.append(0)
            vector[index] = (processed_tokens.count(word) + 1) / (number_of_terms + 1)
            self.term_frequency[doc_id] = vector

    def __preprocess(self, text):
        """
        Preprocess text.

        Remove panctuation.
        Tokenize.
        Remove stopwords.
        """
        tokens = tokenize(remove_panctuation(text))
        without_stopwords = []
        for token in tokens:
            if token not in self.stopwords:
                without_stopwords.append(token)
        return without_stopwords

    def __get_query_vector(self, query):
        vector: list[float] = [0 for _ in range(self.free_index)]
        tokens = self.__preprocess(query)
        known_tokens = list()
        for token in tokens:
            if token in self.word_to_index.keys():
                known_tokens.append(token)
        number_of_terms = len(known_tokens)
        unique_words = set(known_tokens)
        for word in unique_words:
            index = None
            index = self.word_to_index[word]
            vector[index] = (known_tokens.count(word) + 1) / (number_of_terms + 1)
        return vector

    def search_free_text(self, query, document_ids):
        """
        Order documents by similarity to query.

        Preprocess query and calculate its tf vector.
        Calculate cosine similarity of the query tf to each document tf.
        return sorted documents ids by similarity.
        """
        pairs: list[tuple[float, str]] = list()
        q_vector = self.__get_query_vector(query)
        flag = False
        for i in q_vector:
            if i != 0:
                flag = True
                break
        if flag:
            for id_ in document_ids:
                pairs.append(
                    (
                        cosine_similarity(q_vector, self.term_frequency[str(id_)]),
                        str(id_),
                    )
                )
            pairs.sort(key=lambda x: x[0], reverse=True)
            return (x[1] for x in pairs)
        else:
            return document_ids
