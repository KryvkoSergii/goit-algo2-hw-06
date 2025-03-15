import argparse
from map_reduce_util import get_text, map_reduce
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description="Words counter")
parser.add_argument("-u", "--url", help="URL to get the text",
                    default="https://gutenberg.net.au/ebooks01/0100021.txt")
parser.add_argument("-w", "--words", help="Search words",
                    default=None, nargs="*")
args = parser.parse_args()

def visualize(words):
    top_words, frequency = zip(*words[::-1])

    plt.barh(top_words, frequency)
    plt.xlabel("Frequency")
    plt.ylabel("Words")
    plt.title("Top 10 Most Frequent Words")
    plt.show()

text = get_text(args.url)
if text:
    search_words = args.words if args.words else None
    result = map_reduce(text, search_words)
    sorted_words = sorted(result.items(), key=lambda entry: entry[1], reverse=True)
    visualize(sorted_words[:10])