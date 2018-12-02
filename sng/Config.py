"""The Config module. It defines the Config class.
"""


class Config:
    """Configuration options for model training and name generation

    Parameters
    ----------

    \**kwargs:
      Keyword arguments that will overwrite the default config options.

    Examples
    --------

    To create a Config object that results in simulating names between
    6 and 10 letters::

        cfg = sng.Config(
            min_word_len=6,
            max_word_len=10
        )

    To quickly inspect all values::

        cfg.to_dict()
    """

    def __init__(self, **kwargs):

        # ################################################################
        # Misc

        self.debug = True
        """bool: If true, methods will add some additional attributes
        to a Generator object's ``debug`` dict.
        """

        self.verbose = True
        """bool: If true, prints helpful messages on what is happening.
        """

        # ################################################################
        # Training

        self.epochs = 100
        """int: How many epochs to train the RNN for?
        """

        self.batch_size = 64
        """int: The batch size for training the RNN
        """

        self.n_layers = 2
        """int: How many LSTM layers in the model?
        """

        self.hidden_dim = 50
        """int: Number of hidden units per LSTM layer
        """

        # ################################################################
        # Simulation

        self.min_word_len = 4
        """int: How long should simulated words be at least?
        """

        self.max_word_len = 12
        """int: How long should simulated words be maximum?
        """

        self.temperature = 1.0
        """float: Sampling temperature. Lower values are "colder", i.e.
        sampling probabilities will be more conservative.
        """

        self.suffix = ''
        """str: A suffix to append to the suggested names.

        Choose e.g. " Software" (with a leading space!) to see how your
        company name would look with the word Software at the end.
        """

        # ################################################################
        # Update arbitrary attributes:
        # https://stackoverflow.com/questions/8187082
        # e.g. run cfg = Config(suffix=' Software') to keep all other
        # options dfault

        self.__dict__.update(kwargs)

    def to_dict(self):
        """Convert Config object to dictionary.
        """

        return self.__dict__
