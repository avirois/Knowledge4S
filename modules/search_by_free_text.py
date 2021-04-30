"""
Search by free module.

In this module:

=> class:
    DocumentsTermsFrequency:
    Singleton class for eager initialization of the object.
    Object keep information about known words in known document,
    and documents terms frequencies.

    -> methods:
    order_by_similarity_to : order given document ids by similarity to query.
                            (for more info see mothod docstring).
    add_document : process given text TF's and store corresponding to document id.
    __tokenize_query : private helper method to tokenize query.

=> Functions
    -> tokenize : split text into tokent and some minimal cleaning.
    -> term_count : count term in given token list.
    -> token_count : get total amount of tokens in list.
    -> term_frequency : calculate TF.
    -> cosine_similarity : calculate cosine_similarity between two vectors.
"""
import re
from math import sqrt
from typing import Union
from modules.util import Singleton
from modules.stop_words import stopwords

# Patterns:
# Pattern to match punctuations.
punctuation = re.compile(r"([\[\"$%&\'@!#()*+,-./\\:?;<=>\[\]^_`{|}~])|([.])")
# Pattern to match words.
word_pattern = re.compile(r"\w+")


def tokenize(text: str) -> list[str]:
    """
    Split text to tokens

    Return list of word tokens for a string.
    where each string
    - is not in the stopwords
    - is lower case
    - is without panctuations
    """
    # Remove panctuations from text.
    text = re.sub(punctuation, "", text)
    # all text to lower
    text = text.lower()
    # spliting text by matching to word regex
    matches = word_pattern.finditer(text)
    tokens = []
    for match in matches:
        start = match.start()
        end = match.end()
        tokens.append(text[start:end])
    return tokens


def term_count(term: str, document_tokens: list[str]) -> int:
    """
    Return integer Term Count for a document.

    tc = count number of term occurence in document.
    """
    return document_tokens.count(term.lower())


def token_count(document_tokens: list[str]) -> int:
    """
    Return integer with total number of tokens in a document.

    toc = count number of tokens in a document.
    """
    return len(document_tokens)


def term_frequency(term: str, document_tokens: list[str]) -> float:
    """
    Return term frequency (TF), normalized for document size.

    tf = term count / token count
    """
    return term_count(term, document_tokens) / token_count(document_tokens)


def cosine_similarity(v1: list[float], v2: list[float]) -> float:
    """
    Compute cosine similarity of v1 to v2.

    Cosine similarity is cos(angle btween v1 and v2).
    which = (v1 dot v2)/(||v1||*||v2||).
    From the formula:
    v1 dot v2 = ||v1||*||v2||*cos(angle btween v1 and v2).
    """
    sumxx: float = 0
    sumxy: float = 0
    sumyy: float = 0
    for i, _ in enumerate(v1):
        x = v1[i]
        y = v2[i]
        sumxx += x * x
        sumyy += y * y
        sumxy += x * y
    if sumxx * sumyy == 0:
        return 0
    return sumxy / float(sqrt(sumxx * sumyy))


class DocumentsTermsFrequency(metaclass=Singleton):
    """
    Documents Terms Frequency Singleton.

    This class can have one instance.
    The object keep information about document's term frequency.
    for example:
        doc1: "cat fat cat"
        doc2: "fat fat cat"
        documents_term_frequency = { 'doc1':[0.333, 0.666] , 'doc1':[0.666, 0.333] }
        word_to_index = { 'fat':0 , 'cat':1 }

    DocumentsTermsFrequency methods:
        add_document - processing and adding information to object.
        order_by_similarity_to - process query and calculate similarity
        with all args.
    """

    def __init__(self) -> None:
        """Initialze two empty dictionaries."""
        self.documents_term_frequency: dict[str, list[float]] = dict()
        self.word_to_index: dict[str, int] = dict()

    def add_document(self, document_id: Union[str, int], document_text: str) -> None:
        """
        Process and store information.

        Tokenize text that calculate TF for each token.
        Store TF value of each token in list.
        Store in deictionary reference from token to its index in the list.
        All words that not in document_text initialized to 0 on their
        corresponding indexes in the TF list.
        """
        tokens: list[str] = tokenize(document_text)
        term_frequencies: list[float] = [0 for _ in range(len(self.word_to_index))]

        for token in tokens:
            if token not in self.word_to_index.keys():
                self.word_to_index[token] = len(self.word_to_index)
                term_frequencies.append(term_frequency(token, tokens))
                for dtf in self.documents_term_frequency.values():
                    dtf.append(0)
            else:
                i = self.word_to_index[token]
                term_frequencies[i] = term_frequency(token, tokens)
        self.documents_term_frequency[str(document_id)] = term_frequencies

    def __tokenize_query(self, query: str) -> list[str]:
        """
        Query tokenization helper mthod.

        Tokenize query with Tokenize function.
        From recived tokens return tokens that in know token
        aka self.word_to_index.key().
        """
        tokens = tokenize(query)
        relevant_tokens = []
        for token in tokens:
            if token in self.word_to_index.keys():
                relevant_tokens.append(token)
        return relevant_tokens

    def order_by_similarity_to(
        self, query: str, *args: Union[str, int]
    ) -> tuple[str, ...]:
        """
        Oreder document_id passed as *args by similarity to query.

        *document_id can be passed as int or as str.

        cases:
        -----
        Query is empty -> returning args in the same order.
        Query dont have known words -> returning args in the same order.
        Query is with known words but not in given document_id all somilarity is 0
            -> returning empty list.
        Query and documents have words in common
                -> return documents id sorted by similarity (higher first)
        """
        # make sure all ids are srtings
        document_ids: list[str] = [str(arg) for arg in args]

        # tokenize query
        query_tokens: list[str] = self.__tokenize_query(query)

        if not query_tokens:
            return tuple(str(arg) for arg in args)

        # create tfs lists for given tokens
        query_tf: list[float] = list()
        documents_tf: dict[str, list[float]] = {id_: list() for id_ in document_ids}
        for token in query_tokens:
            query_tf.append(term_frequency(token, query_tokens))
            for id_ in document_ids:
                documents_tf[id_].append(
                    self.documents_term_frequency[str(id_)][self.word_to_index[token]]
                )
        # create list of tuples with similarity value and document id
        pairs: list[tuple[float, str]] = list()
        for id_ in document_ids:
            pairs.append(
                (
                    cosine_similarity(query_tf, documents_tf[id_]),
                    id_,
                )
            )
        # sort by similarity
        pairs.sort(key=lambda x: x[0], reverse=True)
        return tuple(x[1] for x in pairs)
