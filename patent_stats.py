import csv
import os.path
import json
import numpy as np
import datetime

pathPrefix = 'static/data/chartdatafiles/'
prefix = pathPrefix + 'chart_cluster_data_'
ending = '.csv'
headerKeys = ['pub_year', 'appl_year', 'grant_year', 'years_to_publish', 'years_to_grant', 'patent_doc_kind', 'appl_change_count', 'number_of_claims']
headerValue = 'count'

def loadStatsFromOneFile(clusterStr):
    fName = ''

    if(len(clusterStr) == 2) and ('x' not in clusterStr):
        fName = prefix + clusterStr[0] + "_" + clusterStr[1] + ending
    #print fName

    dicts = []
    for keystr in headerKeys:
        dicts.append({})

    if(fName == ''):
        return dicts

    with open(fName) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        rowCount = -1
        for row in spamreader:
            rowCount += 1
            jsonStr = str(row).replace("['", '').replace("']", '')
            jsons = json.loads(jsonStr)
            for j in jsons:
                keystr = headerKeys[rowCount]
                if j[keystr] in dicts[rowCount]:
                    dicts[rowCount][j[keystr]] += int(j[headerValue])
                else:
                    dicts[rowCount][j[keystr]] = int(j[headerValue])

    return dicts

def mergeDicts(dict_full, dict_temp):
    for k, v in dict_temp.items():
        if len(str(k)) < 1:
            continue
        if k in dict_full:
            dict_full[k] += v
        else:
            dict_full[k] = v


def loadStatsFromFiles(clusterStr):
    clusters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    files = []
    dicts = []
    for keystr in headerKeys:
        dicts.append({})

    if clusterStr[0] == 'x':
        for x in clusters:
            if(clusterStr[1] == 'x'):
                for xx in clusters:
                    files.append(x + xx)
            else:
                files.append(x + clusterStr[1])
    else:
        if(clusterStr[1] == 'x'):
            for xx in clusters:
                files.append(clusterStr[0] + xx)
        else:
            files.append(clusterStr[0] + clusterStr[1])

    for f in files:
        temp = loadStatsFromOneFile(f)
        count = 0
        for d in dicts:
            mergeDicts(d, temp[count])
            count += 1

    return dicts

def saveToCsv(clusterStr, data_dict, header):
    fileToSave = prefix + clusterStr + '_' + header[0] + ending
    if os.path.isfile(fileToSave) == False:
        with open(fileToSave, 'w') as csvfile:
            fieldnames = header
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for key in data_dict:
                writer.writerow({header[0]: key, header[1]: data_dict[key]})
    return fileToSave


def createStatsSummary(clusterStr):
    dicts = loadStatsFromFiles(clusterStr)
    files = []
    count = 0
    for d in dicts:
        f = saveToCsv(clusterStr, d, [headerKeys[count], headerValue])
        files.append(f)
        count += 1

    return files
