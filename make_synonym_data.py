from gensim.models import word2vec
import csv
import sys
import logging
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--size', type=int, default=100)
parser.add_argument('-m', '--min_count', type=int, default=5)
parser.add_argument('-w', '--window', type=int, default=5)
parser.add_argument('-i', '--input', default='middle_data/jawiki_wakachi.txt')
parser.add_argument('-o', '--output', default='data/synonym_data.tsv')
parser.add_argument('-v', '--vocab', default='middle_data/neologd_vocab.csv')
args = parser.parse_args()


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

sentences = word2vec.Text8Corpus(sys.argv[1])
model = word2vec.Word2Vec(sentences, size=args.size, min_count=args.min_count, window=args.window)

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
