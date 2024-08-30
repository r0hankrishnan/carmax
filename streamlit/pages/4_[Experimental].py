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



    
