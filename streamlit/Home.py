import streamlit as st
import pandas as pd
import plotly.express as px


@st.cache_data
def import_viz_data():
    data = pd.read_csv("./data/viz.csv").drop("Unnamed: 0", axis = 1)
    return data

data = import_viz_data()
    
region_choice = data.region.unique()
value_choice = ["Sold Vehicle Make", "Sold Vehicle Model", 
                "Appraised Vehicle Make", "Appriased Vehicle Model",
                "Sold Vehicle Color", "Appraised Vehicle Color"]

region = st.selectbox(label="Choose a region", options=region_choice)
value = st.selectbox(label="Choose a variable to look at", options=value_choice)

bar_data = data.copy().rename(columns={
    "make":"Sold Vehicle Make",
    "model":"Sold Vehicle Model",
    "make_appraisal":"Appraised Vehicle Make",
    "model_appraisal":"Appriased Vehicle Model",
    "color_grouped":"Sold Vehicle Color",
    "color_grouped_appraisal":"Appraised Vehicle Color"
})
top10_data = bar_data[bar_data["region"] == region][value].value_counts().to_frame().sort_values(by="count",ascending=False).head(10).reset_index()

fig = px.bar(top10_data, x = value, y = "count")
st.plotly_chart(fig)