# importing needed libraries
import streamlit as st
import EDA

# Title
st.markdown(" <center>  <h1> Flights Dataset </h1> </font> </center> </h1> ",
            unsafe_allow_html=True)

# Link of Data
st.markdown(
    '<a href="https://www.kaggle.com/datasets/usdot/flight-delays/"> <center> Link to Dataset  </center> </a> ',
    unsafe_allow_html=True)
st.markdown(
    '<a href="https://www.kaggle.com/datasets/smiller933/bts/"> <center> Helper Dataset  </center> </a> ',
    unsafe_allow_html=True)
# Load data
df = EDA.df.sample(50).reset_index(drop=True)
# Show data
st.write(df)