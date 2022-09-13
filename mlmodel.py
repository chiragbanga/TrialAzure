import numpy as np
import pandas as pd
from traindata import df_fish

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression

y = df_fish['Species']
X = df_fish.drop('Species', axis=1)
#X = df_fish[['Weight', 'Length1', 'Length2', 'Length3', 'Height', 'Width']]

logistic_model = LogisticRegression()
model = logistic_model.fit(X,y)