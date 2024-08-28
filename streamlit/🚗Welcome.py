import streamlit as st

st.title("Welcome to my CarMax Analytics Dashboard")
st.divider()
st.markdown("### Continue reading below to learn what else is available in this web application.")

"This dashboard uses a data set of car appraisal and purchases at CarMax stores across the US from 2014 to 2022."

st.markdown("**You can access 3 pages with this dashboard:**")

with st.expander(label="Explore the data"):
    st.markdown("The first page lets you explore the top characteristics for " 
                "appraised and purchased vehicles. You can filter by characteristic and region. "
                "This section is for learning more about the general trends of the data. "
                "Use the global region filters to extract insights for specific regions and the "
                "chart-specific filters to drill down into the specific values you want to find.")
    
with st.expander(label="Explore relationships between variables"):
    st.markdown("The second page lets you examine how each variable relates to each other "
                "between sold and appraised cars. Again, you can filter by region to see if "
                "the relationship changes depending on where the trade-in or sale occurred."
        )
    
with st.expander(label="Conduct basic hypothesis testing"):
    st.markdown("The third page allows you to compare the difference between average "
                "appraisal offer or sale price between several groups. Support for multiple "
                "group comparison (ANOVA) in the works!")
