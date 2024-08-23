import pandas as pd 
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

data = pd.read_csv("../data/modeling.csv")

rename_color_cols = dict()
for i in data.color_grouped_appraisal.unique():
    rename_color_cols[i] = i + "_appraisal"
    
    
color_dummies = pd.get_dummies(data.color_grouped_appraisal).rename(
    columns = rename_color_cols
)

df = pd.concat([data, color_dummies], axis = 1).drop("color_grouped_appraisal", axis = 1)


appraisal_cols = list()
for i in df.columns:
    if "appraisal" in i:
        appraisal_cols.append(i)
    else:
        pass
    
X = df[appraisal_cols].drop(["make_appraisal", "model_appraisal"], axis = 1)
y = df.price

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=1)

X_test.shape[0]/X_train.shape[0]

rf = RandomForestRegressor(random_state=1)
rf = rf.fit(X_train, y_train)

rf.score(X_test, y_test) #15% rip
