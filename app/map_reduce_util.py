import string

from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict

import requests

def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # check for HTTP errors
        return response.text
    except requests.RequestException as e:
        return None

# remove punctuation
def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))

def map_function(word):
    return word, 1

def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)

# Process MapReduce
def map_reduce(text, search_words=None):
    # removal of punctuation
    text = remove_punctuation(text)
    words = text.split()

    # filter by search_words
    if search_words:
        words = [word for word in words if word in search_words]

    # Parallel Map
    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    # Shuffle
    shuffled_values = shuffle_function(mapped_values)

    # parallel Reduce
    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    return dict(reduced_values)

