import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats

#------CONFIG-----#
st.set_page_config(page_title="Hypothesis Testing", 
                   page_icon="🔎", 
                   layout="centered", 
                   initial_sidebar_state="auto", 
                   menu_items=None)

#------GLOBAL SETUP------#
#Generate data
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

#------TEST CHOICE------#
#Sidebar
with st.sidebar:
    test_type = st.selectbox(label="What type of hypothesis do you want to conduct?",
                             options=["T-test", "ANOVA"])

#----ANOVA-----#
#If ANOVA 
if test_type == "ANOVA":
    #Title
    st.title("Run an ANOVA test below!")
    
    #ANOVA form
    with st.container(border=True):
        var_to_examine_choice = ["Appraisal Offer", "Price"]
        
        var_to_examine = st.selectbox(label="Variable to examine", options=var_to_examine_choice).lower().replace(" ", "_")
        
        if var_to_examine == "price":
            group_to_compare_choice = ["Color Grouped", "Vehicle Type", "Model Year", "Region"]
        else:
            group_to_compare_choice = ["Color Grouped Appraisal", "Model Year Appraisal", "Region"]
            
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
    
#-----T TEST------#
#If T-test
if test_type == "T-test":
    
    #Page title
    st.title("Run a t-test below!")

    st.markdown("*ANOVA testing coming soon!*")
    
    #T-test form
    with st.container(border=True):
        #Choice lists
        var_to_examine_choice = ["Appraisal Offer", "Price"]
        
        #Define t-test variable and group
        var_to_examine = st.selectbox(label="Pick a variable to examine", options=var_to_examine_choice).lower().replace(" ", "_")

        if var_to_examine == "price":
            group_to_compare_choice = ["Online Appraisal Flag", "Trim Level Premium",
                                        "Cylinders High"]
        else:
            group_to_compare_choice = ["Online Appraisal Flag", "Trim Level Premium Appraisal", "Cylinders High Appraisal"]

        group_to_compare = st.selectbox(label="Pick a group to compare", options=group_to_compare_choice).lower().replace(" ", "_")

        #Submit button
        t_test_submit = st.button("Run test")
        
    if not t_test_submit:
        with st.container(border=True):
            st.subheader("Submit the form above to run your t-test")
                
    if t_test_submit:
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
        with st.container(border=True):
            st.metric(label="T-statistic (from scipy):", value=round(t_stat,2).astype(str))
            st.metric(label="P-value (from scipy):", value=round(p_val,4).astype(str))
            st.metric(label="Decision:", value=f"{decision} the null hypothesis at alpha = {alpha}.")
            st.divider()
            st.subheader(conclusion)
