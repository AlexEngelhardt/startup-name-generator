import numpy as np
import pickle

from .Config import Config
from .helpers import temp_scale

from keras.preprocessing.text import text_to_word_sequence
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM, TimeDistributed  # , SimpleRNN, GRU
from keras.callbacks import LambdaCallback


class Generator:
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
            print(self.corpus_size, " words\n")
            print(len(self.chars), "characters, including the \\n:")
            print(self.chars)
            print("\nFirst two sample words:")
            print(self.wordlist[:2])

    def fit(self):
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
                    print("epoch " + str(epoch) + ": ", end="")
                    for _ in range(4):
                        word = self.generate_word(model)
                    print(word + ", ", end="")

                    print("loss: " + str(np.round(logs['loss'], 4)))

            print_callback = LambdaCallback(on_epoch_end=on_epoch_end)
            model.fit(X, Y, batch_size=self.config.batch_size, verbose=0,
                      epochs=self.config.epochs, callbacks=[print_callback])

            self.model = model

    def simulate(self, n=10):
        words = []
        for i in range(n):
            word = self.generate_word(self.model)
            words.append(word + self.config.suffix)
        return words

    def store(self, filename):
        # TODO doesn't work. Maybe pickle the .config attribute
        # and use keras.models.load_model and model.save
        pickle.dump(self, open(filename, "wb"), pickle.HIGHEST_PROTOCOL)

    @classmethod
    def load(cls, filename):
        # TODO also doesn't work yet.
        generator = pickle.load(open(filename, "rb"))
        assert isinstance(generator, "sng.Generator.Generator"), \
            "Specified filename is not a sng.Generator object!"

        return generator

    def generate_word(self, model):

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
