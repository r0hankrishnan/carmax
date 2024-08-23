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
                            "trim_level_appraisal":"trim_level_premium_appraisal"})

#Convert trim_level columns into dummy columns
df2["trim_level_premium"] = pd.get_dummies(
    df2["trim_level_premium"])["Premium"]
df2["trim_level_premium_appraisal"] = pd.get_dummies(
    df2["trim_level_premium_appraisal"])["Premium"]

#Look at cylinders' columns
df2["cylinders"].unique() #Has 0 --> cars can't have 0 cylinders
df2["cylinders_appraisal"].unique()

#Replace 0 values with NA in cylinders columns
df2["cylinders"] = df2["cylinders"].replace(0, pd.NA)
df2["cylinders"].isna().sum() #521 NAs

#Remove newly made NAs -- check that it worked
df3 = df2.dropna()
print(f"{df3.shape[0]} vs {df2.shape[0]}. Diff: {df3.shape[0] - df2.shape[0]}")

#Convert cylinders to int, check cylinders_appraisal
df3["cylinders"] = df3["cylinders"].astype(int)
df3["cylinders"].dtype
df3["cylinders_appraisal"].dtype

#Create dummy even column for cylinders and cylinders_appraisal
df3["cylinders_even"] = np.where(df3["cylinders"]%2==0,1,0)
df3["cylinders_even_appraisal"] = np.where(
    df3["cylinders_appraisal"]%2==0, 1, 0)

#Recheck unique values
for i in ["cylinders", "cylinders_appraisal", 
          "cylinders_even", "cylinders_even_appraisal"]:
    print(df3[i].unique())
    
#Create dummy columns for "high" cylinder values (based on googling)
df3["cylinders_high"] = np.where(df3["cylinders"] >= 6, 1, 0)
df3["cylinders_high_appraisal"] = np.where(
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

#Create dicts to rename dummy columns
vehicle_dict = dict()
for i in df4["vehicle_type"].unique():
    vehicle_dict[i] = i.strip().lower().replace(" ", "_")
    
vehicle_appraisal_dict = dict()
for i in df4["vehicle_type_appraisal"].unique():
    vehicle_appraisal_dict[i] = i.strip().lower().replace(" ", "_") + "_appraisal"

#Generate dummy columns and rename using dicts
vehicle_df = pd.get_dummies(df4["vehicle_type"]).rename(
    columns = vehicle_dict)

vehicle_appraisal_df = pd.get_dummies(df4["vehicle_type_appraisal"]).rename(
    columns=vehicle_appraisal_dict)

#Look at days_since_offer-- I think it's fine to stay as int
df4["days_since_offer"].unique()
df["days_since_offer"].dtype

#Concatenate df and dummies
df4 = pd.concat([df4, vehicle_df, vehicle_appraisal_df], axis = 1)

#Create copy of df and drop vehicle type non-dummy columns
df5 = df4.copy()
df5 = df5.drop(["vehicle_type", "vehicle_type_appraisal"], axis = 1)
df5.columns

#Convert year columns to str and create dummies
df5["model_year"] = df5["model_year"].astype(str)
df5["model_year_appraisal"] = df5["model_year_appraisal"].astype(str)

#Create dummy df for model year
model_year_df = pd.get_dummies(df5["model_year"])

#Create renaming dict for model_year_appraisal
model_year_appraisal_dict = dict()
for i in df5["model_year_appraisal"].unique():
    model_year_appraisal_dict[i] = i + "_appraisal"

#Create dummy df for model_year_appraisal
model_year_appraisal_df = pd.get_dummies(df5["model_year_appraisal"]).rename(
    columns = model_year_appraisal_dict
)

#Copy df5, add dummies, drop non-dummy model_year cols
df6 = df5.copy()
pd.concat([df6, model_year_df, model_year_appraisal_df], axis = 1)
df = df6.drop(["model_year", "model_year_appraisal"], axis = 1)


