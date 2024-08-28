#https://www.kaggle.com/code/sathyanarayanrao89/factor-analysis-and-svm-predictions

#Use prince package for FAMD
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import prince

#Preprocess data
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
X_train_scaled = pd.DataFrame(scale.fit_transform(X_train))
X_test_scaled = scale.fit_transform(X_test)

#Run FAMD
famd = prince.FAMD(n_components = 5, 
                   n_iter = 5, 
                   random_state = 1,
                   copy=True,
                   check_input=True,
                   engine="sklearn",
                   handle_unknown="error")

# get principal components
famd = famd.fit(X_train)

famd.row_coordinates(X_train).head()

famd.column_coordinates_

famd.plot(
    X_train,
    x_component=0,
    y_component=1
)

famd.column_contributions_.style.format('{:.0%}')


