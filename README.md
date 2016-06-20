# NEologdのメタデータ収集

## NEologd辞書内の単語の類義語を収集する

1. neologdの辞書データを解凍し，`neologd_data/`内に置く．
1. wikipediaのダンプデータ(`jawiki-latest-pages-article.xml.bz2`もしくはその軽量版)を`wiki_data/`内に置く．
1. `python make_neologd_vocab.py`を実行する．第一引数には入力データ(neologdの辞書データ.csv)，第二引数には`middle_data/neologd_vocab.csv`を指定する．
1. `middle_data/`の中に`wiki_data_text/`を作成．
1. `wp2txt -i jawiki-latest-pages-articles.xml.bz2 -o middle_data/wiki_data_text/ --no-list --no-heading --no-title --no-marker`を実行．`-i`オプションはwikipediaのダンプデータを指定すること．
1. `cat middle_data/wiki_data_text/* > middle_data/wiki_data_text.txt`を実行する．
1. `python make_wiki_wakachi.py -i middle_data/wiki_data_text.txt -o middle_data/wiki_wakachi.txt`を実行する．
1. `python make_synonym_data.py -i middle_data/wiki_wakachi.txt -o data/synonym_data.
tsv -v middle_data/neologd_vocab.csv`を実行する．`-s, --size`オプションで単語ベクトルの出力次元を，`-m, --min_count`で単語を語彙に加える最低限の出現回数を，`-w, --window`で周辺分布を見る窓の大きさを指定できる．デフォルトは`size=100, min_count=5, window=5`．
