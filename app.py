#
# W210 capstone project 
#
from pandas_datareader import data as web
import cufflinks
import pandas as pd
import plotly.plotly as py
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from patentSearchForm import PatentSearch
import query_similarity

import csv
import os.path
import word_cloud
import patent_stats

#
# Main app
#

app = Flask(__name__)

@app.route("/", methods=['GET'])
@app.route("/home", methods=['GET'])
@app.route("/patent", methods=['GET', 'POST'])
def patentMain():
    form = PatentSearch(csrf_enabled=False)
    if request.method == 'POST' and form.validate():
        # Load search result
        return redirect(url_for('patentResults',
                                abs=request.form['patent_abs'],
                                sim=request.form['patent_cosine_sim_threshold'],
                                top=request.form['patent_result_top']))
    return render_template('patentSearch.html', form=form)

@app.route("/patentResults/<abs>+<sim>+<top>")
def patentResults(abs, sim, top):
    return render_template('patentSearchResults.html', abs=abs, sim=sim, top=top)

@app.route('/static/data/topics/<path:path>')
def send_title_data(path):
    return send_from_directory('static/data/topics', path)

@app.route("/patent/wordcloud/<cluster_level_1>+<cluster_level_2>+<top_n>", methods=['GET'])
def wordCloud(cluster_level_1, cluster_level_2, top_n):
    fName = cluster_level_1 + '' + cluster_level_2
    if(len(fName)!=2):
        fName = 'xx' #if user input invalid cluster, we will default to show all topics
    filePath = "../../" + word_cloud.createTitleSummaryFile(fName, int(top_n))
    title='First level cluster: '
    if(cluster_level_1=='x'):
        title += 'All'
    else:
        title += cluster_level_1

    title += '. Second level cluster: '
    if(cluster_level_2=='x'):
        title += 'All.'
    else:
        title += cluster_level_2 + '.'

    return render_template('wordCloud.html', filePath=filePath, title=title)

@app.route("/patent/wordcloud", methods=['GET'])
def wordCloudToggle():
    cluster_level_1 = 'x'
    cluster_level_2 = 'x'
    top_n = 400
    return wordCloud(cluster_level_1, cluster_level_2, top_n)

@app.route('/static/data/chartdatafiles/<path:path>')
def send_chartdatafiles_data(path):
    return send_from_directory('static/data/chartdatafiles', path)

@app.route("/patent/patentstats/<cluster_level_1>+<cluster_level_2>+<keyName>", methods=['GET'])
def patentStats(cluster_level_1, cluster_level_2, keyName):
    fName = cluster_level_1 + '' + cluster_level_2
    if(len(fName)!=2):
        fName = 'xx' #if user input invalid cluster, we will default to show all topics 
    files = patent_stats.createStatsSummary(fName)
    i = patent_stats.findIndex(keyName) 
    labels = patent_stats.findLables(keyName) 
    fileName = "../../" + files[i]
    return render_template('patentStats.html', keyName=keyName, fileName=fileName, labels=labels)

if __name__ == '__main__':
    #if running local, you can use the following line
    #app.run(host='0.0.0.0', port=7777, debug=True)

    #if deploy to heroku, use the following line instead
    app.run()
