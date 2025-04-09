from typing import List

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def extract_keywords(text: str, num_keywords: int = 10) -> List[str]:
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(text.lower())
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]
    freq_dist = nltk.FreqDist(filtered_words)
    return [word for word, _ in freq_dist.most_common(num_keywords)]
