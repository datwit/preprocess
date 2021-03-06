#!/usr/bin/env python 3.6

"""
Shallow parsing techniques for NLP text
=========================================

Techniques to transform text into informed strings not just the senteces.

Text are less complex if:
- stopwords are eliminated or not
- capital letters are deleted or not
- multiword are trated as is
- TODO: end this list

This module concentrate the majority of shallow parsing techniques identified
in Paraphrase Detection papers.

"""

__author__ = 'Abel Meneses-Abad'

from configparser import ConfigParser
import preprocess
from os.path import join, relpath
from preprocess.shallow import LANGUAGES
from string import punctuation

#TODO verify what happen if nltk there is not.
try:
    from nltk.corpus import stopwords
    from nltk.tag import StanfordPOSTagger
    from nltk.stem import SnowballStemmer
    from nltk.stem import WordNetLemmatizer
except:
    pass

config = ConfigParser()
config.read(preprocess.__path__[0]+'/data/cfg/stanford.cfg')
stanford_pos_model = {}

st4_pos_dir = relpath(config['POS']['stanford_dir'])
stanford_pos_model['en'] = relpath(join(st4_pos_dir,config['POS']['stanford_eng_model']))
stanford_pos_jar = relpath(join(st4_pos_dir,config['POS']['stanford_jar']))

def pos(text, lang='en', interface='stanford', multioutput='raw_value'):
    """Part of Speech Tagging.

    Parameters
    ----------
    text: string to parse, generally a sentence.

    lang: natural languaje of the text.

    interface: a tag of one of the implemented interfaces in preprocess.

    multioutput: Format type of the output.
                 string in ['raw_value', 'tuple_list', 'raw_tag']
                 * raw value - string format
                 * tuple list - format is implemented for ngram generalization of
                 some token distances in textsim papckage.
                 * raw tag - string only with POS tags

    Returns
    -------

    parsed result : string output, list of tuples [(token, POS tag)],
                    POS-tags substituting tokens.

    Note
    ----

    The returned string structure is build to use textsim string and token
    distances.

    """

    if interface == 'stanford':
        result = __stanford_pos(text, lang, multioutput)
    if interface == 'freeling':
        result = ''

    return result

def __stanford_pos(text,lang='en',multioutput='raw_value'):
    """Interface for NLTK Stanford POS Tagger interface.
    """
    st = StanfordPOSTagger(model_filename=stanford_pos_model[lang], path_to_jar=stanford_pos_jar)
    tuple_list = st.tag(text.split())
    string = ''
    raw_tag = ''
    for (word,tag) in tuple_list:
        string += word+'/'+tag+' '
        raw_tag += tag+' '

    if isinstance(multioutput, str):
        if multioutput == 'raw_value':
            return string
        if multioutput == 'tuple_list':
            return tuple_list
        if multioutput == 'raw_tag':
            return raw_tag

def remove_stopwords(text, lang='en', stops_path='', ignore_case = True):
    """Remove stopwords based on language.

    :Software: Based on Normalizr package remove_stop_words.
    """
    new_text = ''
    if stops_path:
        stop_words = set(open(stops_path+'/'+lang+'txt').read().split())
    else:
        stop_words = set(stopwords.words(lang))
    for char in punctuation:
        stop_words.add(char)

    for word in text.split(' '):
        if word.lower() not in stop_words and len(word)>3:
            if ignore_case:
                new_text += ' ' + word
            else:
                new_text += ' ' + word.lower()
    return new_text
    

def stemming(text, lang='en'):
    """Stem words based in Snowball algorithm.
    """
    stemmer = SnowballStemmer(LANGUAGES[lang])
    return ' '.join(stemmer.stem(word) for word in text.split())

POS_LIST = {
    'ADJ':'a',
    'ADJ_SAT':'s',
    'ADV':'r',
    'NOUN':'n',
    'VERB':'v',
}

def lemmatization(text, lang='en', input_type='raw_value'):
    """Lemmatize words based on WordNet corpus.
    """
    lemmatizer = WordNetLemmatizer()
    if input_type == 'raw_value':
        return  ' '.join(lemmatizer.lemmatize(word) for word in text.split())
    elif input_type == 'tuple_list':
        new_text = ''
        for word,POS in text:
            if POS in POS_LIST:
                new_text += lemmatizer.lemmatize(word,POS_LIST[POS])+' '
            else:
                new_text += word + ' '
        return  new_text

#TODO Search the spacy not installed Warning to see how to program a missing installed library

if __name__ == '__main__':
    s1=input("Input text A:")
    print("The inputed text can be lexicalized '%s'" % pos(s1))
