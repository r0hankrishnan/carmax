#https://machinelearningmastery.com/lasso-regression-with-python/
#https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LassoCV.html

#Libraries
import pandas as pd
import numpy as np
from sklearn.linear_model import LassoCV, ElasticNetCV
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns

#Load data
data = pd.read_csv("../data/modeling.csv").drop("Unnamed: 0", axis = 1)


rename_color_cols = dict()
for i in data.color_grouped_appraisal.unique():
    rename_color_cols[i] = i.strip().lower() + "_appraisal"
    
    
color_dummies = pd.get_dummies(data.color_grouped_appraisal).rename(
    columns = rename_color_cols
)

rename_region_cols = dict()
for i in data.region.unique():
    rename_region_cols[i] = i.strip().lower()
    
region_dummies = pd.get_dummies(data.region).rename(
    columns = rename_region_cols
)

df = pd.concat([data, color_dummies, region_dummies], axis = 1).drop(["color_grouped_appraisal","make_appraisal", "model_appraisal", "region"], axis = 1)
cols = pd.DataFrame(df.columns).reset_index().rename(
    columns={"index":"col_index",
             0:"col_name"}
)
#Split data
X = df.drop("price", axis = 1)
y = df.price

X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size=0.40, 
                                                    random_state=1)

#Scale features
scale = StandardScaler()
X_train_scaled = scale.fit_transform(X_train)
X_test_scaled = scale.fit_transform(X_test)

#Fit lasso
reg = LassoCV(cv=5, random_state=0).fit(X_train_scaled, y_train)
reg.score(X_test_scaled, y_test) #19.84% best so far rip
pred = reg.predict(X_test_scaled)

#Plot predicted vs actual
fig = sns.scatterplot(x = y_test, y = pred) #rip

