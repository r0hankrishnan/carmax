#Modules
import pandas as pd
import numpy as np 
import os

#Check cwd
os.getcwd()

#Data
df = pd.read_csv("../data/carmax.csv")

#Basic info about df
df.columns
df.shape
df.dtypes
for col in df.columns:
    if df[col].dtype == "object" or df[col].dtype == "string":
        print(col)

df["color"].unique() 
df["model_year_appraisal"].unique() #1992-2014
df["model_year_appraisal"].nunique()
#Can condense this list of colors into Gray, Black, White, 
# Red, Blue, Brown, Green, Orange, Yellow, Purple, Silver, Gold
df.describe()
df.isna().sum()

#Copy df and remove NAs
df1 = df.copy()
df1 = df1.dropna()
print(f"df shape: {df.shape} vs df1 shape: {df1.shape}")

#Check that NAs were removed
for col in df1.columns:
    if df1[col].isna().sum() != 0:
        print(f"{col} has {df1[col].isna().sum()} NA values")

df1.describe()
df1.nunique()

#Single out columns with under 10 unique values
catList = []
for col in df1.columns:
    if df1[col].nunique() <= 10:
        print(f"{col} has {df[col].nunique()} distinct values.")
        catList.append(col)
        
catList #List of variables that need encoding

df1.head()
df1["make_appraisal"].unique()
df1["model_appraisal"].unique()
df1["engine_appraisal"].unique()

#pip install plotly
#pip install nbformat

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import nbformat

fig = px.histogram(df, x="price", color="trim_level")
fig.show()

fig = px.scatter(df, x = "price", y = "appraisal_offer", size="days_since_offer", opacity=0.6)
fig.select_legends()
fig.show()


    
