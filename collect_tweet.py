import yaml
import json
import time
import re
import multiprocessing
import threading
from requests.exceptions import ConnectionError, ReadTimeout, SSLError
from requests_oauthlib import OAuth1Session
from datetime import datetime
import time
import os
import sys
from six.moves import queue

from natto import MeCab


with open('keys_twitter.yml', 'r') as f:
    keys_twitter = yaml.load(f)


tweet_q = queue.Queue(maxsize=100)
count_tweet = 0
count_word = 0

def feed_tweet():
    global keys_twitter, tweet_q

    api = OAuth1Session(
        keys_twitter['CONSUMER_KEY'],
        client_secret=keys_twitter['CONSUMER_SECRET'],
        resource_owner_key=keys_twitter['ACCESS_TOKEN'],
        resource_owner_secret=keys_twitter['ACCESS_SECRET']
    )

    url = 'https://stream.twitter.com/1.1/statuses/sample.json'
    params = {}
    res = api.get(url, params=params, stream=True)
    try:
        for r in res.iter_lines():
            if not r:
                continue
            data = json.loads(r.decode())
            if 'delete' in data.keys() or 'lang' not in data:
                pass
            elif data['lang'] != 'ja':
                pass
            elif re.match(r'^RT', data['text']):
                pass
            else:
                tweet = data['text']
                if not tweet_q.full():
                    tweet_q.put(tweet)

    except Exception as e:
        print( '=== エラー内容 ===')
        print( 'type:' + str(type(e)))
        print( 'args:' + str(e.args))
        print( 'message:' + str(e.message))
        print( 'e self:' + str(e))

    except:
        print( "error.")


def wakachigaki():
    global tweet_q, count_tweet, count_word

    ops={'dicdir': '/usr/local/lib/mecab/dic/mecab-ipadic-neologd',
       'node_format': '%f[6]'}
    with open(sys.argv[1], 'a') as f:
        with MeCab(options=ops) as nm:
            while True:
                tweet = tweet_q.get()
                # 前処理
                # @ユーザ，URL，ハッシュタグ，空白改行を削除
                tweet = re.sub(r'@[A-Za-z0-9_]+', '', tweet)
                tweet = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+', '', tweet)
                tweet = re.sub(r'[#＃][Ａ-Ｚａ-ｚA-Za-z一-鿆0-9０-９ぁ-ヶｦ-ﾟー]+[\s$]+', '', tweet)
                tweet = re.sub(r'[\s　]+', '', tweet)

                nodes = nm.parse(tweet, as_nodes=True)
                tweet_mors = []
                for n in nodes:
                    if not n.is_eos():
                        if n.feature != '':
                            tweet_mors.append(n.feature)
                        else:
                            tweet_mors.append(n.surface)

                f.write(' '.join(tweet_mors) + '\n')
                count_tweet += 1
                count_word += len(tweet_mors)


def log_output():
    global count_tweet, count_word
    while True:
        message = "{}\t{}\t{}".format(datetime.now().strftime('%H:%M:%S'), count_tweet, count_word)
        print(message)
        time.sleep(30)

if __name__ == '__main__':
    feeder = threading.Thread(target=feed_tweet)
    feeder.daemon = True
    feeder.start()

    wakacher = threading.Thread(target=wakachigaki)
    wakacher.daemon = True
    wakacher.start()

    log_output()
    feeder.join()
    wakacher.join()
