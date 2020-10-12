import os
from keras.preprocessing.text import text_to_word_sequence


def show_builtin_wordlists():
    """Returns a list of all builtin wordlists' filenames.

    Use one of them as an argument to :func:`load_builtin_wordlist`
    and get back a ready-to-go wordlist.
    """
    return [x for x in
            os.listdir(os.path.join(os.path.dirname(__file__), "wordlists"))
            if x.endswith('.txt')]


def load_builtin_wordlist(name):
    """Load and process one of the wordlists that ship with the sng package.

    Arguments
    ---------
    name : str
        A file name of one of the files in the wordlists/ directory.
        Call :func:`show_builtin_wordlists` to see a list of available
        names. Choose one of these.

    Returns
    -------
    list : a list of strings
        A wordlist. Literally, a list of words in the text corpus.
        It's not yet preprocessed, so there are still duplicates etc. in there.
        This is taken care of by :class:`sng.Generator`'s ``__init__`` method.
    """

    path = os.path.join(os.path.dirname(__file__), "wordlists")
    wordlist_file = os.path.join(path, name)
    if os.path.isfile(wordlist_file):
        contents = open(wordlist_file).read().replace('\n', ' ')
        wordlist = text_to_word_sequence(
            contents,
            filters='!"#$%&()*+,-./:;<=>?@[\]^_`{|}~0123456789–…\'\"’«·»'
        )
        return wordlist
    else:
        raise FileNotFoundError('Could not find the file ' + wordlist_file)
