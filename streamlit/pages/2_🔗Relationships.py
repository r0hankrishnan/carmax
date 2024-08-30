import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

st.set_page_config(page_title="Relationships", 
                   page_icon="🔗", 
                   layout="centered", 
                   initial_sidebar_state="auto", 
                   menu_items=None)

#Page title
st.title("Explore the relationships between a vehicle's characteristics and its sale or appraisal price")

#Generate data
@st.cache_data
def import_viz_data():
    data = pd.read_csv("./data/viz.csv").drop("Unnamed: 0", axis = 1)
    
    return data
#Load data
with st.spinner("Loading data..."):
    data = import_viz_data()

#Region choice list
region_choice = np.append("All", data.region.unique())

#Create sidebar with global region filter
with st.sidebar:
    st.subheader("🌎 Global Filters")
    region = st.selectbox(label="Choose a region", options=region_choice)
    
#Filter for numeric columns
num_cols = list()
for i in data.columns:
    if data[i].dtype == "int64" or data[i].dtype == "int32" or data[i].dtype == "float64" or data[i].dtype == "float64":
        num_cols.append(i)
    else:
        pass  

#Create list of appraisal vars and purchased vars
appraised_cols = list()
purchased_cols = list()
for i in num_cols:
    if "appraisal" in i:
        appraised_cols.append(i)
    else:
        purchased_cols.append(i)
        
#Reformat variable names
appraised_cols_display = [word.strip().title().replace("_", " ") for word in appraised_cols]
purchased_cols_display = [word.strip().title().replace("_", " ") for word in purchased_cols]
        
#Generate correlation matrix data for purchased vehicles
def generate_correlations_sold():
    if region == "All":
        correlations_sold = pd.DataFrame(data[purchased_cols].corr())
    else:
        correlations_sold = pd.DataFrame(data[data["region"]==region][purchased_cols].corr())
        
    return correlations_sold

#Create corr data for purchased vehicles
with st.spinner("Calculating correlations..."):
    correlations_sold = generate_correlations_sold()

#Generate correlation matrix and update size
with st.spinner("Generating figure..."):
    fig_corr_sold = px.imshow(correlations_sold, x= purchased_cols_display, y = purchased_cols_display,
                    text_auto=True, color_continuous_scale=["white", "#ffd520"])
    fig_corr_sold.update_layout(width=1000,height=600)

#Generate correlation matrix data for appraised vehicles
def generate_correlations_appraisal():
    if region == "All":
        correlations_appraisal = pd.DataFrame(data[appraised_cols].corr())
    else:
        correlations_appraisal = pd.DataFrame(data[data["region"]==region][appraised_cols].corr())
        
    return correlations_appraisal

#Load corr data for appraised vehicles
with st.spinner("Calculating correlations..."):
    correlations_appraisal = generate_correlations_appraisal()

#Generate correlation matrix and update size
with st.spinner("Generating figure..."):
    fig_corr_appraised = px.imshow(correlations_appraisal, x=appraised_cols_display, y=appraised_cols_display, 
                    text_auto=True, color_continuous_scale=["white", "#ffd520"])
    fig_corr_appraised.update_layout(width=1000,height=600)


#Display charts
st.plotly_chart(fig_corr_sold)
st.plotly_chart(fig_corr_appraised)