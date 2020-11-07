import os
from decimal import Decimal
from os import listdir


def getFileNamesAndCount(path):
    files = []
    count = 0
    for file in listdir(path):
        files.append(os.path.join(path, file))
        count += 1
    return files, count


def readfile(name, WordList):
    file = open(name, "r+", errors='replace')
    List = file.read()

    WordName = []
    for i in List:
        if i.isalpha():
            WordName.append(i)
        else:
            word = ""
            for a in WordName:
                word += a
            if word != "":
                WordList.append(word)
            WordName = []

    return WordList


def getAllWords(path):
    allWords = []
    files, count = getFileNamesAndCount(path)
    for f in files:
        readfile(f, allWords)

    return allWords, count


def findTermFrequency(List, Dict):
    for w in List:
        if w in Dict.keys():
            Dict[w] += 1
        else:
            Dict[w] = 1


def trainNaiveBayes(d, c):
    print("Training Naive Bayes")
    path1 = d + "\\" + c[0]
    path2 = d + "\\" + c[1]
    HamList, hamFileCount = getAllWords(path1)
    SpamList, spamFileCount = getAllWords(path2)

    CombinedList = HamList + SpamList

    hamTermFreq = {}
    spamTermFreq = {}

    findTermFrequency(HamList, hamTermFreq)
    findTermFrequency(SpamList, spamTermFreq)

    V = set(CombinedList)
    vCount = len(V)

    hamProb = {}
    hamWordCount = len(HamList)
    spamProb = {}
    spamWordCount = len(SpamList)

    for w in hamTermFreq:
        hamProb[w] = float((hamTermFreq[w] + 1) / float(hamWordCount + vCount))
    for w in spamTermFreq:
        spamProb[w] = float((spamTermFreq[w] + 1) / float(spamWordCount + vCount))

    priorHam = hamFileCount / (hamFileCount + spamFileCount)
    priorSpam = spamFileCount / (hamFileCount + spamFileCount)

    return priorHam, priorSpam, hamProb, spamProb, vCount, hamWordCount, spamWordCount


priorHam, priorSpam, hamProb, spamProb, V, hWC, sWC = trainNaiveBayes("train", ["ham", "spam"])


def calculateDocMetrics(path):
    files, count = getFileNamesAndCount(path)
    pHamcount = 0
    pSpamcount = 0
    for f in files:
        words = []
        words = readfile(f, words)
        pHam = Decimal(priorHam)
        pSpam = Decimal(priorSpam)
        for w in words:
            if w in hamProb:
                pHam = Decimal(pHam * Decimal(hamProb[w]))
            else:
                pHam = Decimal(pHam * 1 / (hWC + V))
            if w in spamProb:
                pSpam = Decimal(pSpam * Decimal(spamProb[w]))
            else:
                pSpam = Decimal(pSpam * Decimal(1 / (sWC + V)))

        if pHam < pSpam:
            pSpamcount += 1
        else:
            pHamcount += 1

    return pHamcount, pSpamcount


def trainNaiveBayes(d, c):
    print("Testing Naive Bayes")
    path1 = d + "\\" + c[0]
    path2 = d + "\\" + c[1]
    count1, count2 = calculateDocMetrics(path1)
    count3, count4 = calculateDocMetrics(path2)

    print("Printing Metrics")
    print("TN: " + str(count1))
    print("FP: " + str(count2))
    print("FN: " + str(count3))
    print("TP: " + str(count4))

    return count1, count2, count3, count4


TN, FP, FN, TP = trainNaiveBayes("test", ["ham", "spam"])

precision = TP / (TP + FP)
recall = TP / (TP + FN)
accuracy = (TP + TN) / (TP + TN + FP + FN)
F1 = (2 * TP) / (2 * TP + FP + FN)

print("Precision: " + str(precision))
print("Recall: " + str(recall))
print("F1: " + str(F1))
print("Accuracy: " + str(accuracy))
