import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats

st.warning("This page is just here to test various layouts for the three main pages of this dashboard. Please ignore!")


@st.cache_data
def import_viz_data():
    data = pd.read_csv("./data/viz.csv").drop("Unnamed: 0", axis = 1)
    return data

#Load data
data = import_viz_data()
#Page title
st.title("Run a t-test below!")

st.markdown("*ANOVA testing coming soon!*")

#T-test form
with st.container(border=True):
    #Choice lists
    var_to_examine_choice = ["Appraisal Offer", "Price"]
    
    #Define t-test variable and group
    var_to_examine = st.selectbox(label="Pick a variable to examine", options=var_to_examine_choice).lower().replace(" ", "_")
    st.write(var_to_examine)
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
