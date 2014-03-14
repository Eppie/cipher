import string
import operator
import itertools
import os
import re

tab = string.maketrans(string.ascii_lowercase + string.ascii_uppercase, string.ascii_lowercase * 2)
text = ""
i = 0
for root, dirs, files in os.walk('D:\projects\cipher\OANC'):
    for file in files:
        if file.endswith(".txt"):
            text = text + open(os.path.join(root, file)).read()

non_alpha = re.compile(r'[^a-zA-Z ]+')  # remove all non "a-z" and space characters, keeps both upper and lower case
text = non_alpha.sub('', text).replace('  ', ' ')  # get rid of double spaces
print 'done reading files'


def ngram(inputstring, nlen):
    if nlen < 1:
        raise ValueError('Makes no sense to have a 0 length n-gram.')

    if len(inputstring) < 1:
        raise ValueError('The inputstring has to be longer than 1 char')

    inputstring = string.translate(inputstring, tab)
    ngram_list = [inputstring[x:x+nlen] for x in xrange(len(inputstring)-nlen+1)]
    ngram_freq = {}
    total = 0
    for n in ngram_list:
        if n in ngram_freq:
            ngram_freq[n] += 1
        else:
            ngram_freq[n] = 1
        total += 1
    total = float(total)
    return {k: (ngram_freq[k] / total * 100) for k in ngram_freq.keys()}

temp = ngram(text, 4)
f = open('output.txt', 'w')
f.write(str(temp))
f.close()
