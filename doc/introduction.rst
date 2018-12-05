Introduction
============

Summary
-------

This package takes a wordlist, then trains a model that can automatically
generate name suggestions for things like companies or software. You feed it a
text corpus with a certain theme, e.g. a Celtic text, and it then outputs
similar sounding suggestions. An example call to a trained model looks like this::

    >>> cfg = sng.Config(suffix=' Labs')
    >>> gen = sng.Generator(wordlist_file='my_wordlist.txt')
    >>> gen.fit()
    >>> gen.simulate(n=4)

    ['Ercos Software', 'Riuri Software', 'Palia Software',
     'Critim Software']

The package source is available on `GitHub <https://github.com/AlexEngelhardt/startup-name-generator>`_.

I also gave a lightning talk presenting the basic idea, it's available `on Youtube <https://www.youtube.com/watch?v=1w3Q3CEldG0>`_.


Supplied wordlists
------------------

The package comes with sample word lists in German, English, and French, and
more "exotic" corpora of Pokemon names, death metal song lyrics, and
J.R.R. Tolkien’s Black Speech, the language of Mordor. Below, I'll briefly
describe them and also show some randomly sampled output for the (totally not
cherry-picked) generated words. These corpora are available in the `wordlists
subdirectory
<https://github.com/AlexEngelhardt/startup-name-generator/tree/master/sng/wordlists>`_.


- `German <http://gutenberg.spiegel.de/buch/robinson-crusoe-747/1>`_.
  The first chapter of Robinson Crusoe in German
- `English <http://www.umich.edu/~umfandsf/other/ebooks/alice30.txt>`_.
  Alice in Wonderland
- `Greek <http://ntwords.com/eng_gr.htm>`_
  A short list of Greek words (in the latin alphabet)
- Gallic `(source 1) <http://oda.chez-alice.fr/gallicdico.htm>`_: A list of Gallic words. `(source 2) <http://www.darklyrics.com/e/eluveitie.html>`_: Selected Gallic song lyrics from the band Eluveitie
- `Latin <http://www.thelatinlibrary.com/ovid/ovid.met1.shtml>`_:
  The first book of Ovid's Metamorphoses
- `French <https://fr.wikipedia.org/wiki/France>`_:
  The French Wikipedia entry for France
- `Behemoth <http://www.darklyrics.com/b/behemoth.html>`_:
  English song lyrics by the death metal band Behemoth. Sampled words will have be more occult themed
- `The Black Speech <http://www.angelfire.com/ia/orcishnations/englishorcish.html>`_:
  JRR Tolkien's language of the Orcs
- `Lorem Ipsum <http://www.lipsum.com>`_:
  The classic lorem ipsum text
- `Pokemon <https://github.com/veekun/pokedex/blob/74e22520db7e6706d2e7ad2109f15b7e9be10a24/pokedex/data/csv/pokemon.csv>`_:
  A list of 900 Pokemon. Your company will sound like one of them, then!


Celtic
^^^^^^

My main target was a Celtic sounding name. Therefore, I first created a corpus of two parts (`browse it here <https://github.com/AlexEngelhardt/startup-name-generator/blob/master/sng/wordlists/gallic.txt>`_): first, a Gallic dictionary, and second, selected song lyrics by the swiss band `Eluveitie <http://www.darklyrics.com/e/eluveitie.html>`_. They write in the Gaulish language, which reads very pleasantly and makes for good startup names in my opinion::

    Lucia
    Reuoriosi
    Iacca
    Helvetia
    Eburo
    Ectros
    Uxopeilos
    Etacos
    Neuniamins
    Nhellos

Pokemon
^^^^^^^

I also wanted to feed the model a `list of all Pokemon <https://github.com/AlexEngelhardt/startup-name-generator/blob/master/sng/wordlists/pokemon.txt>`_, and then generate a list of new Pokemon-themed names::

    Grubbin
    Agsharon
    Oricorina
    Erskeur
    Electrode
    Ervivare
    Unfeon
    Whinx
    Onterdas
    Cagbanitl

Tolkien’s Black Speech
^^^^^^^^^^^^^^^^^^^^^^

J.R.R. Tolkien's `Black Speech <http://www.angelfire.com/ia/orcishnations/englishorcish.html>`_, the language of the Orcs, was a just-for-fun experiment (`wordlist here <https://github.com/AlexEngelhardt/startup-name-generator/blob/master/sng/wordlists/black-speech.txt>`_). It would be too outlandish for a company name, but nonetheless an interesting sounding corpus::

    Aratani
    Arau
    Ushtarak
    Ishi
    Kakok
    Ulig
    Ruga
    Arau
    Lakan
    Udaneg

Death metal lyrics
^^^^^^^^^^^^^^^^^^

As a metal fan, I also wanted to see what happens if the training data becomes song lyrics. I used lyrics by the Polish death metal band `Behemoth <http://www.darklyrics.com/b/behemoth.html>`_, because the songs are filled with occult-sounding words (`see the wordlist <https://github.com/AlexEngelhardt/startup-name-generator/blob/master/sng/wordlists/behemoth.txt>`_)::

    Artered
    Unlieling
    Undewfions
    Archon
    Unleash
    Architer
    Archaror
    Lament
    Unionih
    Lacerate

You can add anything from "Enterprises" to "Labs" as a suffix to your company name. I found a long list of possible suffixes `here <https://www.reddit.com/r/Entrepreneur/comments/4jfrgl/is_there_a_list_of_generic_company_name_endings/>`_.


Background
----------

My need for automatic company names
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Recently, an associate and I started work on founding a software development
company. The one thing we struggled most with was to come up with a good
name. It has to sound good, be memorable, and the domain should still be
available. Both of us like certain themes, e.g. words from Celtic
languages. Sadly, most actual celtic words were already in use. We'd come up
with a nice name every one or two days, only to find out that there's an
`HR company and a ski model with that exact name <https://www.google.de/search?channel=fs&q=camox>`_.

We needed a larger number of candidate names, and manual selection took too
long. I came up with an idea for a solution: Create a neural network and have it
generate new, artificial words that hopefully are not yet in use by other
companies. You'd feed it a corpus of sample words in a certain style you
like. For example, Celtic songs, or a Greek dictionary, or even a list of
Pokemon. If you train the model on the character-level text, it should pick up
the peculiarities of the text (the "language") and then be able to sample new
similar sounding words.

A famous `blog post by Andrej Karpathy <http://karpathy.github.io/2015/05/21/rnn-effectiveness/>`_ provided me with the necessary knowledge
and the confidence that this is a realistic idea. In his post, he uses recurrent
neural networks (RNNs) to generate Shakespeare text, Wikipedia articles, and
(sadly, non-functioning) source code. Thus, my goal of generating single words
should not be a big problem.
