from gensim.models import word2vec
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

sentences = word2vec.Text8Corpus('middle_data/tweet_wakachi.txt')


model = word2vec.Word2Vec(sentences, size=200, min_count=5, window=5)

model.save('word2vec.model')

print('finished')
