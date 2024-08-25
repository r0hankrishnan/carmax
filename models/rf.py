import pandas as pd 
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn import metrics

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
df.columns

# appraisal_cols = list()
# for i in df.columns:
#     if "appraisal" in i:
#         appraisal_cols.append(i)
#     else:
#         pass
    
X = df.drop(["price"], axis = 1)
y = df.price

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=1)

X_test.shape[0]/X_train.shape[0]

rf = RandomForestRegressor(random_state=1)
rf = rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)

#Not great performance
print('Mean Absolute Error (MAE):', metrics.mean_absolute_error(y_test, y_pred))
print('Mean Squared Error (MSE):', metrics.mean_squared_error(y_test, y_pred))
print('Root Mean Squared Error (RMSE):', metrics.mean_squared_error(y_test, y_pred, squared=False))
print('Mean Absolute Percentage Error (MAPE):', metrics.mean_absolute_percentage_error(y_test, y_pred))
print('Explained Variance Score:', metrics.explained_variance_score(y_test, y_pred))
print('Max Error:', metrics.max_error(y_test, y_pred))
print('Mean Squared Log Error:', metrics.mean_squared_log_error(y_test, y_pred))
print('Median Absolute Error:', metrics.median_absolute_error(y_test, y_pred))
print('R^2:', metrics.r2_score(y_test, y_pred))
print('Mean Poisson Deviance:', metrics.mean_poisson_deviance(y_test, y_pred))
print('Mean Gamma Deviance:', metrics.mean_gamma_deviance(y_test, y_pred))

rf.score(X_train, y_train) #88% training R2 -- maybe model is overfitting data?
rf.score(X_test, y_test) #17% rip -- if I take the opposite prediction, it's pretty good?

 
# Try changing n_estimators, max_features and max_depth
#Referencing https://stats.stackexchange.com/questions/558060/range-of-values-for-hyperparameter-fine-tuning-in-random-forest-classification

#Rerun rf with more trees- seems to be most important-- default is only 100
rf = RandomForestRegressor(random_state=1,
                           n_estimators=1000, 
                           n_jobs=-1)
rf = rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)

#Still pretty bad performance
print('Mean Absolute Error (MAE):', metrics.mean_absolute_error(y_test, y_pred))
print('Mean Squared Error (MSE):', metrics.mean_squared_error(y_test, y_pred))
print('Root Mean Squared Error (RMSE):', metrics.mean_squared_error(y_test, y_pred, squared=False))
print('Mean Absolute Percentage Error (MAPE):', metrics.mean_absolute_percentage_error(y_test, y_pred))
print('Explained Variance Score:', metrics.explained_variance_score(y_test, y_pred))
print('Max Error:', metrics.max_error(y_test, y_pred))
print('Mean Squared Log Error:', metrics.mean_squared_log_error(y_test, y_pred))
print('Median Absolute Error:', metrics.median_absolute_error(y_test, y_pred))
print('R^2:', metrics.r2_score(y_test, y_pred))
print('Mean Poisson Deviance:', metrics.mean_poisson_deviance(y_test, y_pred))
print('Mean Gamma Deviance:', metrics.mean_gamma_deviance(y_test, y_pred))

#There is likely some level of colinearity going on here

