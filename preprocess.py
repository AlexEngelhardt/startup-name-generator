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
