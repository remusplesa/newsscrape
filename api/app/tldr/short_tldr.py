from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import corpus  # to modify
from nltk.stem.snowball import SnowballStemmer
from nltk.probability import FreqDist
import re


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
        def calc_score(best_words, sentence, index):
            sentence = sentence.replace('.', '').replace('\n', '')
            stemmer = SnowballStemmer(self.language)

            score = 0

            sentence_words = sentence.split(' ')
            stemmed_words = [
                stemmer.stem(word)
                for word in sentence_words
            ]
            for word in best_words:
                if word in stemmed_words:
                    score += 1
            return [index, sentence, score]

        def Sort(list_to_sort, reverse, pos):
            list_to_sort.sort(key=lambda x: x[pos], reverse=reverse)
            return list_to_sort

        sentences = re.split(
            r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s',
            self.text
        )
        words = [
            word.lower()
            for word in word_tokenize(self.text)
            if word.isalnum()
        ]
        ro_stopwords = stopwords.words(self.language)
        ro_stopwords.append('și')
        words_wo_stop = [
            word
            for word in words
            if word not in ro_stopwords
        ]
        stemmer = SnowballStemmer(self.language)

        stems = [
            stemmer.stem(word)
            for word in words_wo_stop
        ]
        freq = FreqDist(stems)
        best = []
        for pair in freq.most_common(5):
            best.append(pair[0])

        res = []
        index = 0
        for s in sentences:
            res.append(calc_score(best, s, index))
            index += 1

        top = Sort(res, 1, 2)
        out = Sort(top[:self.no_of_sentences], 0, 0)
        short = []
        for sentence in out:
            short.append(sentence[1])

        final_short = '. '.join(short)
        return final_short, best
