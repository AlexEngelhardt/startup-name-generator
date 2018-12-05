# coding: utf-8

import os
import numpy as np
import pickle

from .Config import Config
from .helpers import temp_scale

import keras
from keras.preprocessing.text import text_to_word_sequence
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM, TimeDistributed  # , SimpleRNN, GRU
from keras.callbacks import LambdaCallback


class Generator:
    """Main class that holds the config, wordlist, and the trained model.

    Parameters
    ----------
    config : sng.Config, optional
        A Config instance specifying training and simulation parameters.
        If not supplied, a default configuration will be created.
    wordlist_file : str
        Path to a textfile holding the text corpus you want to use.
    wordlist : list of strings
        Alternatively to ``wordlist_file``, you can provide the already
        processed wordlist, a list of (ideally unique) strings.

    Attributes
    ----------
    config : sng.Config
        The Config object supplied, or a default object if none was supplied
        at initialization.
    wordlist : list of strings
        A processed list of unique words, each ending in a newline.
        This is the input to the neural network.

    Examples
    --------
    You can create a word generator like this::

        import sng
        cfg = sng.Config()

        # Folder for pre-installed wordlists:
        wordlist_folder = os.path.join(
            os.path.dirname(os.path.abspath(sng.__file__)), 'wordlists')
        sample_wordlist = os.path.join(wordlist_folder, 'latin.txt')

        # Create a Generator object with some wordlist:
        gen = sng.Generator(wordlist_file=sample_wordlist, config=cfg)

        # Train the model:
        gen.fit()

        # Get a few name suggestions:
        gen.simulate(n=5)
    """

    def __init__(self, config=Config(), wordlist_file=None, wordlist=None):
        self.config = config

        if wordlist_file:
            # text_to_word_sequence only splits by space, not newline.
            # Make all word separators spaces:
            contents = open(wordlist_file).read().replace('\n', ' ')
            wordlist = text_to_word_sequence(
                contents,
                filters='!"#$%&()*+,-./:;<=>?@[\]^_`{|}~0123456789–…\'\"’«·»'
            )

        # Keep only unique words:
        self.wordlist = list(set(wordlist))
        # Terminate each word with a newline:
        self.wordlist = [word.strip() + '\n' for word in self.wordlist]

        # Generate the set of unique characters (including newline)
        # https://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python
        self.chars = sorted(list(set(
            [char for word in self.wordlist for char in word]
        )))

        self.vocab_size = len(self.chars)
        self.corpus_size = len(self.wordlist)

        self.ix_to_char = {
            ix: char for ix, char in enumerate(self.chars)
        }
        self.char_to_ix = {
            char: ix for ix, char in enumerate(self.chars)
        }

        if self.config.verbose:
            print(self.corpus_size, "words\n")
            print(len(self.chars), "characters, including the \\n:")
            print(self.chars)
            print("\nFirst two sample words:")
            print(self.wordlist[:2])

    def fit(self):
        """Fit the model. Adds the 'model' attribute to itself.
        """

        X = np.zeros((self.corpus_size,
                      self.config.max_word_len,
                      self.vocab_size))
        Y = np.zeros((self.corpus_size,
                      self.config.max_word_len,
                      self.vocab_size))
        for word_i in range(self.corpus_size):
            word = self.wordlist[word_i]
            chars = list(word)

            for char_j in range(min(len(word), self.config.max_word_len)):
                char = chars[char_j]
                char_ix = self.char_to_ix[char]
                X[word_i, char_j, char_ix] = 1
                if char_j > 0:
                    # the 'next char' at time point char_j
                    Y[word_i, char_j - 1, char_ix] = 1

        model = Sequential()
        model.add(LSTM(self.config.hidden_dim,
                       input_shape=(None, self.vocab_size),
                       return_sequences=True))
        for i in range(self.config.n_layers - 1):
            model.add(LSTM(self.config.hidden_dim, return_sequences=True))
        model.add(TimeDistributed(Dense(self.vocab_size)))
        model.add(Activation('softmax'))
        model.compile(loss="categorical_crossentropy", optimizer="rmsprop")

        # TODO how to move this function into helpers.py?
        def on_epoch_end(epoch, logs):
            if epoch % 10 == 0 and self.config.verbose:
                print("epoch " + str(epoch) + " words: ", end="")
                for _ in range(4):
                    word = self._generate_word(model)
                    print(word + ", ", end="")

                print("loss: " + str(np.round(logs['loss'], 4)))

        print_callback = LambdaCallback(on_epoch_end=on_epoch_end)
        model.fit(X, Y, batch_size=self.config.batch_size, verbose=0,
                  epochs=self.config.epochs, callbacks=[print_callback])

        self.model = model

    def simulate(self, n=10, temperature=None, min_word_len=None,
                 max_word_len=None):
        """Use the trained model to simulate a few name suggestions.

        Parameters
        ----------

        n : int
            The number of name suggestions to simulate
        temperature : float or None
            Sampling temperature. Lower values are "colder", i.e.
            sampling probabilities will be more conservative.
            If None, will use the value specified in self.config.
        min_word_len : int or None
            Minimum word length of the simulated names.
            If None, will use the value specified in self.config.
        max_word_len : int or None
            Maximum word length of the simulated names.
            If None, will use the value specified in self.config.
        """

        temperature = temperature or self.config.temperature
        min_word_len = min_word_len or self.config.min_word_len
        max_word_len = max_word_len or self.config.max_word_len

        assert hasattr(self, 'model'), 'Call the fit() method first!'
        words = []
        for i in range(n):
            word = self._generate_word(self.model)
            words.append(word + self.config.suffix)
        return words

    def save(self, directory, overwrite=False):
        """Save the model into a folder.

        Parameters
        ----------
        directory : str
            The folder to store the generator in. Should be non-existing.
        overwrite : bool
            If True, the folder contents will be overwritten if it already
            exists. Not recommended, though.
        """

        if not overwrite:
            assert not os.path.exists(directory), 'Directory already ' + \
                'exists! Please choose a non-existing path.'

        if not os.path.exists(directory):
            os.makedirs(directory)

        pickle.dump(self.config,
                    open(os.path.join(directory, 'config.pkl'),
                         "wb"), pickle.HIGHEST_PROTOCOL)
        pickle.dump(self.wordlist,
                    open(os.path.join(directory, 'wordlist.pkl'),
                         "wb"), pickle.HIGHEST_PROTOCOL)
        self.model.save(os.path.join(directory, 'model.h5'))

    @classmethod
    def load(cls, directory):
        """Create a Generator object from a stored folder.

        Arguments
        ---------
        directory : str
            Folder where you used Generator.save() to store the contents in.
        """

        config = pickle.load(
            open(os.path.join(directory, 'config.pkl'), 'rb'))
        wordlist = pickle.load(
            open(os.path.join(directory, 'wordlist.pkl'), 'rb'))
        model = keras.models.load_model(os.path.join(directory, 'model.h5'))
        generator = cls(config=config, wordlist=wordlist)
        generator.model = model
        return generator

    def _generate_word(self, model):

        X = np.zeros((1, self.config.max_word_len, self.vocab_size))

        # sample the first character
        initial_char_distribution = temp_scale(
            model.predict(X[:, 0:1, :]).flatten(), self.config.temperature
        )

        ix = 0

        # make sure the initial character is not a newline (i.e. index 0)
        while ix == 0:
            ix = int(np.random.choice(self.vocab_size, size=1,
                                      p=initial_char_distribution))

        X[0, 0, ix] = 1

        # start with first character, then later successively append chars
        generated_word = [self.ix_to_char[ix].upper()]

        # sample all remaining characters
        for i in range(1, self.config.max_word_len):
            next_char_distribution = temp_scale(
                model.predict(X[:, 0:i, :])[:, i-1, :].flatten(),
                self.config.temperature
            )

            ix_choice = np.random.choice(
                self.vocab_size, size=1, p=next_char_distribution
            )

            ctr = 0
            while ix_choice == 0 and i < self.config.min_word_len:
                ctr += 1
                # sample again if you picked the end-of-word token too early
                ix_choice = np.random.choice(
                    self.vocab_size, size=1, p=next_char_distribution
                )
                if ctr > 1000:
                    print("caught in a near-infinite loop."
                          "You might have picked too low a temperature "
                          "and the sampler just keeps sampling \\n's")
                    break

            next_ix = int(ix_choice)
            X[0, i, next_ix] = 1
            if next_ix == 0:
                break
            generated_word.append(self.ix_to_char[next_ix])

        return ('').join(generated_word)
