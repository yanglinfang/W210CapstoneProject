import csv
import os.path
import numpy as np 
from decimal import Decimal

allowedId = ['0','1','2','3','4','5','6','7','8','9','x']
pathPrefix = 'static/data/topics/'
prefix = pathPrefix + 'summary_'
ending = '.csv'
header = ['word', 'count']
fileNameSplit = '-'
def loadTitles(fileId, rowId):
    fName = pathPrefix + 'topics_'+ fileId + ending
    returnList = [] 
    allRows = [] 
    weights = np.logspace(0.8,0.1,dtype='double', num=2000)
    #print (weights) 
    if(fileId in allowedId):
        #print(fName)
        with open(fName) as csvfile:
            spamreader = csv.reader(csvfile, delimiter= ' ', quotechar='|')
            for row in spamreader:
                #print(len(row))
                Id, firstWord = row[0].split(',')
                row[0] = firstWord 
                row_with_weight = []
                index = 0 
                for row_word in row:
                    row_with_weight.append(row_word + '|' + "{0:.3f}".format(weights[index]))
                    index += 1
                #print (row)
                #print (row_with_weight)
                #print(Id, firstWord)
                if(rowId == Id):
                    returnList = row_with_weight
                allRows += row_with_weight 
    if(rowId == 'x'):
        return allRows
    else:  
        return returnList 
           
            
def getDict(inputList):
    counts = dict()
    #print (inputList)
    for word_with_weight in inputList:
        #print(word_with_weight)
        word, weightStr = word_with_weight.split('|')
        weight = Decimal(weightStr)
        counts[word] = counts.get(word, 0) + 1000 + int(weight*1000)
        #print(word, weight, counts[word])
    return counts 

def saveToCsv(fName, counts, topWords):
    with open(prefix + fName + '_' + str(topWords) + ending, 'w') as csvfile:
        fieldnames = header
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        wordsSaved = 0 
        for key in counts: 
            if(wordsSaved<topWords):
                writer.writerow({header[0]: key, header[1]: counts[key]})
                wordsSaved +=1 
            else:
                break 
        
def createTitleSummaryFile(fName, topWords):
    if os.path.isfile(prefix+fName+ending) == False:
        files = fName.split(fileNameSplit)
        wordList = []
        for f in files: 
            if(len(f)==2) and f[0] in allowedId and f[1] in allowedId:
                wordList += loadTitles(f[0], f[1])
        counts = getDict(wordList)
        saveToCsv(fName, counts, topWords)
    return prefix + fName + '_' + str(topWords) + ending
        
        
    