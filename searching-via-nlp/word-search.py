import nltk

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# nltk.download('wordnet')    # lemmatization (convertion of words to their base form)
# nltk.download('punkt')      # tokenization (splitting text into words)
# nltk.download('stopwords')  # stopwords (common words that are usually removed)
# nltk.download('averaged_perceptron_tagger')  # part-of-speech tagging

user_query = """I saw a boy with a telescope.
             He was standing in the balcony.
             He had a girlfriend living in the U.S.A. and being a fan of A.I. he was attracted to astronomy."""

sentences = sent_tokenize(user_query)
print(sentences)

words = word_tokenize(user_query)
print(words)

stop_words = set(stopwords.words('english'))
print(stopwords)

stopwords_in_text = [word for word in words if word.lower() in stop_words]
print(stopwords_in_text)