import pandas as pd
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
