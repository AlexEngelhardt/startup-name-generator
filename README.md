# company-name-generator

Script to randomly generate company name ideas.

Two approaches are implemented:

1. A recurrent neural network (RNN) is trained on a dictionary of words from one language (Greek and Gallic), and then generates new random names that sound simliar
2. A heuristics-based simulator that samples and concatenates syllables.

### Literature/References

- Andrew Ng's Deep Learning MOOC
- http://karpathy.github.io/2015/05/21/rnn-effectiveness/
- https://github.com/keras-team/keras/blob/master/examples/lstm_text_generation.py

### 1. Dictionary RNNs

rnn.py

### 2. Syllable Sampling

syllables.py
