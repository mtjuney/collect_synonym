
# 第一引数 : neologd辞書のcsvファイル
# 第二引数 : 出力ファイル

import sys

words = []

with open(sys.argv[1], 'r') as f_in:
	with open(sys.argv[2], 'w') as f_out:
		for line in f_in:
			f_out.write(line.split(',')[0] + ',')
