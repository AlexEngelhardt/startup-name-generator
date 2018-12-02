"""The helpers module. Contains a few useful functions.
"""

import numpy as np


def temp_scale(probs, temperature=1.0):
    """Scale probabilities according to some temperature.

    Temperatures lower than 1 mean "cold", i.e. more conservative sampling. A
    low temperature (< 1 and approaching 0) results in the char sampling
    approaching the argmax. A high temperature (> 1, approaching infinity)
    results in sampling from a uniform distribution)
    """

    probs = np.exp(np.log(probs) / temperature)
    probs = probs / np.sum(probs)
    return probs
