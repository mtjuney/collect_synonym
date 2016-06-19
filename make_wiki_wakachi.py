from natto import MeCab
import sys

line_num_total = sum(1 for line in open(sys.argv[1], 'r'))
disp_num = line_num_total // 100
print('line_num_total', line_num_total)

# 入力ファイル，出力ファイルを開き，MeCabを呼び出す
# dicdirは処理するサーバ用
ops={'dicdir': '/usr/lib/mecab/dic/mecab-ipadic-neologd', 'node_format': '%f[6]'}
with open(sys.argv[1], 'r') as f_in, open(sys.argv[2], 'w') as f_out, MeCab(options=ops) as nm:
    for line in f_in:
        line_num += 1
        if line_num % disp_num == 0:
            print('{} / {} : {:.1f}%'.format(line_num, line_num_total, 100 * line_num / line_num_total))

        if line == '\n':
            continue
        line_text = re.sub(r'[\s　]+', '', line.strip())
        nodes = nm.parse(line_text, as_nodes=True)
        mors = []
        for n in nodes:
            if not n.is_eos():
                if n.feature != '':
                    tweet_mors.append(n.feature)
                else:
                    tweet_mors.append(n.surface)

        f_out.write(' '.join(tweet_mors) + '\n')

print('finished')
