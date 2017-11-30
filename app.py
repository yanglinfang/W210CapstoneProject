#
# Historical Stock Prices
# using Python & Flask & Plotly
#
# stock_interactive.py
#
# The Python Quants GmbH
#
from pandas_datareader import data as web
import cufflinks
import pandas as pd
import plotly.plotly as py
from flask import Flask, request, render_template, redirect, url_for
from forms import SymbolSearch
from patentSearchForm import PatentSearch
import query_similarity

import csv
import os.path
import word_cloud

# login to plot.ly
py.sign_in('yanglinfang', 'F5jaY29GDfD8TIenMz9p')

#
# Main app
#

app = Flask(__name__)


@app.route("/symbol", methods=['GET', 'POST'])
def main():
    form = SymbolSearch(csrf_enabled=False)
    if request.method == 'POST' and form.validate():
        return redirect(url_for('results', symbol=request.form['symbol'],
                                trend1=request.form['trend1'],
                                trend2=request.form['trend2']))
    return render_template('selection.html', form=form)


@app.route("/symbol/<symbol>+<trend1>+<trend2>")
def results(symbol, trend1, trend2):
    data = web.DataReader(symbol, data_source='yahoo')
    data['Trend 1'] = data['Adj Close'].rolling(int(trend1)).mean()
    data['Trend 2'] = data['Adj Close'].rolling(int(trend2)).mean()
    url = data[['Adj Close', 'Trend 1', 'Trend 2']].iplot(asUrl=True)
    table = data.tail().to_html()
    return render_template('plotly.html', symbol=symbol,
                           plot=url, table=table)


@app.route("/home", methods=['GET'])
def home():
    return render_template('home.html')


@app.route("/", methods=['GET'])
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
    # call from query_similarity to get search results
    data, data_type = query_similarity.search(abs, sim, top)
    # convert dataframe to table, tell pandas to not truncate width
    pd.set_option('display.max_colwidth', -1)
    table = data.to_html()
    return render_template('patentSearchResults.html', abs=abs, sim=sim, top=top, table=table)


@app.route("/patent/wordcloud/<cluster_level_1>+<cluster_level_2>+<top_n>", methods=['GET'])
def wordCloud(cluster_level_1, cluster_level_2, top_n):
    fName = cluster_level_1 + '' + cluster_level_2
    if(len(fName)!=2):
        fName = 'xx' #if user input invalid cluster, we will default to show all topics from level 1
    filePath = "../../" + word_cloud.createTitleSummaryFile(fName, int(top_n))
    return render_template('wordCloud.html', filePath=filePath)


if __name__ == '__main__':
    #if running local, you can use the following line
    #app.run(host='0.0.0.0', port=5000, debug=True)

    #if deploy to heroku, use the following line instead
    app.run()
