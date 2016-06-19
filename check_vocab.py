import csv
import sys

with open(sys.argv[1], 'r', newline='') as f:
    reader = csv.reader(f)

    for row in reader:
        words = row
        break

print('words length : {}'.format(len(words)))
print('words : {}'.format(words[:10]))

tweet_num = sum(1 for line in open(sys.argv[2], 'r'))

count = 0
false_count = 0
tweet_count = 0
test_flag = True
with open(sys.argv[2], 'r') as f:
    for line in f:
        tweet_count += 1
        if tweet_count % 100:
            print('tweet : {} / {}'.format(tweet_count, tweet_num))
        for line_splited in line.strip().split(' '):
            # for word in words:
            #     if line_splited == word:
            #         count += 1
            #         if count % 100 == 0 or test_flag:
            #             print(count)
            #             if count >= 10:
            #                 test_flag = False
            #         words.remove(word)
            #     else:
            #         false_count += 1

            try:
                words.remove(line_splited)
            except Exception as e:
                false_count += 1
            else:
                count += 1
                if count % 100 == 0 or test_flag:
                    print(count)
                    if count >= 10:
                        test_flag = False

print('tweet_count : {}'.format(tweet_count))
print('count : {}'.format(count))
print('false_count : {}'.format(false_count))
