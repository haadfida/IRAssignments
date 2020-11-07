import re
import pandas as pd

file = open("jang.txt", "r+", encoding='utf-8')
List = file.read()

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
                Dict[word] += 1
                count += 1
            else:
                Dict[word] = 1
                count += 1
            WordList.append(word)
        WordName = []
    # print(i)

print(Dict)
print(count)

print(WordList)

Unigram={}
for w in WordList:
    Unigram[w] = Dict[w] / count
    print(Unigram[w])


print(Unigram)
Bigram = {}
for i in range(len(WordList) - 1):
    #print(WordList[i] + " " + WordList[i + 1])
    Bigram[WordList[i] + " " + WordList[i + 1]] = Unigram[WordList[i]] * Unigram[WordList[i + 1]]

print(Bigram)


def genedit1(word):
    letters = 'ابپتٹثجچحخدڈذرڑزژسشصضطظعغفقکگلمنوہیے'

    insertions = []
    deletions = []
    transpositons = []
    replacements = []

    # insert 1 character
    for i in range(len(word) + 1):
        for l in letters:
            insertions.append(word[:i] + l + word[i:])

    # delete 1 character
    for i in range(len(word) + 1):
        deletions.append(word[:i - 1] + word[i:])

    # replace 1 character
    for i in range(len(word) + 1):
        for l in letters:
            replacements.append(word[:i - 1] + l + word[i:])

        # replace 1 character

    for i in range(len(word) - 1):
        transpositons.append(word[:i] + (word[i + 1] + word[i]) + word[i + 2:])

    return set(insertions + deletions + replacements + transpositons)


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
print(Dict)


i=0
probabilityList=[]
WordDict={}
for word in errorList:
    if word not in wordList:
        wordedit1= genedit1(word)
        candidateset= set()
        for edits in wordedit1:
            candidateset=candidateset.union(genedit1(edits))
        candidateset=candidateset.intersection(wordList)

        candwithscore=[]
        for candidate in candidateset:
            if candidate in Unigram:
                unigramscore= Unigram[candidate]
                bigram1=errorList[i-1] + " " + candidate
                bigram2=candidate + " " + errorList[i+1]
                probability=2*unigramscore
                if bigram1 in Bigram and bigram2 in Bigram:
                    bigramscore= Bigram[bigram1] * Bigram[bigram2]
                    probability=2*unigramscore+5*bigramscore
                candwithscore.append([probability,candidate])
            else:
                probability=0
                candwithscore.append([probability, candidate])
        df=pd.DataFrame(candwithscore,columns=['probability','candidate'])
        sort = df.sort_values(df.columns[0], ascending=False)
        sort=sort[:10]
        probabilityList.append([sort['candidate'].tolist(),sort['probability'].tolist()])
        sort=sort['candidate'].tolist()
        WordDict[word]=sort

    i+=1

print(WordDict)
f = open("reportfile.txt", "a", encoding='utf-8')
count=0
for i in range(len(errorList)-1):
    if errorList[i]!=nonErrorList[i]:
        f.write("Error=" + errorList[i] + " ")
        for k in probabilityList[count]:
            f.write(str(k))
        sortedList=WordDict[errorList[i]]
        for j in sortedList:
            if nonErrorList[i]==j:
                f.write(" " + errorList[i]+ "Error corrected successfully" + nonErrorList[i])
        f.write("\n")
        count+=1


