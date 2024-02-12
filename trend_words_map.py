import nltk

from nltk.tokenize import word_tokenize
from nltk.corpus   import stopwords
from collections   import Counter
from langdetect    import detect
from wordcloud     import WordCloud

from resources.abbr import abbr


nltk.download('punkt')
nltk.download('stopwords')


def get_stopwords(language):
    try:
        language_full = abbr.get(language, 'english')
        return set(stopwords.words(language_full))
    except LookupError:
        return set(stopwords.words('english')) # english is default


def analyze_text(text):
    language = detect(text)
    tokens = word_tokenize(text)

    try:
        stopwords = get_stopwords(language)
    except OSError:
        stopwords = get_stopwords('en')

    if language == 'uk':
        from resources.stopwords_uk import stopwords_uk
        stopwords = stopwords_uk


    cleaned_tokens = [
        word.lower() 
        for word in tokens 
        if word.isalpha() and word.lower() not in stopwords
    ]


    word_freq = Counter(cleaned_tokens)

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)
    wordcloud.to_file("wordcloud.png")


if __name__ == "__main__":
    #if len(sys.argv) != 2:
    #    print("Використання: python script.py 'текст для аналізу'")
    #    sys.exit(1)
    from resources.test_text import text
    #input_text = sys.argv[1]
    analyze_text(text)
