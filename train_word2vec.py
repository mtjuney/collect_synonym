from gensim.models import word2vec
import logging
import sys

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

sentences = word2vec.Text8Corpus(sys.argv[1])

model = word2vec.Word2Vec(sentences, size=100, min_count=3, window=5)
model.save(sys.argv[2])


print('finished')
