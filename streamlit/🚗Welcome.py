import streamlit as st

st.title("Welcome to my Car Max Analytics Dashboard")
st.header("Continue reading below to learn what else is available in this web application.")

with st.expander(label="Data"):
    st.write( "I used a data set of car appraisals and purchases from 2014 to 2022.")