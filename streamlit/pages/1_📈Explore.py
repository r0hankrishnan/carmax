import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


@st.cache_data
def import_viz_data():
    data = pd.read_csv("./data/viz.csv").drop("Unnamed: 0", axis = 1)
    return data

data = import_viz_data()
    
region_choice = np.append("All", data.region.unique())
value_choice = ["Vehicle Make", "Vehicle Model", 
                "Vehicle Color"]

with st.sidebar:
    st.subheader("Global Filters")
    st.divider()
    region = st.selectbox(label="Choose a region", options=region_choice)


value = st.selectbox(label="Choose a variable to look at", options=value_choice)

bar_data = data.copy().rename(columns={
    "make":"Sold Vehicle Make",
    "model":"Sold Vehicle Model",
    "make_appraisal":"Appraised Vehicle Make",
    "model_appraisal":"Appraised Vehicle Model",
    "color_grouped":"Sold Vehicle Color",
    "color_grouped_appraisal":"Appraised Vehicle Color"
})

def generate_top10_data_sold():
    value_sold = "Sold " + value

    if region != "All":
        top10_data_sold = bar_data[bar_data["region"] == region][value_sold].value_counts().to_frame().sort_values(by="count",ascending=False).head(10).reset_index().rename(
            columns = {value_sold:"value"}
        )
    else: 
        top10_data_sold = bar_data[value_sold].value_counts().to_frame().sort_values(by="count", ascending=False).head(10).reset_index().rename(
            columns={value_sold:"value"}
        )
    
    return top10_data_sold

def generate_top10_data_appraised():
    value_appraised = "Appraised " + value

    if region != "All":
        top10_data_appraised = bar_data[bar_data["region"] == region][value_appraised].value_counts().to_frame().sort_values(by="count",ascending=False).head(10).reset_index().rename(
            columns = {value_appraised:"value"}
        )
    else: 
        top10_data_appraised = bar_data[value_appraised].value_counts().to_frame().sort_values(by="count", ascending=False).head(10).reset_index().rename(
            columns={value_appraised:"value"}
        )
    
    return top10_data_appraised
    
top10_data_sold = generate_top10_data_sold()
top10_data_appraised = generate_top10_data_appraised()

fig_sold = px.bar(top10_data_sold, x="value", y="count",
                  labels = {
                      "value":" ",
                      "count":"Count"
                  },
                  title = "Sold " + value,
                  text_auto=True)
fig_sold.update_xaxes(tickangle=45)
fig_sold.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)


fig_appraised = px.bar(top10_data_appraised, x="value", y="count",
                       labels = {
                      "value":" ",
                      "count":"Count"
                  },
                  title = "Appraised " + value,
                  text_auto=True)
fig_appraised.update_xaxes(tickangle=45)
fig_appraised.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)



col1, col2 = st.columns(2)

col1.plotly_chart(fig_sold)
col2.plotly_chart(fig_appraised)

def generate_scatter_data():
    if region != "All":
        scatter_data = data[data["region"] == region]
    else:
        scatter_data = data
        
    return scatter_data

scatter_data = generate_scatter_data()
fig_scatter = px.scatter(scatter_data, x = "price", y = "appraisal_offer", 
                         opacity=0.60, 
                         labels={
                             "price":"Sold Vehicle Price",
                             "appraisal_offer":"Appraised Vehicle Offer"
                         },
                         title = "Sale Price vs Appraisal Offer | Region: " + region,)
st.plotly_chart(fig_scatter)
