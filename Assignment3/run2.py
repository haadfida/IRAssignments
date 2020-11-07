from numpy.ma import zeros

List2 = "ادب"

List = " ادبب ابد اادبب "

WordList = []
count = 0
WordName = []
Dict = {}
word = ""
for i in List:
    if not (i == ' ' or i == '<' or i == 's' or i == '>' or i == ' ' or i == '/'):
        WordName.append(i)
    else:
        word = ""
        for a in WordName:
            word += a
        if word != "":
            if word in Dict:
                Dict[word][0] += 1
                count += 1
            else:
                Dict[word] = [1, 0]
                count += 1
            WordList.append(word)
        WordName = []
    # print(i)

print(Dict)
print(count)

print(WordList)


def lev(a, b):
    if not a: return len(b)
    if not b: return len(a)
    return min(lev(a[1:], b[1:]) + (a[0] != b[0]), lev(a[1:], b) + 1, lev(a, b[1:]) + 1)


def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2 + 1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]


def editDist(x, y):
    rows = len(x)
    cols = len(y)
    D = zeros((len(x) + 1, len(y) + 1), dtype=int)

    count1 = 0
    for i in range(rows):
        D[i][0] = int(i)

    for j in range(cols):
        D[0][j] = int(j)

    for i in range(1, rows + 1):
        for j in range(1, cols + 1):
            subCost = 0
            if x[i - 1] != y[j - 1]:
                subCost = 1
            elif x[i - 1] != y[j - 1]:
                subCost = 0

            D[i, j] = min(D[i - 1, j - 1] + subCost, D[i - 1, j] + 1, D[i, j - 1] + 1, D[i - 2, j - 2] + 1)
    return D[rows, cols]



def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

#print(edits1("good"))

def genedit1(word):
    letters = 'ابپتٹثجچحخدڈذرڑزژسشصضطظعغفقکگلمنوہیے'
    letters2 = 'abcdefghijklmnopqrstuvwxyz'

    wordlen = len(word)
    #print(wordlen)

    insertions=[]
    deletions=[]
    transpositons=[]
    replacements=[]

    #insert 1 character
    for i in range(len(word)+1):
        for l in letters:
            insertions.append(word[:i] + l + word[i:])

    # delete 1 character
    for i in range(len(word)+1):
        deletions.append(word[:i-1] + word[i:])

    # replace 1 character
    for i in range(len(word)+1):
        for l in letters:
            replacements.append(word[:i-1] + l + word[i:])

        # replace 1 character

    for i in range(len(word)-1):
        transpositons.append(word[:i]+(word[i+1]+word[i])+ word[i+2:])

    return set(insertions+deletions+replacements+transpositons)


def readfile(name):
    file = open(name, "r+", encoding='utf-8')
    List = file.read()

    WordList = []
    count = 0
    WordName = []
    word = ""
    for i in List:
        if not (i == ' ' or i == '<' or i == 's' or i == '>' or i == ' ' or i == '/'):
            WordName.append(i)
        else:
            word = ""
            for a in WordName:
                word += a
            if word != "":
                WordList.append(word)
            WordName = []

    return WordList

errorList=readfile("jang_errors.txt")
#print(errorList)
nonErrorList=readfile("jang_nonerrors.txt")
#print(nonErrorList)

def readWordList(name):
    file = open(name, "r+", encoding='utf-8')
    List = file.read()

    WordList = []
    count = 0
    WordName = []
    word = ""
    for i in List:
        if i=='\n':
            word = ""
            for a in WordName:

                word += a
            if word != "":
                WordList.append(word)
            WordName = []
        else:
            WordName.append(i)
    return WordList

wordList=readWordList("wordlist.txt")
#print(wordList)

wordList=set(wordList)

for word in errorList:
    if word not in wordList:
        wordedit1= genedit1(word)
        candidateset= set()
        for edits in wordedit1:
            candidateset=candidateset.union(genedit1(edits))
        candidateset=candidateset.intersection(wordList)
        print(candidateset)


