# importing necessary libraries
import streamlit as st
import numpy as np
import pandas as pd

# Page content
st.markdown(" <center>  <h1> Flight Delays Analysis </h1> </font> </center> </h1> ",
            unsafe_allow_html=True)

st.markdown(''' <center>  <h6>
    This app is created to analyze abd predict flight delays </center> </h6> ''', unsafe_allow_html=True)

# the path of a photo provided from the path of this file
st.image('sources/images/airplane.jpg')
