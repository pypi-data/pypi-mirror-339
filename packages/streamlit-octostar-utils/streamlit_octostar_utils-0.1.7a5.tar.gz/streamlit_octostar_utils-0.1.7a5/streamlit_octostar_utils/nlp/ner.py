import re
import streamlit as st
from spacy_download import load_spacy
from flair.data import Sentence
from flair.models import SequenceTagger
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.utils import get_stop_words
import itertools
import numpy as np
import math
import nltk
from typing import Optional, List

SPACY_NER_MODELS = {
    "english": lambda: load_spacy(
        "en_core_web_sm",
        disable=["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer"],
    )
}
FLAIR_NER_MODELS = {"english": lambda: SequenceTagger.load("flair/ner-english")}
REGEX_NER_MODELS = {
    "IP_ADDRESS": [
        r"(?:(?<=:=)|(?<=\s)|(?<=\b))(?:\d{1,3}\.){3}\d{1,3}(?::\d{1,5})?(?:(?=\s)|(?=\b))",
        r"(?:(?<=:=)|(?<=\s)|(?<=\b))(?:[A-Fa-f0-9]{1,4}:){7}[A-Fa-f0-9]{1,4}(?::\d{1,5})?(?:(?=\s)|(?=\b))"
    ],
    "PHONE": r"(?:(?<=:=)|(?<=\s)|(?<=\b))[+]?[(]?[0-9]{1,4}[)]?[-\s\/0-9]*(?:(?=\s)|(?=\b))",
    "EMAIL": r"(?:(?<=:=)|(?<=\s)|(?<=\b))[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?:(?=\s)|(?=\b))",
}

BASE_TO_ONTONOTES_LABELMAP = {"PER": "PERSON"}
BASE_ALLOWED_LABELS = ["PERSON", "ORG", "LOC", "NORP", "GPE", "PRODUCT", "DATE", "TIME", "PHONE", "IP_ADDRESS", "EMAIL"]


def _sumy__get_best_sentences(sentences, rating, *args, **kwargs):
    from operator import attrgetter
    from sumy.summarizers._summarizer import SentenceInfo

    rate = rating
    if isinstance(rating, dict):
        assert not args and not kwargs
        rate = lambda s: rating[s]
    infos = (SentenceInfo(s, o, rate(s, *args, **kwargs)) for o, s in enumerate(sentences))
    infos = sorted(infos, key=attrgetter("rating"), reverse=True)
    return tuple((i.sentence, i.rating, i.order) for i in infos)


def _sumy__lsa_call(summarizer, document):
    summarizer._ensure_dependecies_installed()
    dictionary = summarizer._create_dictionary(document)
    if not dictionary:
        return ()
    matrix = summarizer._create_matrix(document, dictionary)
    matrix = summarizer._compute_term_frequency(matrix)
    from numpy.linalg import svd as singular_value_decomposition

    u, sigma, v = singular_value_decomposition(matrix, full_matrices=False)
    ranks = iter(summarizer._compute_ranks(sigma, v))
    return _sumy__get_best_sentences(document.sentences, lambda s: next(ranks))


def _sumy__luhn_call(summarizer, document):
    words = summarizer._get_significant_words(document.words)
    return _sumy__get_best_sentences(document.sentences, summarizer.rate_sentence, words)


def get_nltk_tokenizer(language: str) -> Tokenizer:
    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download("punkt")
    return Tokenizer(language)


class NERObject(object):
    def __init__(self, name, label, score, context, count, comentions):
        self.name: str = name
        self.label: str = label
        self.score: Optional[float] = score
        self.context: Optional[str] = context
        self.count: int = count
        self.comentions: Optional[List[str]] = comentions
        self.sources: Optional[List[str]] = list()

    def to_dict(self):
        data = {
            "name": self.name,
            "label": self.label,
            "score": self.score,
            "context": self.context,
            "count": self.count,
            "comentions": self.comentions or [],
        }
        if self.sources:
            data["sources"] = self.sources
        return data
            
    def __repr__(self):
        return f"NERObject(label={self.label},name={self.name})"


def postprocess_ner(entities, whitelisted_labels=None, max_entities=None):
    if whitelisted_labels is not None:
        entities = [e for e in entities if e.label in whitelisted_labels]
    entities = sorted(entities, key=lambda x: x.name)
    final_entities = []
    for _, group in itertools.groupby(entities, key=lambda x: x.name):
        group = list(group)
        best_entity = max(group, key=lambda x: x.score * x.count)
        best_entity = NERObject(
            best_entity.name,
            best_entity.label,
            best_entity.score,
            best_entity.context,
            sum([0] + [e.count for e in group]),
            list(set(itertools.chain(*[e.comentions for e in group]))),
        )
        best_entity.sources = list(set(itertools.chain(*[e.sources for e in group])))
        final_entities.append(best_entity)
    final_entities = sorted(final_entities, key=lambda x: x.score * x.count, reverse=True)
    if max_entities and len(final_entities) > max_entities:
        final_entities = final_entities[:max_entities]
    return final_entities


