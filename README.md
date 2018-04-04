# startup-name-generator

Naming a startup is [hard](https://mashable.com/2012/10/04/startup-naming/). 

I therefore wrote a Python script to randomly generate company name ideas.

It takes an arbitrary text as input, and then trains a recurrent neural network (RNN) on each its words, learning the structure of the text. The input text can be a simple word list (e.g. Greek or Gallic), or a chapter from a book, or just a random list of words (e.g. all Pokemon). The script then generates new random names that sound simliar to the provided list.

I provided a few input texts in the `wordlists` directory - see the `README.md` there for descriptions. I also added a Jupyter Notebook here that walks you through the inner workings, if you want to experiment yourself.

You can (and maybe should) save a trained model in the `models` subdirectory, so that you don't have to train it every time you want to generate new names.

### Detailed description and tutorial

I wrote a [blog post](http://alpha-epsilon.de/python/2018/04/04/an-lstm-based-startup-name-generator/) with a more detailed description of this project, and a few sample calls and outputs.

### Usage

- Show a brief help:

```python
./generate.py -h
```

- Sample usage, appending a custom, fixed suffix to each name:

```python
./generate.py -e 500 -n 10 -t 0.7 -s models/behemoth_500epochs.h5 wordlists/behemoth.txt --suffix Labs
```

```
Artered Labs
Unlieling Labs
Undewfions Labs
Archon Labs
Unleash Labs
Architer Labs
Archaror Labs
Lament Labs
Unionih Labs
Lacerate Labs
```

(I found a long list of possible suffixes [here](https://www.reddit.com/r/Entrepreneur/comments/4jfrgl/is_there_a_list_of_generic_company_name_endings/))

- After you stored the model (with the `-s` option), word generation is quicker when you load instead of re-compute the model:

```python
./generate.py -n 10 -t 0.7 -m models/behemoth_500epochs.h5 wordlists/behemoth.txt --suffix Labs
```

### Literature/References

- [Andrew Ng's Deep Learning MOOC](https://www.deeplearning.ai/)
- http://karpathy.github.io/2015/05/21/rnn-effectiveness/
- https://github.com/keras-team/keras/blob/master/examples/lstm_text_generation.py

### TODOs / next steps

- When using a stored model for simulation, I still need to load the wordlist in order to generate the character dictionary. The wordlist can not be changed, otherwise you'd have to retrain the model. It would be nice to store the character set (it's the `ix_to_char` dictionary in the code) along with the model.
- Since I'm not yet a Python expert, there are most likely some suboptimal ways of doing things in the code.
- I currently filter out the hyphen during preprocessing. Ideally, I should keep it if it appears within a word, and filter it if it represents something else like a bullet list item.
- It would be cool to have an option to specify that one input name should be one *line* instead of one word. Then, one could use lists of actual company names that include symbols like ampersands, whitespace, etc., and sample these as well. See [here](https://www.wordlab.com/archives/company-names-list) and [here](https://www.sec.gov/rules/other/4-460list.htm) for nice possible input lists.
