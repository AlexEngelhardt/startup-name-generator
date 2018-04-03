# company-name-generator

Naming a startup is [hard](https://mashable.com/2012/10/04/startup-naming/). 

I therefore wrote a Python script to randomly generate company name ideas.

It takes an arbitrary text as input, and then trains a recurrent neural network (RNN) on each its words, learning the structure of the text. The input text can be a simple word list (e.g. Greek or Gallic), or a chapter from a book, or just a random list of words (e.g. all Pokemon). The script then generates new random names that sound simliar to the provided list.

I provided a few input texts in the `wordlists` directory - see the `README.md` there for descriptions. I also added a Jupyter Notebook here that walks you through the inner workings, if you want to experiment yourself.

You can (and maybe should) save a trained model in the `models` subdirectory, so that you don't have to train it every time you want to generate new names.

### Detailed description and tutorial

TODO blogpost

### Literature/References

- Andrew Ng's Deep Learning MOOC
- http://karpathy.github.io/2015/05/21/rnn-effectiveness/
- https://github.com/keras-team/keras/blob/master/examples/lstm_text_generation.py

### Usage

- Show a brief help:

```python
./generate.py -h
```

- Sample usage, appending a custom, fixed suffix to each name:

```python
./generate.py -n 5 -t 0.7 -m models/behemoth_500epochs.h5 wordlists/behemoth.txt --suffix Labs
```

```
Artered Labs
Unlieling Labs
Undewfions Labs
Archon Labs
Unleash Labs
```

(I found a long list of possible suffixes [here](https://www.reddit.com/r/Entrepreneur/comments/4jfrgl/is_there_a_list_of_generic_company_name_endings/))
