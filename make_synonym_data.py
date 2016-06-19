from gensim.models import word2vec
import csv
import sys

model = word2vec.Word2Vec.load(sys.argv[1])

with open(sys.argv[2], 'r', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        neologd_vocab = frozenset(row)
        break

neologd_vocab_num = len(neologd_vocab)

with open(sys.argv[3], 'w') as f:
    hit_count = 0
    neologd_vocab_count = 0
    disp_num = neologd_vocab_num // 100
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
            f.write(output_line)
            hit_count += 1
        finally:
            neologd_vocab_count += 1
            if neologd_vocab_count % disp_num == 0:
                print('{}\t{} / {}\t{}'.format(hit_count, neologd_vocab_count, neologd_vocab_num, neologd_vocab_count / neologd_vocab_num))
            
            
