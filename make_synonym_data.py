from gensim.models import word2vec
import csv
import sys

model = word2vec.Word2Vec.load(sys.argv[1])

with open(sys.argv[2], 'r', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        neologd_vocab = row
        break

with open(sys.argv[3], 'w') as f:
    count = 0
    for word in neologd_vocab:
        try:
            synonyms = model.most_similar(positive=[word], negative=[], topn=5)
        except KeyError:
            continue
        else:
            output_line = word + '\t'
            for synonym in synonyms:
                output_line += synonym[0] + '\t' + str(synonym[1]) + '\t'

            output_line = output_line[:-1] + '\n'
            if count > 10:
                break