def compute_ner(language, sentences, spacy_model, flair_model=None, context_width=150):
    sentence_starts = [0] + [len(s[0]) + 1 for s in sentences]
    del sentence_starts[-1]
    sentence_starts = list(np.cumsum(sentence_starts))
    text = "\n".join([s[0] for s in sentences])
    min_score = 1.0
    entities = []

    # FLAIR model (if not fast)
    if flair_model:
        input = [Sentence(sentence[0]) for sentence in sentences]
        flair_model.predict(input)
        output = [e for sentence in input for e in sentence.get_spans("ner")]
        flair_entities = [
            (
                entity.text,
                BASE_TO_ONTONOTES_LABELMAP.get(
                    entity.annotation_layers["ner"][0].value,
                    entity.annotation_layers["ner"][0].value,
                ),
                entity.score,
                sentence_starts[input.index(entity[0].sentence)] + entity[0].start_position,
            )
            for entity in output
        ]
        min_score = min(min_score, *[e[2] for e in flair_entities])
        entities += flair_entities
        del flair_entities

    # REGEX model
    for label, regexes in REGEX_NER_MODELS.items():
        if not isinstance(regexes, list):
            regexes = [regexes]
        for regex in regexes:
            print(regex)
            regex_entities = [
                (match.group(), label, min_score - 0.5, match.start()) for match in re.finditer(regex, text)
            ]
            print(regex_entities)
            entities += regex_entities
            
    # SPACY model
    spacy_entities = [
        (
            entity.text,
            BASE_TO_ONTONOTES_LABELMAP.get(entity.label_, entity.label_),
            min_score - 1,
            entity.start_char,
        )
        for entity in spacy_model(text).ents
    ]
    entities += spacy_entities
    del spacy_entities

    # Reformatting for consistency
    if entities:
        min_entity_score = min([e[2] for e in entities])
        max_entity_score = max([min_entity_score] + [e[2] for e in entities])
        entity_score_range = 1 if min_entity_score == max_entity_score else (max_entity_score - min_entity_score)
        entities = [(e[0], e[1], (e[2] - min_entity_score) / entity_score_range, e[3]) for e in entities]
        scores = list(np.searchsorted(sentence_starts, [e[3] + 1 for e in entities]))
        scores = [sentences[i - 1][1] for i in scores]
        scores = [scores[i] + int(10 * entities[i][2]) for i in range(len(entities))]
        for i in range(len(entities)):
            entities[i] = (entities[i][0], entities[i][1], scores[i], entities[i][3])
        for i in range(len(entities)):
            entity = entities[i]
            count = 1
            comentions = [
                entities[j][0]
                for j in range(len(entities))
                if j != i and abs(entities[j][3] - entity[3]) < math.ceil(context_width / 2)
            ]
            entities[i] = (
                entity[0],
                entity[1],
                entity[2],
                entity[3],
                count,
                comentions,
            )
        for i in range(len(entities)):
            entity = entities[i]
            if entity[3] >= 0 and entity[3] < len(text):
                left = max(0, entity[3] - math.floor(context_width / 2))
                right = min(len(text), entity[3] + math.ceil(context_width / 2))
                context = ("[..]" if left > 0 else "") + text[left:right] + ("[..]" if right < len(text) else "")
                entities[i] = (
                    entity[0],
                    entity[1],
                    entity[2],
                    context,
                    entity[4],
                    entity[5],
                )
        entities = [NERObject(*entities[i]) for i in range(len(entities))]
    return entities


def get_extractive_summary(text, language, max_chars, fast=False, with_scores=False):
    tokenizer = get_nltk_tokenizer(language)
    stemmer = Stemmer(language)
    parser = PlaintextParser.from_string(text, tokenizer)
    if fast:
        summarizer = LuhnSummarizer(stemmer)
        summarizer.stop_words = get_stop_words(language)
        scored_sentences = iter(_sumy__luhn_call(summarizer, parser.document))
    else:
        summarizer = LsaSummarizer(stemmer)
        summarizer.stop_words = get_stop_words(language)
        scored_sentences = iter(_sumy__lsa_call(summarizer, parser.document))
    summary = []
    summary_chars = 0
    summary_chars_penultimate = 0
    while summary_chars < max_chars:
        try:
            next_sentence = next(scored_sentences)
            summary.append(next_sentence)
            summary_chars_penultimate = summary_chars
            summary_chars += len(" " + next_sentence[0]._text)
        except StopIteration:
            break
    summary = sorted(summary, key=lambda x: x[2])
    summary = [(sentence[0]._text, sentence[1]) for sentence in summary]
    if summary_chars > max_chars:
        summary[-1] = (
            summary[-1][0][: max_chars - summary_chars_penultimate],
            summary[-1][1],
        )
    if not with_scores:
        summary = " ".join([s[0] for s in summary])
    else:
        min_score = min([s[1] for s in summary]) if summary else 0
        max_score = max([min_score] + [s[1] for s in summary])
        score_range = 1 if min_score == max_score else (max_score - min_score)
        summary = [(s[0], (s[1] - min_score) / score_range) for s in summary]
    return summary


def ner_pipe(text, language, spacy_model, flair_model=None, fast=False, compression_ratio="auto"):
    if compression_ratio == "auto":
        compression_ratio = max(1.0, len(text) / 15000) if fast else 1.0
    sentences = get_extractive_summary(text, language, int(len(text) / compression_ratio), fast=fast, with_scores=True)
    ner = compute_ner(language, sentences, spacy_model, flair_model)
    return ner


def get_ner_handler(language, fast=False, compression_ratio="auto"):
    try:
        get_nltk_tokenizer(language)  # raises a LookupError if the language is not valid
    except LookupError:
        language = "english"
    spacy_model = SPACY_NER_MODELS.get(language, SPACY_NER_MODELS['english'])()
    flair_model = None if fast else FLAIR_NER_MODELS.get(language, FLAIR_NER_MODELS['english'])()
    return lambda text: ner_pipe(text, language, spacy_model, flair_model, fast, compression_ratio)


@st.cache_resource
def get_cached_ner_handler(language, fast):
    return get_ner_handler(language, fast)