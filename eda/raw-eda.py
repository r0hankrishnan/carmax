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

def removeL(value):
    return value[0:3]

df2 = df1.copy()
df2["engine_appraisal"]= df2["engine_appraisal"].apply(removeL).astype(float)
df2["engine"] = df2["engine"].apply(removeL).astype(float)

df2 = df2.rename(columns = {"trim_level":"trim_level_premium",
                            "trim_level_appraisal":"trim_level_appraisal_premium"})

df2.columns

df2["trim_level_premium"] = pd.get_dummies(df2["trim_level_premium"])["Premium"]
df2["trim_level_appraisal_premium"] = pd.get_dummies(df2["trim_level_appraisal_premium"])["Premium"]

df2[["trim_level_premium", "trim_level_appraisal_premium"]]

df2.groupby("online_appraisal_flag").mean(numeric_only=True)
df2["model_year"].nunique()

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


    
