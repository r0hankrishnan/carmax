import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats

st.warning("This page is just here to test various layouts for the three main pages of this dashboard. Please ignore!")


@st.cache_data
def import_viz_data():
    data = pd.read_csv("./data/viz.csv").drop("Unnamed: 0", axis = 1)
    return data

def fill_anova_dict(anova_dict):
    groups = data[group_to_compare].unique()
    for i in groups:
        anova_dict[i] = data[data[group_to_compare] == i][var_to_examine]
    return anova_dict

#Load data
data = import_viz_data()

#Title
st.title("Run an ANOVA test below!")
    
#ANOVA form
with st.container(border=True):
    var_to_examine_choice = ["Appraisal Offer", "Price"]
    
    var_to_examine = st.selectbox(label="Variable to examine", options=var_to_examine_choice).lower().replace(" ", "_")
    
    if var_to_examine == "price":
        group_to_compare_choice = ["Color Grouped", "Vehicle Type", "Model Year", "Region"]
    else:
        group_to_compare_choice = ["Color Grouped Appraisal", "Vehicle Type Appraisal", "Model Year Appraisal", "Region"] 
        
    group_to_compare = st.selectbox(label="Groups to compare", options=group_to_compare_choice).lower().replace(" ", "_")
    
    anova_submit = st.button(label="Run ANOVA")
    
if not anova_submit:
    with st.container(border=True):
        st.subheader("Click run to see results!")

if anova_submit:
    anova_dict = dict()
    anova_dict = fill_anova_dict(anova_dict)
    
    null = "There is no difference between " +  var_to_examine.replace("_", " ") + " across " + group_to_compare.replace("_", " ") + "."
    alternative = "There is a difference between " + var_to_examine.replace("_", " ") + " across "  + group_to_compare.replace("_", " ") + "."

    #Set alpha
    alpha = 0.50

    #Generate t stat and p val using scipy
    f_stat, p_val = stats.f_oneway(*anova_dict.values())

    #Check p val and assign correct values to decision and conclusion
    if p_val <= alpha:
        decision = "Reject"
    else:
        decision = "Fail to reject"

    # Conclusion
    if decision == "Reject":
        conclusion = "There is statistically significant evidence that at least one of the groups across " + group_to_compare.replace("_", " ") +  " have a different average "  + var_to_examine.replace("_", " ") + " than the others."
    else:
        conclusion = "There is insufficient evidence to claim a significant difference in average " + var_to_examine.replace("_", " ") + " across " + group_to_compare.replace("_", " ") + "."

    # Display results
    with st.container(border=True):
        st.metric(label="F-statistic (from scipy):", value=round(f_stat,2).astype(str))
        st.metric(label="P-value (from scipy):", value=round(p_val,4).astype(str))
        st.metric(label="Decision:", value=f"{decision} the null hypothesis at alpha = {alpha}.")
        st.divider()
        st.subheader(conclusion)


    
