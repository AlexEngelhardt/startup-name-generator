#!/usr/bin/python3

from utils import *
import argparse
import os, sys
import numpy as np


parser = argparse.ArgumentParser(description = "A Python script that generates startup names."
                                 "It takes as input a text file containing some "
                                 "list of words, e.g. a German book chapter, a Greek dictionary, or a list of Pokemon "
                                 "(it doesn't have to be formatted, the script contains a rudimentary "
                                 "preprocessing step). The script then trains a recurrent neural network to learn "
                                 "the structure of the words, and finally outputs a list of suggestions with "
                                 "a similar structure as the words in the provided wordlist.")
parser.add_argument("wordlist",
                    help="Path to the word list, a not necessarily well-formatted .txt file. "
                    "You have to provide it even if you load a pre-trained model, because "
                    "you currently need it to compute the list of possible characters to sample from.")
parser.add_argument("-s", "--savepath",
                    help="Path to save the computed model")
parser.add_argument("-m", "--modelpath",
                    help="Don't compute a model, instead load a previously computed one from this path")
parser.add_argument("-t", "--temperature", type = float, default = 1.0,
                    help="The randomness with which to sample the words' characters. Range from zero to " 
                    "inifinity, but a value between 0.5 (conservative) and 1.5 (more random) is recommended. "
                    "Defaults to 1.0")
parser.add_argument("-n", "--nwords", type = int, default = 10,
                    help="Number of words to sample. Default 10.")
parser.add_argument("-e", "--epochs", type = int, default = 100,
                    help="Number of epochs to train the model. Default 100, but try up to 500")
parser.add_argument("-v", "--verbose",
                    help="Report more details", action = "store_true")
parser.add_argument("--suffix",
                    help="Suffix to put after the generated company name")

args = parser.parse_args()

# Don't print the many warnings
# https://github.com/h5py/h5py/issues/961
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=DeprecationWarning)
import h5py
# warnings.resetwarnings()

import keras

from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM, SimpleRNN, GRU, TimeDistributed
from keras.callbacks import LambdaCallback

# Generate a list of words (including newline)
words = text_to_words(args.wordlist)

# Generate the set of unique characters (including newline)
# https://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python
chars = sorted(list(set([char for word in words for char in word])))

VOCAB_SIZE = len(chars)
N_WORDS = len(words)  # #words in corpus - not #words to generate
MIN_WORD_LEN = 4   # minimum company name length
MAX_WORD_LEN = 12  # maximum company name length

if args.verbose:
    print(N_WORDS, "words\n")
    print("vocabulary of", len(chars), "characters, including the \\n:")
    print(chars)
    print("\nFirst two sample words:")
    print(words[0:2])

ix_to_char = {ix:char for ix, char in enumerate(chars)}
char_to_ix = {char:ix for ix, char in enumerate(chars)}

# TODO how to move this function into utils.py? If I do, execution fails because of "args.verbose not found"    
def on_epoch_end(epoch, logs):
    if epoch % 10 == 0 and args.verbose:
        print("epoch " + str(epoch) + ": ", end="")
        for _ in range(4):
            word = generate_word(model,
                                 ix_to_char = ix_to_char,
                                 temperature = 1.0,
                                 min_word_length = MIN_WORD_LEN,
                                 max_word_length = MAX_WORD_LEN)
            print(word + ", ", end="")

        print("loss: " + str(np.round(logs['loss'], 4)))


if args.modelpath != None:
    # Load one of these models if you have trained them before
    #  and want to skip re-training
    model = keras.models.load_model(args.modelpath)
else:
    X = np.zeros((N_WORDS, MAX_WORD_LEN, VOCAB_SIZE))
    Y = np.zeros((N_WORDS, MAX_WORD_LEN, VOCAB_SIZE))
    for word_i in range(N_WORDS):
        word = words[word_i]
        chars = list(word)
        word_len = len(word)
    
        for char_j in range(min(len(word), MAX_WORD_LEN)):
            char = chars[char_j]
            char_ix = char_to_ix[char]
            X[word_i, char_j, char_ix] = 1
            if char_j > 0:
                Y[word_i, char_j - 1, char_ix] = 1  # the 'next char' at time point char_j

    LAYER_NUM = 2
    HIDDEN_DIM = 50

    model = Sequential()
    model.add(LSTM(HIDDEN_DIM, input_shape=(None, VOCAB_SIZE), return_sequences=True))
    for i in range(LAYER_NUM - 1):
        model.add(LSTM(HIDDEN_DIM, return_sequences=True))
    model.add(TimeDistributed(Dense(VOCAB_SIZE)))
    model.add(Activation('softmax'))
    model.compile(loss="categorical_crossentropy", optimizer="rmsprop")

    print_callback = LambdaCallback(on_epoch_end = on_epoch_end)
    BATCH_SIZE = 64
    model.fit(X, Y, batch_size = BATCH_SIZE, verbose = 0,
              epochs = args.epochs, callbacks = [print_callback])

    if args.savepath != None:
        model.save(args.savepath)

# Print a few words with the final model:
print("\n\nOutput:\n=======\n")
for _ in range(args.nwords):
    name = generate_word(model,
                         ix_to_char = ix_to_char,
                         temperature = args.temperature,
                         min_word_length = MIN_WORD_LEN,
                         max_word_length = MAX_WORD_LEN)
    if args.suffix != None:
        name = name + " " + args.suffix
    print(name)
