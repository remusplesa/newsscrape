from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import corpus  # to modify
from nltk.stem.snowball import SnowballStemmer
from nltk.probability import FreqDist


def process_content(text: str, no_of_sentences: int):
    words = word_tokenize(text)
    new_words = [word for word in words if word.isalnum()]
    new_content = [
        word for word in new_words if word not in stopwords.words('romanian')]
    stemmer = SnowballStemmer("romanian")
    stems = [stemmer.stem(word) for word in new_content]
    fdist = FreqDist(stems)

    sentence = text.lower().split('.')
    org_sentence = text.split('.')

    short = []
    best = []
    for pair in fdist.most_common(5):
        best.append(pair[0])

    print('best: ', best)
    for (i, s) in enumerate(sentence):
        words = s.split(' ')
        for word in words:
            if word in best:
                if s not in short and (len(short) <= no_of_sentences):
                    short.append(org_sentence[i] + '.')

    tldr = ' '.join(short)
    return tldr, best


class Tldr_content():
    def __init__(self, text, no_of_sentences):
        self.set_text(text)
        self.set_no_of_sentences(no_of_sentences)
        self.language = 'romanian'
        self.stemmer = SnowballStemmer(self.language)
        self.stopwords = corpus.stopwords.words(self.language)

    def set_text(self, text: str):
        if not text:
            raise ValueError('Should have text & text validation')
        self.text = text

    def set_no_of_sentences(self, no_of_sentences):
        if not no_of_sentences:
            raise ValueError('Should have a valid value')
        self.no_of_sentences = no_of_sentences

    def short(self):
        words = word_tokenize(self.text)
        new_words = [word for word in words if word.isalnum()]
        new_content = [
            word for word in new_words if word not in self.stopwords]
        stems = [self.stemmer.stem(word) for word in new_content]
        fdist = FreqDist(stems)

        sentence = self.text.lower().split('.')
        org_sentence = self.text.split('.')

        short = []
        best = []

        for pair in fdist.most_common(5):
            best.append(pair[0])

        print('best: ', best)
        for (i, s) in enumerate(sentence):
            words = s.split(' ')
            for word in words:
                if word in best:
                    if s not in short and (len(short) <= self.no_of_sentences):
                        short.append(org_sentence[i] + '.')

        tldr = ' '.join(short)
        return tldr, best
