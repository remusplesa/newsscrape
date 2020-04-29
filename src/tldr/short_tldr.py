from bs4 import BeautifulSoup
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.probability import FreqDist

def process_content(text: str, no_of_sentences: int):
    words = word_tokenize(text)
    new_words= [word for word in words if word.isalnum()]
    new_content= [word for word in new_words if word not in stopwords.words('romanian')]
    stemmer = SnowballStemmer("romanian")
    stems = [stemmer.stem(word) for word in new_content]
    fdist = FreqDist(stems)

    sentence = text.lower().split('.')
    org_sentence = text.split('.')

    short = []
    best= []
    for pair in fdist.most_common(5):
        best.append(pair[0])
        
    print('best: ',best)
    for (i,s) in enumerate(sentence):
        words = s.split(' ')
        for word in words:
            if word in best:
                if s not in short and len(short) <= no_of_sentences:
                    short.append(org_sentence[i]+'.')
                    
    tldr=' '.join(short)
    return tldr
