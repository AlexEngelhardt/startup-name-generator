import numpy as np


def text_to_words(textfile):
    from keras.preprocessing.text import text_to_word_sequence

    filters = '!"#$%&()*+,-./:;<=>?@[\]^_`{|}~0123456789–…\'\"’«·»'
    words = [text_to_word_sequence(x.lower().strip(), filters=filters)
             for x in open(textfile)]

    all_words = [word for line in words for word in line]

    unique_words = list(set(all_words))

    # finally, append a newline as end-of-word token to each word:
    unique_words = [word + "\n" for word in unique_words]

    return unique_words


def temp_scale(probs, temperature=1.0):
    # a low temperature (< 1 and approaching 0) results in the char sampling
    # approaching the argmax.  a high temperature (> 1, approaching infinity)
    # results in sampling from a uniform distribution)
    probs = np.exp(np.log(probs) / temperature)
    probs = probs / np.sum(probs)
    return probs


def generate_word(model, ix_to_char, temperature=1.0, min_word_length=4,
                  max_word_length=12):

    VOCAB_SIZE = model.get_config()[0]['config']['batch_input_shape'][2]

    X = np.zeros((1, max_word_length, VOCAB_SIZE))

    # sample the first character
    initial_char_distribution = temp_scale(
        model.predict(X[:, 0:1, :]).flatten(),
        temperature
    )

    ix = 0

    # make sure the initial character is not a newline (i.e. index 0):
    while ix == 0:
        ix = int(
            np.random.choice(VOCAB_SIZE, size=1, p=initial_char_distribution)
        )

    X[0, 0, ix] = 1

    # start with first character, then later successively append chars:
    generated_word = [ix_to_char[ix].upper()]

    # sample all remaining characters
    for i in range(1, max_word_length):
        next_char_distribution = temp_scale(
            model.predict(X[:, 0:i, :])[:, i-1, :].flatten(),
            temperature
        )

        ix_choice = np.random.choice(
            VOCAB_SIZE,
            size=1,
            p=next_char_distribution
        )

        # corresponds to sampling with a very low temperature:
        # ix_choice = np.argmax(next_char_distribution)

        ctr = 0
        while ix_choice == 0 and i < min_word_length:
            ctr += 1
            # sample again if you picked the end-of-word token too early
            ix_choice = np.random.choice(
                VOCAB_SIZE,
                size=1,
                p=next_char_distribution
            )
            if ctr > 1000:
                print("caught in a near-infinite loop. You might have "
                      "picked too low a temperature "
                      "and the sampler just keeps sampling \\n's")
                break

        next_ix = int(ix_choice)
        X[0, i, next_ix] = 1
        if next_ix == 0:
            break
        generated_word.append(ix_to_char[next_ix])

    return ('').join(generated_word)
