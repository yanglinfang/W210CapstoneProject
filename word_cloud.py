import csv
import os.path

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
    if(fileId in allowedId):
        with open(fName) as csvfile:
            spamreader = csv.reader(csvfile, delimiter= ' ', quotechar='|')
            for row in spamreader:
                #print(len(row))
                Id, firstWord = row[0].split(',')
                row[0] = firstWord 
                #print(Id, firstWord)
                if(rowId == Id):
                    returnList = row
                allRows += row 
    if(rowId == 'x'):
        return allRows
    else:  
        return returnList 
           
            
def getDict(inputList):
    counts = dict()
    for i in inputList:
        counts[i] = counts.get(i, 0) + 1
    return counts 

def saveToCsv(fName, counts, topWords):
    with open(prefix + fName + ending, 'w') as csvfile:
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
    return prefix + fName + ending
        
        
    