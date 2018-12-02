# startup-name-generator

### Summary

This package can train a model that learns the "structure" of the words in a
supplied text corpus. It then generates new words with a similar structure,
which can be used as suggestions for naming things like companies or software.

### Quickstart

Check out the Jupyter Notebook(s) in ``doc/notebooks/``.

### Extended summary

Naming a startup is [hard](https://mashable.com/2012/10/04/startup-naming/). 

I therefore wrote a Python package to randomly generate company name ideas.

It takes an arbitrary text as input, and then trains a recurrent neural network
(RNN) on each its words, learning the structure of the text. The input text can
be a simple word list (e.g. Greek or Gallic), or a chapter from a book, or just
a random list of words (e.g. all Pokemon). The script then generates new random
names that sound simliar to the provided list.

### Literature/References

- [Andrew Ng's Deep Learning MOOC](https://www.deeplearning.ai/)
- http://karpathy.github.io/2015/05/21/rnn-effectiveness/
- https://github.com/keras-team/keras/blob/master/examples/lstm_text_generation.py
