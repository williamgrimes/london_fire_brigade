import numpy as np
import pandas as pd
import pickle

from corpus_extractor import *

import data_cleaning
from data_cleaning import *

import topic_modellor
from topic_modellor import *

import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')

import seaborn as sns

lfb = pd.read_csv('./data/lfb_all_primary_fire_data.csv')
lfb = convert_date_time(lfb)
corpus = pd.read_csv('./corpus/corpus.txt')
preprocesed = pd.read_csv('./corpus/preprocessed.txt')
vector, vector_fit, model = pickle.load(open("./model/model_pickled.p", "rb"))

#print_top_words(vector, model, 10)

lfb_free_text = CorpusExtractor().extract_free_text_only_data_frame(lfb)

lfb_free_text['year'] = lfb_free_text['DDDateTimeOfCall'].dt.year
lfb_free_text['month'] = lfb_free_text['DDDateTimeOfCall'].dt.month
lfb_free_text['weekday'] = lfb_free_text['DDDateTimeOfCall'].dt.weekday
lfb_free_text['year-month'] = lfb_free_text['DDDateTimeOfCall'].map(lambda x: x.strftime('%Y-%m'))

topic_classified = classify_model_topics(model, vector_fit)
lfb_free_text['topic'] = topic_classified.values

# pie - proportion of topics
df = lfb_free_text.topic.value_counts()
df.plot.pie()
plt.show()

# bar - number of topics
df = lfb_free_text.topic.value_counts()
sns.set_style("whitegrid")
sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 2.5})
ax = sns.barplot(x=df.index,y=df.values)
ax.set(xlabel='Topic', ylabel='Number of reports')
sns.plt.show()


# topic stacked area year-month
df = lfb_free_text[['year-month','topic']].pivot_table(index='year-month', columns='topic', aggfunc=len, fill_value=0)
ax = df.plot.area();
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 1.05, box.height])
ax.set(xlabel='Year-Month', ylabel='Proportion of reports')
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()



# facet plots
#df = lfb_free_text[['year','topic']].pivot_table(index='year', columns='topic', aggfunc=len, fill_value=0)
df = lfb_free_text[['topic','ActionBased']]
mapping = {k: v for v, k in enumerate(df.ActionBased.unique())}
df['ActionBased'] = df.ActionBased.map(mapping)
g = sns.FacetGrid(df, col="topic", col_wrap=4, margin_titles=True)
g.map(plt.hist,"ActionBased", normed=True)
plt.show()
