import pandas as pd
import plotly.express as px
from scipy import stats
data = pd.read_csv("../data/viz.csv").drop("Unnamed: 0", axis = 1)
value_choice = ["Vehicle Make", "Vehicle Model", 
                "Vehicle Color"]
bar_data = data.copy().rename(columns={
    "make":"Sold Vehicle Make",
    "model":"Sold Vehicle Model",
    "make_appraisal":"Appraised Vehicle Make",
    "model_appraisal":"Appriased Vehicle Model",
    "color_grouped":"Sold Vehicle Color",
    "color_grouped_appraisal":"Appraised Vehicle Color"
})

value = value_choice[0]

value_sold = "Sold " + value


top10_data_sold = bar_data[value_sold].value_counts().to_frame().sort_values(by="count", ascending=False).head(10).reset_index().rename(
    columns={value_sold: "value"}
)

bar_data[bar_data["region"]=="West"][value_sold]

top10_data_sold = bar_data[bar_data["region"] == "Northeast"][value_sold].value_counts().to_frame().sort_values(by="count",ascending=False).head(10).reset_index().rename(
    columns={value_sold: "value"}
)

import plotly.express as px
fig = px.bar(top10_data_sold, x = "value", y = "count")
fig.show()

num_cols = list()
for i in data.columns:
    if data[i].dtype == "int64" or data[i].dtype == "int32" or data[i].dtype == "float64" or data[i].dtype == "float64":
        num_cols.append(i)
    else:
        pass 

x_choice = data.columns
y_choice = num_cols

x_choice = "medium_suv"
y_choice = "price"
region = "West"

data.dtypes
def generate_xy_choice_fig():
    if data[x_choice].dtype == "bool" or data[x_choice] == "object":
        fig = px.box(data, x = x_choice, y = y_choice,
                     labels={
                         x_choice: x_choice.title().strip().replace("_", " "),
                         y_choice: y_choice.title().strip().replace("_", " ")
                     },
                     title = x_choice.title().replace("_", " ") + " vs " + y_choice.title().strip().replace("_", " ") + " | Region: " + region
                     )
        
    else:
        fig = px.scatter(data, x = x_choice, y = y_choice, 
                         opacity=0.60, 
                         labels={
                             x_choice: x_choice.title().strip().replace("_", " "),
                             y_choice: y_choice.title().strip().replace("_", " ")
                         },
                         title = x_choice.title().replace("_", " ") + " vs " + y_choice.title().strip().replace("_", " ") + " | Region: " + region
                         )
    
    return fig

fig = generate_xy_choice_fig()
fig.show()


x_list = data.columns

capital = [word.strip().title().replace("_", " ") for word in x_list]

capital[0].lower()

capital[1].lower().replace(" ", "_")


#Figuring out how to do dynamic ANOVA tests in dashboard
data.columns

data.color_grouped.unique()

var_to_examine = "price"
group_to_compare = "color_grouped"
    
anova_dict = dict()
def fill_anova_dict():
    groups = data[group_to_compare].unique()
    for i in groups:
        anova_dict[i] = data[data[group_to_compare] == i][var_to_examine]
    return anova_dict

anova_dict = fill_anova_dict()

f_stat, p_val = stats.f_oneway(*anova_dict.values())

print(stats.f_oneway(*anova_dict.values()))