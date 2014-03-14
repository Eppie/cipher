# This Python file uses the following encoding: utf-8
import string
import operator
import itertools
import re
import cProfile

table = string.maketrans(string.ascii_lowercase + string.ascii_uppercase, string.ascii_lowercase * 2)
alphabet = string.ascii_lowercase

freqs = eval(open('freqs.txt', 'r').read())
freqsNoSpace = eval(open('freqsNoSpace.txt', 'r').read())
diFreqs = eval(open('diFreqs.txt', 'r').read())
triFreqs = eval(open('triFreqs.txt', 'r').read())
patterns = eval(open('patterns_small.txt', 'r').read())

allFreqs = [freqs, diFreqs, triFreqs]
nonAlpha = re.compile(r'[^a-z]+')
numberedLetters = {k: v for k, v in zip(alphabet, range(0, 26))}

vigenerePlain = 'In the Western experience with evil, we choose repeatedly to put our faith in law and the legal culture to redeem ourselves from sin.'
vigenereCipher = 'Jr ulf Afwuisr fbqismfrdi xmul fzjp, xi dlpsti siqibxfhmc us qyu svv gejxi mo pba bre xii mihem gvpuysi us sieifq pyswfpwit jssn wjr.'
cipherText = 'GJGEVVRNRHFYFRURUGFAEFRAHYRERNRUJGUOAHNLIR'
caesarText = 'LZAKAKSLWKL'
string1 = 'Now is the time for all good men to come to the aid of their country.'
string2 = 'The quick brown fox jumps over the lazy dog.'


def ngram(inputstring, nlen):
    if nlen < 1:
        raise ValueError('Makes no sense to have a 0 length n-gram.')

    if len(inputstring) < 1:
        raise ValueError('The inputstring has to be longer than 1 char')

    inputstring = string.translate(inputstring, table)
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
    return {k: (ngram_freq[k] / total * 100) for k in ngram_freq}


def freqDiff(testFreqs, n):
    total = 0

    for k in testFreqs:
        try:
            total = total + abs(allFreqs[n - 1][k] - testFreqs[k])
        except KeyError:
            total = total + testFreqs[k]
    return total


def caesar(cipher, shift, reverse=False):
    cipher = cipher.lower()
    if reverse:
        cipher = cipher[::-1]
    return cipher.translate(string.maketrans(alphabet, alphabet[shift:] + alphabet[:shift]))


def vigenere(key, message, mode):
    '''Make sure the key is in all lower case
    '''
    translated = []
    keyIndex = 0
    for symbol in message:
        try:
            num = numberedLetters[symbol]
        except KeyError:
            num = -1
        if num != -1:
            if mode == 'encrypt':
                num += numberedLetters[key[keyIndex]]
            elif mode == 'decrypt':
                num -= numberedLetters[key[keyIndex]]

            num %= 26
            translated.append(alphabet[num])

            keyIndex += 1
            if keyIndex == len(key):
                keyIndex = 0
        else:
            translated.append(symbol)
    return ''.join(translated)


def divide(string, n):
    result = ""
    n = len(string) / n
    string = [string[i:i+n] for i in range(0, len(string), n)]
    for i in range(len(string[0])):
        for j in string:
            try:
                result = result + j[i]
            except:
                pass
    return result


def pattern(word):
    pattern = {}
    result = ''
    index = 0
    for letter in word:
        if not letter in pattern:
            pattern[letter] = alphabet[index]
            index = index + 1
    for letter in word:
        result = result + pattern[letter]
    return result


def patternsFromFile():
    f = open('output.txt', 'a')
    result = {}
    for line in open('words_small.txt', 'r'):
        line = line.strip().lower()
        p = pattern(line)
        if p in result:
            result[p].append(line)
        else:
            result[p] = [line]
    f.write(str(result))
    f.close()


def solve(cipher, n):
    cipher = str(cipher).lower()
    possibilities = []
    poss2 = []
    result = {}
    for i in range(1, 27):
        possibilities.append(caesar(cipher, i))
        possibilities.append(caesar(cipher, i, True))
    for i in possibilities:
        for j in range(2, 10):
            poss2.append(divide(i, j))
    for string in itertools.imap(''.join, itertools.product(alphabet, repeat=2)):
        possibilities.append(vigenere(string, cipher, 'decrypt'))
    for item in possibilities:
        result[item] = freqDiff(ngram(item, n), n)
    for item in poss2:
        result[item] = freqDiff(ngram(item, n), n)
    sortedResult = sorted(result.iteritems(), key=operator.itemgetter(1))
    return sortedResult


def timing():
    result = []
    for j in range(5):
        for line in open('lotsofwords.txt', 'r'):
            pattern(line)
    return result


def patternLookup(patt):
    patt = pattern(nonAlpha.sub('', patt.lower()))
    try:
        return patterns[patt]
    except KeyError:
        return None

test1 = caesar(string1, 10, False)
test2 = caesar(string2, 3, True)

patternCipherTest = 'fybnqmf qjnqmf fwfsz dpngpsubcmf'
n = 2
#print solve(test2, n)[0:2]
#print solve(test1, n)[0:2]
#print solve(caesarText, n)[0:2]
#print solve(cipherText, n)[0:2]
#print solve(vigenereCipher, n)[0:2]


def patternTest(string):
    a = patternLookup(string)
    mapping = {}
    for char in string:
        mapping[char] = set()
    for word in a:
        for i in range(len(string)):
            mapping[string[i]].add(word[i])

    return mapping

unique = set()
fullset = set(alphabet)

for char in patternCipherTest:
    unique.add(char)

unique.remove(' ')

sets = []
for word in patternCipherTest.split():
    sets.append(patternTest(word))


for char in unique:
    result = fullset
    for s in sets:
        try:
            result = set.intersection(result, s[char])
        except KeyError:
            pass
    print char, result
