import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Explore", 
                   page_icon="📈", 
                   layout="centered", 
                   initial_sidebar_state="auto", 
                   menu_items=None)

#Page title
st.title("Explore the data")

#Generate data
@st.cache_data
def import_viz_data():
    data = pd.read_csv("./data/viz.csv").drop("Unnamed: 0", axis = 1)
    return data

#Load data
data = import_viz_data()

#Define filter choices 
region_choice = np.append("All", data.region.unique())
value_choice = ["Vehicle Make", "Vehicle Model", 
                "Vehicle Color"]

#Create/set global region filter in sidebar
with st.sidebar:
    st.subheader("🌎 Global Filters")
    region = st.selectbox(label="Choose a region", options=region_choice)

#Create/set bar-plot specific variable filter 
value = st.selectbox(label="Choose a variable to look at", options=value_choice)

#Create bar data with relevant columns renamed to be presentable
bar_data = data.copy().rename(columns={
    "make":"Sold Vehicle Make",
    "model":"Sold Vehicle Model",
    "make_appraisal":"Appraised Vehicle Make",
    "model_appraisal":"Appraised Vehicle Model",
    "color_grouped":"Sold Vehicle Color",
    "color_grouped_appraisal":"Appraised Vehicle Color"
})

#Generate the top 10 {variable} sold in {region}
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

#Generate the top 10 {variable} appraised in {region}
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

#Create data  
top10_data_sold = generate_top10_data_sold()
top10_data_appraised = generate_top10_data_appraised()

#Generate top 10 sold features bar plot
fig_sold = px.bar(top10_data_sold, x="value", y="count",
                  labels = {
                      "value":" ",
                      "count":"Count"
                  },
                  title = "Sold " + value,
                  text_auto=True,
                  color_discrete_sequence=["#ffd520"]*len(top10_data_sold)
                  )
fig_sold.update_xaxes(tickangle=45)
fig_sold.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)

#Create top 10 appraised features barplot
fig_appraised = px.bar(top10_data_appraised, x="value", y="count",
                       labels = {
                      "value":" ",
                      "count":"Count"
                  },
                  title = "Appraised " + value,
                  text_auto=True,
                  color_discrete_sequence=["#ffd520"]*len(top10_data_appraised)
                  )
fig_appraised.update_xaxes(tickangle=45)
fig_appraised.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)

#Create two columns
col1, col2 = st.columns(2)

#Display charts side-by-side
col1.plotly_chart(fig_sold)
col2.plotly_chart(fig_appraised)

#Generate data filtered by region for scatter plot
def generate_scatter_data():
    if region != "All":
        scatter_data = data[data["region"] == region]
    else:
        scatter_data = data
        
    return scatter_data

#Create scatter plot data
scatter_data = generate_scatter_data()

#Create list of numeric columns
num_cols = list()
for i in data.columns:
    if data[i].dtype == "int64" or data[i].dtype == "int32" or data[i].dtype == "float64" or data[i].dtype == "float64":
        num_cols.append(i)
    else:
        pass  

#List of possible x variables + make them look presentable
x_list = data.drop(["color_appraisal", "color", "model_appraisal", "model", "make_appraisal", "make"], axis=1).columns
x_list = [word.strip().title().replace("_", " ") for word in x_list]

#List of possible y variables + make them look presentable
y_list = num_cols
y_list = [word.strip().title().replace("_", " ") for word in x_list]

#Define x and y axes choices
x_choice = st.selectbox(label="Choose x axis", options=x_list)
y_choice = st.selectbox(label="Choose y axis", options=y_list)

#Generate plotly figure depending on x and y choice -- if x is not numeric make a barplot
def generate_xy_choice_fig():
    data = scatter_data.drop(["color_appraisal", "color", "model_appraisal", "model", "make_appraisal", "make"], axis=1)
    data[["model_year_appraisal", "model_year"]] = data[["model_year_appraisal", "model_year"]].astype(str)
    if data[x_choice.lower().replace(" ", "_")].dtype == "int64" or data[x_choice.lower().replace(" ", "_")].dtype == "int32" or data[x_choice.lower().replace(" ", "_")].dtype == "float64" or data[x_choice.lower().replace(" ", "_")].dtype == "float64":
        fig = px.scatter(scatter_data, x = x_choice.lower().replace(" ", "_"), y = y_choice.lower().replace(" ", "_"), 
                         opacity=0.60, 
                         labels={
                             x_choice.lower().replace(" ", "_"): x_choice.title().strip().replace("_", " "),
                             y_choice.lower().replace(" ", "_"): y_choice.title().strip().replace("_", " ")
                         },
                         title = x_choice.title().strip().replace("_", " ") +  " vs " + y_choice.title().strip().replace("_", " ") + " | Region: " + region
                         )
        fig.update_traces(marker_color = "#ffd520")
    
    else: 
        fig = px.box(scatter_data, x = x_choice.lower().replace(" ", "_"), y = y_choice.lower().replace(" ", "_"),
                     labels={
                         x_choice.lower().replace(" ", "_"): x_choice.title().strip().replace("_", " "),
                         y_choice.lower().replace(" ", "_"): y_choice.title().strip().replace("_", " ")
                     },
                     title = y_choice.title().strip().replace("_", " ") + " by " + x_choice.title().strip().replace("_", " ") +" | Region: " + region
                     )
        fig.update_traces(marker_color = "#ffd520")
    
    return fig

#Generate figure
fig_scatter = generate_xy_choice_fig()

#Display figure
st.plotly_chart(fig_scatter)


