#Modules
import pandas as pd
import numpy as np 
from sklearn.preprocessing import OrdinalEncoder

#Load data, remove NAs
df = pd.read_csv("../data/carmax.csv")
data = df.copy().dropna()

#List categorical variables
catList = []
for col in data.columns:
    if data[col].nunique() <= 10:
        print(f"{col} has {data[col].nunique()} distinct values.")
        catList.append(col)

catList

#Fuction to only keep first 3 values of string
def removeL(value):
    return value[0:3]

#Copy data, remove Ls from engine and engine_appraisal columns
df2 = data.copy()
df2["engine_appraisal"]= df2["engine_appraisal"].apply(removeL).astype(float)
df2["engine"] = df2["engine"].apply(removeL).astype(float)

#Rename trim level columns
df2 = df2.rename(columns = {"trim_level":"trim_level_premium",
                            "trim_level_appraisal":"trim_level_appraisal_premium"})

#Convert trim_level columns into dummy columns
df2["trim_level_premium"] = pd.get_dummies(
    df2["trim_level_premium"])["Premium"]
df2["trim_level_appraisal_premium"] = pd.get_dummies(
    df2["trim_level_appraisal_premium"])["Premium"]

#Look at cylinders' columns
df2["cylinders"].unique() #Has 0 --> cars can't have 0 cylinders
df2["cylinders_appraisal"].unique()

#Replace 0 values with NA in cylinders columns
df2["cylinders"] = df2["cylinders"].replace(0, pd.NA)
df2["cylinders"].isna().sum() #521 NAs

#Remove newly made NAs -- check that it worked
df3 = df2.dropna()
print(f"{df3.shape[0]} vs {df2.shape[0]}. 
      Diff: {df3.shape[0] - df2.shape[0]}")

#Convert cylinders to int, check cylinders_appraisal
df3["cylinders"] = df3["cylinders"].astype(int)
df3["cylinders"].dtype
df3["cylinders_appraisal"].dtype

#Create dummy even column for cylinders and cylinders_appraisal
df3["cylinders_even"] = np.where(df3["cylinders"]%2==0,1,0)
df3["cylinders_appraisal_even"] = np.where(
    df3["cylinders_appraisal"]%2==0, 1, 0)

#Recheck unique values
for i in ["cylinders", "cylinders_appraisal", 
          "cylinders_even", "cylinders_appraisal_even"]:
    print(df3[i].unique())
    
#Create dummy columns for "high" cylinder values (based on googling)
df3["cylinders_high"] = np.where(df3["cylinders"] >= 6, 1, 0)
df3["cylinders_appraisal_high"] = np.where(
    df3["cylinders_appraisal"] >= 6, 1, 0)

#Drop cylinder columns
df4 = df3.copy().drop(["cylinders", "cylinders_appraisal"], axis = 1)

#Convert online_appraisal_flag to bool
df4["online_appraisal_flag"] = df4["online_appraisal_flag"].astype(bool)

#Look at vehicle type
df4["vehicle_type"] = df4["vehicle_type"].str.strip()
df4["vehicle_type"].unique()

df4["vehicle_type_appraisal"] = df4["vehicle_type_appraisal"].str.strip()
df4["vehicle_type_appraisal"].unique()

catList

df4["days_since_offer"].unique()
