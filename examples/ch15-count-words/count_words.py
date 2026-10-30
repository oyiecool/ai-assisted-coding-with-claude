"""The learner's word counter (Chapter 15, 15.7; Chapter 18, scenario 12)."""


def count_words_buggy(path):
    """The original: returns the word count of the LAST line only.

    `words` is overwritten on every pass of the loop, and `count` is set
    once, after the loop. A file whose last line is empty therefore always
    reports 0.
    """
    count = 0
    with open(path) as f:
        for line in f:
            words = line.split()
        count = len(words)
    return count


def count_words(path):
    """The fix the learner found by tracing the loop: add up every line."""
    count = 0
    with open(path) as f:
        for line in f:
            count += len(line.split())
    return count
