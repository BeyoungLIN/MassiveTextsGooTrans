# file="cnn.txt"


def seq_gen(fp, sep_len=2000):
    with open(fp, 'r', encoding='utf8') as f:
        words = 0
        seq = []
        for l in f:
            # print(len(l),l)

            if len(l) > sep_len:
                raise Exception('too long line')

            words += len(l)
            if words > sep_len:
                words = len(l)
                yield ''.join(seq)
                seq.clear()
            seq.append(l)
        yield ''.join(seq)

# for s in seq_gen(file):
#     print(s)
#     print(len(s))
#     print()
