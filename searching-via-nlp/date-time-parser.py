import re

import spacy
import dateparser

nlp = spacy.load("en_core_web_sm")


def preprocess_text(text) -> str:
    """
    Pre processes text such that spaCy can fetch Date Entities from NLP
    """

    """Convert 'last to last week' -> '2 weeks ago' (and similar patterns)"""
    replacements = {
        r'\blast to last week\b': '2 weeks ago',
        r'\bweek before last\b': '2 weeks ago',
        r'\blast to last month\b': '2 months ago',
        r'\bmonth before last\b': '2 months ago',
        r'\bprevious month\b': '1 month ago',
        r'\bprevious week\b': '1 week ago',
        r'\bprevious year\b': '1 year ago',
    }

    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    return text


def spacy_date_extraction(text) -> list[str]:
    processed_text = preprocess_text(text)
    doc = nlp(processed_text)
    # dates = [token.text for token in doc if token.ent_type_ == "DATE"]
    # Extract full date expressions
    dates = [ent.text for ent in doc.ents if ent.label_ == "DATE"]
    return dates


def extract_dates(text):
    parser_compliant_text = spacy_date_extraction(text)
    print(f"spaCy Extracted: {parser_compliant_text}")
    for parsed_text in parser_compliant_text:
        parsed_date = dateparser.parse(parsed_text, settings={"PREFER_DATES_FROM": "past"})
        print(parsed_date)


# Testing different phrases
queries = [
    "I met a girl last month then took her on a date last week and am going for a movie today",
    "Movies released previous month",
    "I went to play cricket last to last week",
    "Last year, we went to New York",
    "I met with an accident somewhere between March and September of 23",
    "Show me photos taken during April 2020 or May 2021",
]

for query in queries:
    print(f"Original: {query}")
    # print(f"Extracted: {extract_dates(query)}")
    extract_dates(query)
    print("-"*50)
    # print(f"Parsed Date: {extract_time_information(query)}\n")
