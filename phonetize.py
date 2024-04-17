import collections
import sys
import nltk
nltk.download('words')
from nltk.corpus import words
CMUDICT_DICT = "/content/drive/MyDrive/cmudict.dict"


# def _stream(resource_name):
#     stream = resources.open_binary("cmudict.data", resource_name)
#     return stream
    
def _stream(file_path):
    try:
        stream = open(file_path, "rb")
        return stream
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None

def dict_stream():
    """Return a readable file-like object of the cmudict.dict file."""
    stream = _stream(CMUDICT_DICT)
    return stream

pronunciations = None
lookup = None

def parse_cmu(cmufh):
    pronunciations = list()
    for line in cmufh:
        line = line.strip().decode('utf-8')
        if line.startswith(';'):
            continue
        word, phones = line.split(" ", 1)
        pronunciations.append((word.split('(', 1)[0].lower(), phones))
    return pronunciations

def init_cmu(filehandle=None):
    global pronunciations, lookup
    if pronunciations is None:
        if filehandle is None:
            filehandle = dict_stream()
        pronunciations = parse_cmu(filehandle)
        filehandle.close()
        lookup = collections.defaultdict(list)
        for word, phones in pronunciations:
            lookup[word].append(phones)

def phones_for_word(find):
    init_cmu()
    return lookup.get(find.lower(), [])

from nltk.corpus import words
english_words = set(words.words())
def is_english_word(word):
    return word.lower() in english_words

def phonetization(word):
  text = phones_for_word(word)[0]

  text = ''.join(char for char in text if char.isalpha())
  text = text.lower()
  if text.endswith('y'):
      text = text[:-1]
  return text


# <_io.BufferedReader name='/MLDS/ml/lib/python3.11/site-packages/cmudict/data/cmudict.dict'>
# <_io.BufferedReader name='cmudict.dict'>