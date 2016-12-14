from random import shuffle

#Avoid very long lines. Chunk long lines into at most 20 word lines...
def normalize_lines(line, size=20):
    words = line.split()
    for i in range(0, len(words), size):
        yield words[i:i + size]


#Read any text file, ignore blank lines and return normalized 20 word lines
def read_file(filename):
    lines = []
    with open(filename) as f:
        for line in f:
            if len(line)>1:
                line_generator = normalize_lines(line.strip("\n"))
                for l in line_generator:
                    ll = " ".join(l)
                    lines.append(ll)
    return lines

#Split the given language samples into 80% Training and 20% Testing...
def split_sample(sample, split=0.8):
    train_sample = []
    test_sample = []
    cutoff = int(len(sample) * split)
    shuffle(sample)
    train_sample = sample[:cutoff]
    test_sample = sample[cutoff:]
    return train_sample, test_sample
