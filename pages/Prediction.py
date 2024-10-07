import streamlit as st
import Model
import sys
sys.path.append('../')

st.title('Flight Delay Prediction')
st.write('Enter the details to predict the flight delay')

# Add a selectbox to the sidebar:
airline = st.selectbox('Airline', Model.Airline_list)
origin_airport = st.selectbox('Origin Airport', Model.Origin_Airport_list)
destination_airport = st.selectbox('Destination Airport', Model.Destination_Airport_list)
distance = st.number_input('Distance', min_value=1, max_value=5000)
day = st.number_input('Day', min_value=1, max_value=31)
month = st.number_input('Month', min_value=1, max_value=12)
departure_delay = st.number_input('Departure Delay (Minutes)', step=1)
scheduled_time = st.number_input('Scheduled Time (Minutes)', step=1, min_value=0)
elapsed_time = st.number_input('Elapsed Time (Minutes)', step=1, min_value=0)
airtime = st.number_input('Airtime (Minutes)', step=1, min_value=0)
taxi_in = st.number_input('Taxi In (Minutes)', step=1, )
taxi_out = st.number_input('Taxi Out (Minutes)', step=1)

if st.button('Predict'):
    result = Model.predict_delay(airline, origin_airport, destination_airport, distance, day, month, departure_delay, scheduled_time, elapsed_time, airtime, taxi_in, taxi_out)
    st.success('The predicted flight delay is {}'.format(result))
