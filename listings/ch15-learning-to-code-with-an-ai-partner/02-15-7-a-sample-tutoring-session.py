def count_words(path):
    count = 0
    with open(path) as f:
        for line in f:
            words = line.split()
        count = len(words)
    return count
