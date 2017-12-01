import csv
import os.path 
import json 
import numpy as np
import datetime

import plotly
import plotly.plotly as py
from plotly.graph_objs import Scatter, Layout, Bar


pathPrefix = 'static/data/chartdatafiles/'
prefix = pathPrefix + 'chart_cluster_data_'
ending = '.csv'
fileNameSplit = '_'

def loadStatsFromOneFile(clusterStr): 
    fName = ''
    
    if(len(clusterStr)==2) and ('x' not in clusterStr):
        fName = prefix + clusterStr[0] + fileNameSplit + clusterStr[1] + ending   
    #print fName
    
    pub_year_dict = {}
    appl_year_dict = {}
    years_to_publish_dict = {}
    
    if(fName == ''):
        return [pub_year_dict, appl_year_dict, years_to_publish_dict]
    
    with open(fName) as csvfile:
        spamreader = csv.reader(csvfile, delimiter= ' ', quotechar='|')
        rowCount = 0 
        for row in spamreader:
            rowCount += 1
            jsonStr = str(row).replace("['",'').replace("']",'')
            jsons = json.loads(jsonStr)
            for j in jsons:  
                if (rowCount == 1):
                    if j['pub_year'] in pub_year_dict:
                        pub_year_dict[j['pub_year']] += int(j['count'])
                    else:
                        pub_year_dict[j['pub_year']] = int(j['count'])

                if (rowCount == 2):
                    if j['appl_year'] in appl_year_dict:
                        appl_year_dict[j['appl_year']] += int(j['count'])
                    else:
                        appl_year_dict[j['appl_year']] = int(j['count'])

                if (rowCount == 3):
                    if j['years_to_publish'] in years_to_publish_dict:
                        years_to_publish_dict[j['years_to_publish']] += int(j['count'])
                    else:
                        years_to_publish_dict[j['years_to_publish']] = int(j['count'])

    return [pub_year_dict, appl_year_dict, years_to_publish_dict]

def mergeDicts(dict_full, dict_temp):
    for k,v in dict_temp.items():
        if k in dict_full:
            dict_full[k] += v
        else:
            dict_full[k] = v
            
def loadStatsFromFiles(clusterStr): 
    clusters = ['0','1','2','3','4','5','6','7','8','9']
    files = []
    pub_year_dict = {}
    appl_year_dict = {}
    years_to_publish_dict = {}
    
    if clusterStr[0] == 'x':
        for x in clusters: 
            if(clusterStr[1] == 'x'):
                for xx in clusters:
                    files.append(x+xx)
            else:
                files.append(x+clusterStr[1])
    else:
        if(clusterStr[1] == 'x'):
            for xx in clusters:
                files.append(clusterStr[0]+xx)
        else:
            files.append(clusterStr[0]+clusterStr[1])

    for f in files: 
        temp = loadStatsFromOneFile(f)
        mergeDicts(pub_year_dict, temp[0])
        mergeDicts(appl_year_dict, temp[1])
        mergeDicts(years_to_publish_dict, temp[2])

    return [pub_year_dict, appl_year_dict, years_to_publish_dict]
   
def saveToCsv(clusterStr, data_dict, header):
    fileToSave = prefix + clusterStr + fileNameSplit + header[0] + ending
    if os.path.isfile(fileToSave) == False:
        with open(fileToSave, 'w') as csvfile:
            fieldnames = header
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for key in data_dict: 
                writer.writerow({header[0]: key, header[1]: data_dict[key]})
    return fileToSave

def createStatsSummary(clusterStr):
    [pub_year_dict, appl_year_dict, years_to_publish_dict] = loadStatsFromFiles(clusterStr)
    f1 = saveToCsv(clusterStr, pub_year_dict, ["pub_year","count"])
    f2 = saveToCsv(clusterStr, appl_year_dict, ["appl_year","count"])
    f3 = saveToCsv(clusterStr, years_to_publish_dict, ["years_to_publish","count"])
    return [f1, f2, f3]