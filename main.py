import pandas as pd
import numpy as np

from sklearn.preprocessing import LabelEncoder
from collections import defaultdict

import free_text
from free_text import CorpusExtractor
from free_text import TopicModelling

import data_cleaning
from data_cleaning import DataCleaning

lfb = pd.read_csv('./data/lfb_all_primary_fire_data.csv')
lfb_cleaned = DataCleaning.all_cleaning(lfb)
lfb_complete = lfb.dropna(1)

columns = ['IncidentNumber', 'DDDateTimeOfCall', 'easting', 'northing',
 'IncGeo_DACarea' ,'StnGround', 'StnGroundName', 'StnGrndBorough',
 'LondonBorough']
lfb_complete = lfb_complete.drop(columns, 1)

d = defaultdict(LabelEncoder)
lfb_complete_label_encode = lfb_complete.apply(
    lambda x: d[x.name].fit_transform(x)
)
lfb_complete_label_encode.to_csv(r'data/lfb_label_encoded.csv', index=None)
