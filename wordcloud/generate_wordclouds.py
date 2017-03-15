import sys
sys.path.insert(0,'..')

import numpy as np
import pandas as pd
import pickle

import pyLDAvis
import pyLDAvis.sklearn

from corpus_extractor import *

import topic_modellor
from topic_modellor import *

from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
from scipy.misc import imread

from matplotlib import pyplot as plt


vector, vector_fit, model = pickle.load(open("../model/model_pickled.p", "rb"))

n_words = 100

topic_words = get_top_words(vector, model, n_words)
n_topics = model.n_topics

fire = imread("fire.png")
image_colors = ImageColorGenerator(fire)


for topic in range(n_topics):
    max_tokens = 15
    df = pd.DataFrame(topic_words[topic],
                      columns=['token', 'topic_word_dist'])
    df.sort('topic_word_dist', inplace=True, ascending=True)
    df['cumulative'] = df.topic_word_dist.cumsum()
    df['weight']= (df.cumulative/df.cumulative.max())
    df.sort('weight', inplace=True, ascending=False)

    tail = 1 - df.ix[max_tokens, 'weight']
    #tail = df.ix[max_tokens:, 'weight'].sum()
    df2 = df.iloc[0:max_tokens].copy()
    nrow = pd.Series({'token': '--[other terms]--', 'weight': tail})
    df2.ix[df2.shape[0]] = nrow
    df2.index = np.arange(df2.shape[0])

    plt.figure(figsize=(10,5))
    colors = []
    for c in range(df2.shape[0]-1):
        colors.append('#383838')

    colors.append('#ebe728')
    plt.barh(df2.index * -1, df2['weight'], color=colors)
    plt.gca().yaxis.grid(False)
    plt.yticks(df2.index * -1 + 0.1, df2['token'])
    plt.ylim(-1 * df2.shape[0] + 0.8, 1)
    plt.xlabel('weight')
    plt.savefig('plots/topic_'+str(topic + 1)+'.png',
                bbox_inches='tight'
               )

    # mask black
    wc = WordCloud(prefer_horizontal=1.0,
                   width=1920,
                   height=1080,
                   mask=fire,
                   background_color="black").fit_words(topic_words[topic])
    plt.figure( figsize=(60,50), facecolor='black' )
    plt.imshow(wc.recolor(color_func=image_colors))
    plt.axis("off")
    plt.savefig('mask_black/topic_'+str(topic + 1)+'.png',
                facecolor='k',
                bbox_inches='tight'
               )

    # mask white
    wc = WordCloud(prefer_horizontal=1.0,
                   width=1920,
                   height=1080,
                   mask=fire,
                   background_color="white").fit_words(topic_words[topic])
    plt.figure( figsize=(60,50), facecolor='black' )
    plt.imshow(wc.recolor(color_func=image_colors))
    plt.axis("off")
    plt.savefig('mask_white/topic_'+str(topic + 1)+'.png',
                facecolor='k',
                bbox_inches='tight'
               )


    # default black
    wc = WordCloud(prefer_horizontal=1.0,
                   width=1920,
                   height=1080,
                   background_color="black").fit_words(topic_words[topic])
    plt.figure( figsize=(40,30), facecolor='black' )
    plt.imshow(wc)
    plt.axis("off")
    plt.savefig('default_black/topic_'+str(topic + 1)+'.png',
                facecolor='k',
                bbox_inches='tight')

    # default white
    wc = WordCloud(prefer_horizontal=1.0,
                   width=1920,
                   height=1080,
                   background_color="white").fit_words(topic_words[topic])
    plt.figure( figsize=(40,30), facecolor='black' )
    plt.imshow(wc)
    plt.axis("off")
    plt.savefig('default_white/topic_'+str(topic + 1)+'.png',
                facecolor='k',
                bbox_inches='tight')

    print('saving topic ' + str(topic + 1))
