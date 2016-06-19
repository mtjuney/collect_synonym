
# 第一引数 : neologd辞書のcsvファイル
# 第二引数 : 出力ファイル

import sys

words = []

with open(sys.argv[1], 'r') as f_in:
	for line in f_in:
		words.append(line.split(',')[0])

vocab = frozenset(words)
print('word num : ', len(words))
print('vocab num : ', len(vocab))

with open(sys.argv[2], 'w') as f_out:
	f_out.write(','.join(vocab))
