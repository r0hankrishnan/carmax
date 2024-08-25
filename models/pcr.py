#Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.linear_model import LinearRegression
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cross_decomposition import PLSRegression, PLSSVD
from sklearn.metrics import mean_squared_error

#Load data, set target variable
data = pd.read_csv("../data/modeling.csv").drop("Unnamed: 0", axis = 1)
y = data.price

#Only considering continuous variables for now, remove all others
pick_numeric_cols = list()

for i in data.drop(["price", "cylinders_even_appraisal", "cylinders_high_appraisal"], axis = 1).columns:
    if data[i].dtype == "int64" or data[i].dtype == "float64":
        pick_numeric_cols.append(i)
        
#Set feature variables 
X = data[pick_numeric_cols]

#Scale features
scaling=StandardScaler()
scaling.fit(X)
scaled_X=scaling.transform(X)

#Initialize and fit PCA
pca = PCA()
reduced_X = pca.fit_transform(scaled_X)

#Look at first 5 components 
pd.DataFrame(pca.components_.T).loc[:,:5]

#10-fold CV, with shuffle
n = len(reduced_X)
kf_10 = model_selection.KFold(n_splits=10, shuffle=True, random_state=1)

regressor = LinearRegression()
mse = []

# Calculate MSE with only the intercept (no principal components in regression)
score = -1 * model_selection.cross_val_score(regressor, np.ones((n,1)), y.ravel(), cv=kf_10, scoring='neg_mean_squared_error').mean()    
mse.append(score)

# Calculate MSE using CV for the 19 principle components, adding one component at the time.
for i in np.arange(1, 8):
    score = -1 * model_selection.cross_val_score(regressor, reduced_X[:,:i], y.ravel(), cv=kf_10, scoring='neg_mean_squared_error').mean()
    mse.append(score)
    
# Plot results    
plt.plot(mse, '-o')
plt.xlabel('Number of principal components in regression')
plt.ylabel('MSE')
plt.title('Price')
plt.xlim(xmin=-1)

#Cumulative variance explained with each component
np.cumsum(np.round(pca.explained_variance_ratio_, decimals=4)*100)

#Run with training and testing sets
pca2 = PCA()

# Split into training and test sets
X_train, X_test , y_train, y_test = model_selection.train_test_split(X, y, test_size=0.3, random_state=1)

# Scale the training data
scaling.fit(X_train)
X_scaled_train = scaling.transform(X_train)
X_reduced_train = pca2.fit_transform(X_scaled_train)
n = len(X_reduced_train)

# 10-fold CV, with shuffle
kf_10 = model_selection.KFold(n_splits=10, shuffle=True, random_state=1)

mse = []

# Calculate MSE with only the intercept (no principal components in regression)
score = -1*model_selection.cross_val_score(regressor, np.ones((n,1)), y_train.ravel(), cv=kf_10, scoring='neg_mean_squared_error').mean()    
mse.append(score)

# Calculate MSE using CV for the 19 principle components, adding one component at the time.
for i in np.arange(1, 8):
    score = -1*model_selection.cross_val_score(regressor, X_reduced_train[:,:i], y_train.ravel(), cv=kf_10, scoring='neg_mean_squared_error').mean()
    mse.append(score)

plt.plot(np.array(mse), '-o')
plt.xlabel('Number of principal components in regression')
plt.ylabel('MSE')
plt.title('Salary')
plt.xlim(xmin=-1);
#There is a big drop from 1-2 components and again from 3-4 but then each successive drop is minimal
#Choosing 4 PCs to introduce a little bias and hopefully improve generizeability

#Scale test data
scaling.fit(X_test)
X_scaled_test = scaling.transform(X_test)

#Fit PCA and get only first 4 PCs
X_reduced_test = pca2.transform(X_scaled_test)[:,:5]

# Train regression model on training data 
regressor = LinearRegression()
regressor.fit(X_reduced_train[:,:5], y_train)

# Prediction with test data
pred = regressor.predict(X_reduced_test)
mean_squared_error(y_test, pred)

y_test[87721].item() #16500
pred[0].item() #21456.081099956245

