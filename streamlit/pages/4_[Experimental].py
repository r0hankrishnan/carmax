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
        group_to_compare_choice = ["Color Grouped Appraisal", "Model Year Appraisal", "Region"]
        
    group_to_compare = st.selectbox(label="Groups to compare", options=group_to_compare_choice).lower().replace(" ", "_")
    
    anova_submit = st.button(label="Run ANOVA")
    
if not anova_submit:
    with st.container(border=True):
        st.subheader("Click run to see results!")

if anova_submit:
    anova_dict = dict()


anova_dict = fill_anova_dict()

st.text(anova_dict)
    
