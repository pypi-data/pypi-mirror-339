import spacy
from spacy.tokens import Span
from spacy.util import is_package
from spacy.cli.download import download as spacy_download
from typing import List
import re
# local imports
from .execute import ModelRunner
from .utils import extract_literals, restore_literals
from .log import logger

MODEL_NAME = "en_core_web_sm"


def load_spacy_model(name: str = MODEL_NAME):
    if not is_package(name):
        logger.info(f"Downloading spaCy model '{name}'...")
        spacy_download(name)

    return spacy.load(name)


# Load the English language model once
_nlp = load_spacy_model("en_core_web_sm")

# load our ONNX model that can compress stuff
compressor = ModelRunner()

# POS tags we want to keep
MEANINGFUL_POS = {"NOUN", "VERB", "PRON", "PROPN", "ADJ", "ADV", "NUM"}


def simplify_span(span: Span) -> str:
    """
    Simplify text into what we need in order to maintain gramatical sense.
    """
    spans_to_keep = []
    for token in span:
        # throw out non-meaningful tokens
        if token.pos_ in MEANINGFUL_POS:
            spans_to_keep.append(token)
    # combine into a single string
    final = " ".join(token.text for token in spans_to_keep)
    # throw out things that are just whitespace or punctuation
    final = re.sub(r"\s+", " ", final)
    final = re.sub(r"[^\w\s]", "", final)
    final = re.sub(r"\s+", " ", final)
    final = final.strip()

    return final


def split_into_segments(text: str) -> List[Span]:
    """
    Splits text into segments, treating LITERAL_{n} placeholders as their own spans.
    Returns a list of spaCy Span objects.
    """
    # convert the text into a spaCy NLP document
    doc = _nlp(text)
    # segments aren't quite sentences but they're pretty close. there are potentially
    # special cases where we want to break up something that spaCy deems a sentence.
    # for example, a <literal> tag block.
    segments = []

    # go through each spaCy sentence and split it into segements. most important thing
    # here is that we are extracting special cases such as <literal> blocks. potentially
    # other things in the future.
    for sent in doc.sents:
        # get rid of preceeding/trailing whitespace
        sent_text = sent.text.strip()
        # don't keep empty blocks. this confuses downstream processing
        if not sent_text:
            continue

        # for now, we're just looking for LITERAL_{n}s. in the future, this could be
        # other things too.
        matches = list(re.finditer(r"LITERAL_\d+", sent_text))

        # if we didn't find anything special, just keep the original text
        if not matches:
            segments.append(sent)
        else:
            # if we did, then we're going to turn this into a special type of segment. we'll
            # also process the tags.
            # TODO: this should be its own XML DSL so we have things such as <STENO_LITERAL>,
            # <STENO_RAG>, <STENO_QA_PAIR>, etc.
            last_char = sent.start_char
            for match in matches:
                match_start = sent.start_char + match.start()
                match_end = sent.start_char + match.end()

                # Add pre-literal span
                if match_start > last_char:
                    span = doc.char_span(
                        last_char, match_start, alignment_mode="expand")
                    if span:
                        segments.append(span)

                # Add literal span
                literal_span = doc.char_span(
                    match_start, match_end, alignment_mode="expand")
                if literal_span:
                    segments.append(literal_span)

                last_char = match_end

            # Add post-literal span
            if last_char < sent.end_char:
                span = doc.char_span(
                    last_char, sent.end_char, alignment_mode="expand")
                if span:
                    segments.append(span)

    return segments


def compress_text(text: str) -> str:
    """
    Compresses the text by simplifying each sentence.
    """
    # Pull out literal blocks and store them in a dict. after we process
    # the rest of the text, we'll put these back into the text unchanged.
    text_with_placeholders, literal_map = extract_literals(text)

    # Process only the parts outside <literal>
    segments = split_into_segments(text_with_placeholders)
    compressed_texts = []
    for segment in segments:
        # skip literal blocks
        if segment.text.startswith("LITERAL_"):
            compressed_texts.append(segment.text)
            continue

        # does some fast, basic processing. such as removing filler words
        simplified_text = simplify_span(segment)
        # skip empty sentences
        if not simplified_text.strip():
            continue

        # compress the input using the model
        compressed_text = compressor.run(simplified_text)
        logger.debug(f"Original: {segment.text}")
        logger.debug(f"Sanitized: {simplified_text}")
        logger.debug(f"Compressed: {compressed_text}")
        compressed_texts.append(compressed_text)
    # combine back into a single string
    joined = " ".join(compressed_texts)

    # restore the literal content to the original
    final = restore_literals(joined, literal_map)
    return final
