import sys
import nltk
import string
import pandas as pd
import numpy as np
import math
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import text

query_string = sys.argv[1]
cosine_sim_threshold = float(sys.argv[2])
top = int(sys.argv[3])

df_data = pd.read_csv('common_application_text_data_small.csv')
df_data['claim_text_orig'] = df_data['claim_text']
#take first 1000 characters for each claim text
df_data['claim_text'] = df_data['claim_text'].str[:10000]
# remove words smaller than 4 characters
df_data['claim_text'] = df_data['claim_text'].str.findall('\w{4,}').str.join(' ')

my_words = ['','()','(),']
my_stop_words = text.ENGLISH_STOP_WORDS.union(my_words)

tokenize = lambda doc: doc.lower().split(" ")
 
corpus_vectorizer = TfidfVectorizer(norm='l2', max_df=0.95, min_df=2, use_idf=True, smooth_idf=False, sublinear_tf=True,
                                stop_words=set(my_stop_words),
                                max_features = 200, tokenizer=tokenize)

corpus_tfidf = corpus_vectorizer.fit_transform(df_data['claim_text'])


def cosine_similarity(vector1, vector2):
    dot_product = sum(p*q for p,q in zip(vector1, vector2))
    magnitude = math.sqrt(sum([val**2 for val in vector1])) * math.sqrt(sum([val**2 for val in vector2]))
    if not magnitude:
        return 0
    return dot_product/magnitude

#query_string = df_data.iloc[300,1]
query_tfidf = corpus_vectorizer.transform([query_string])

df_result = pd.DataFrame(columns=['cosine_similarity', 'application_number', 'claim_text'])

# get the result and add to a new dataframe
loc_index = 0
patent_query = query_tfidf.toarray()[0]
for index_corpus, patent_corpus in enumerate(corpus_tfidf.toarray()):
    cosine_sim = cosine_similarity(patent_query, patent_corpus)
    if cosine_sim > cosine_sim_threshold:
        df_result.loc[loc_index] = [cosine_sim,df_data.iloc[index_corpus]['application_number'],df_data.iloc[index_corpus]['claim_text_orig']]
        loc_index += 1
        
# sort the results and pick top results        
df_result = df_result.sort_values('cosine_similarity',ascending=[False])
df_result = df_result[:top]
print(df_result)   