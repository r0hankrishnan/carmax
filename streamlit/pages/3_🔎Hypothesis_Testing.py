import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats

#Page title
st.title("Run a t-test to determine if there is a significant difference between groups")

st.markdown("*ANOVA testing coming soon!*")

#Generate data
@st.cache_data
def import_viz_data():
    data = pd.read_csv("./data/viz.csv").drop("Unnamed: 0", axis = 1)
    return data

#Load data
data = import_viz_data()

#Choice lists
var_to_examine_choice = ["Appraisal Offer", "Price"]
group_to_compare_choice = ["Online Appraisal Flag", "Trim Level Premium Appraisal", "Trim Level Premium",
                           "Cylinders High Appraisal", "Cylinders High"]

#Define t-test variable and group
var_to_examine = st.selectbox(label="Pick a variable to examine", options=var_to_examine_choice).lower().replace(" ", "_")
group_to_compare = st.selectbox(label="Pick a group to compare", options=group_to_compare_choice).lower().replace(" ", "_")

#Create grouped lists
group_in = data[data[group_to_compare]==True][var_to_examine]
group_out = data[data[group_to_compare]==False][var_to_examine]

#Create null and alt hyp
null = "There is no difference between " +  var_to_examine.replace("_", " ") + " grouped by " + group_to_compare.replace("_", " ") + "."
alternative = "There is a difference between " + var_to_examine.replace("_", " ") + " grouped by "  + group_to_compare.replace("_", " ") + "."

#Set alpha
alpha = 0.50

#Generate t stat and p val using scipy
t_stat, p_val = stats.ttest_ind(group_in, group_out)

#Check p val and assign correct values to decision and conclusion
if p_val <= alpha:
    decision = "Reject"
else:
    decision = "Fail to reject"

# Conclusion
if decision == "Reject":
    conclusion = "There is statistically significant evidence that the average "  + var_to_examine.replace("_", " ") + " is different when grouped by " + group_to_compare.replace("_", " ") + "."
else:
    conclusion = "There is insufficient evidence to claim a significant difference in " + var_to_examine.replace("_", " ") + " when grouped by " + group_to_compare.replace("_", " ") + "."

# Display results
st.write("T-statistic (from scipy):", t_stat.astype(str))
st.write("P-value (from scipy):", p_val.astype(str))
st.write(f"Decision: {decision} the null hypothesis at alpha = {alpha}.")
st.write("Conclusion:", conclusion)