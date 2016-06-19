from natto import MeCab
import sys
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--dicdir', default='/usr/lib/mecab/dic/mecab-ipadic-neologd')
parser.add_argument('-i', '--input', default='middle_data/wiki_data_text.txt')
parser.add_argument('-o', '--output', default='middle_data/wiki_wakachi.txt')
args = parser.parse_args()

line_num_total = sum(1 for line in open(args.input, 'r'))
disp_num = line_num_total // 100
print('line_num_total', line_num_total)

# 入力ファイル，出力ファイルを開き，MeCabを呼び出す
# dicdirは処理するサーバ用
ops={'dicdir': args.dicdir, 'node_format': '%f[6]'}
with open(args.input, 'r') as f_in, open(args.output, 'w') as f_out, MeCab(options=ops) as nm:
    line_num = 0
    escape_flag = False
    escape_count = 0
    for line in f_in:
        line_num += 1
        if line_num % disp_num == 0:
            print('{} / {} : {:.0f}%'.format(line_num, line_num_total, 100 * line_num / line_num_total))

        if line == '\n':
            continue
        elif re.match(r'^\{\{', string=line):
            escape_flag = True
            escape_count += 1
            continue
        elif escape_flag:
            if re.search(r'\}\}\n', string=line) or escape_count > 100:
                escape_flag = False
                escape_count = 0

            escape_count += 1
            continue

        line_text = re.sub(r'[\s　]+', '', line.strip())
        nodes = nm.parse(line_text, as_nodes=True)
        mors = []
        for n in nodes:
            if not n.is_eos():
                if n.feature != '':
                    mors.append(n.feature)
                else:
                    mors.append(n.surface)

        f_out.write(' '.join(mors) + '\n')

print('finished')
