# import needed libraries
import sys
sys.path.append("../")

import streamlit as st
import EDA
from EDA import df

tab_delays, tab_cancellations, tab_geographic,  tab_time, tab_airlines, tab_airports = st.tabs(
    ['Flight Delays', 'Cancellations and Diversions', 'Geographic Analysis', 'Time-Based Analysis', 'Airline Analysis', 'Airport Analysis'])

with tab_delays:
    # Title of tab
    st.title("Flight Delays")

    # insights in this tab
    st.write("This tab answers the following questions:")
    st.write("    1- What is the average Arrival delay for each airline ?")
    st.write("    2- Which airport has the highest average departure or arrival delay ?")
    st.write("    3- How do delays vary based on the day of the week ?")
    st.write("    4- How do delays vary based on the time of day ?")
    st.write("    5- What is the distribution of arrival delays ?")
    st.write("    6- What is the distribution of arrivals ahead of time ?")

    st.header("1- What is the average Arrival delay for each airline ?")
    cont = st.container()

    with cont:
        dim = st.radio(
            "Select Dimension",
            ("Arrival_Delay", "Departure_Delay"),
            index=1,
            key=1,
            horizontal=True
        )
    st.plotly_chart(EDA.delay_by_airline(df, dim))

    st.header("2- Which airport has the highest average departure or arrival delay ?")

    cont = st.container()
    cont1, cont2 = st.columns(2)
    with cont1:
        n = int(st.number_input(
            "Number of Airports",
            min_value=5,
            max_value=30,
            value=10,
            step=1,
            key=2
            ))
    with cont2:
        dim = st.radio(
            "Select Dimension",
            ("Arrival_Delay", "Departure_Delay"),
            index=1,
            key=3,
            horizontal=True
        )
    st.plotly_chart(EDA.delay_by_airport(df, n, dim))

    st.header("3- How do delays vary based on the day of the week ?")

    cont = st.container()
    with cont:
        dim = st.radio(
            "Select Dimension",
            ("Arrival_Delay", "Departure_Delay"),
            index=1,
            key=4,
            horizontal=True
        )

    st.plotly_chart(EDA.delay_by_day(df, dim))

    st.header("4- How do delays vary based on the time of day ?")

    cont = st.container()
    with cont:
        dim = st.radio(
            "Select Dimension",
            ("Arrival_Delay", "Departure_Delay"),
            index=1,
            key=5,
            horizontal=True
        )

    st.plotly_chart(EDA.delay_by_hour(df, dim))

    st.header("5- What is the distribution of arrival delays?")

    st.plotly_chart(EDA.arrival_delay_distribution(df))

    st.header("6- What is the distribution of arrivals ahead of time?")

    st.plotly_chart(EDA.arrival_ahead_distribution(df))


with tab_cancellations:
    st.title("Cancellations and Diversions")

    st.write("This tab answers the following questions:")
    st.write("    1- What are the most common reasons for flight cancellations ?")
    st.write("    2- Which airlines and airports have the highest cancellation rates ?")
    st.write("    3- Are there any patterns in cancellations or diversions based on the time of year?")

    st.header("1- What are the most common reasons for flight cancellations ?")

    st.plotly_chart(EDA.cancellation_reasons(df))

    st.header("2- Which airlines and airports have the highest cancellation rates ?")

    cont = st.container()
    with cont:
        n = int(st.number_input(
            f"Number of {dim}s",
            min_value=5,
            max_value=30,
            value=10,
            step=1,
            key=6
        ))
        dim = st.radio(
            "Select Dimension",
            ("Origin_Airport", "Airline"),
            index=1,
            key=7,
            horizontal=True
        )

    st.plotly_chart(EDA.cancellation_by_airport_airline(df, n, dim))

    st.header("3- Are there any patterns in cancellations or diversions based on the time of year?")

    cont = st.container()
    with cont:
        dim = st.radio(
            "Select Dimension",
            ("Cancelled", "Diverted"),
            index=1,
            key=8,
            horizontal=True
        )

    st.plotly_chart(EDA.cancellation_by_season(df, dim))


with tab_geographic:
    st.title("Geographic Analysis")

    st.write("This tab answers the following questions:")
    st.write("    1- Which airports have the highest volume of flights ?")
    st.write("    2- Which states or cities experience the most delays or cancellations ?")
    st.write("    3- Are there any patterns in delays based on the geographic location of airports?")

    st.header("1- Which airports have the highest volume of flights ?")

    st.plotly_chart(EDA.volume_by_airport(df))

    st.header("2- Which states or cities experience the most delays or cancellations ?")

    st.plotly_chart(EDA.volume_by_state(df))

    st.header("3- Are there any patterns in delays based on the geographic location of airports?")

    st.plotly_chart(EDA.delay_by_airport_location(df))


with tab_time:
    st.title("Time-Based Analysis")

    st.write("This tab answers the following questions:")
    st.write("    1- Which days of the week have the most frequent delays ?")
    st.write("    2- Which days of the week have the most frequent cancellations ?")
    st.write("    3- Are there any patterns in delays or cancellations based on the geographic location of airports?")
    st.write("    4- Are there any patterns in delays or cancellations based on the time of year?")

    st.header("1- Which days of the week have the most frequent delays ?")

    st.plotly_chart(EDA.delay_by_day_time(df))

    st.header("2- Which days of the week have the most frequent cancellations ?")

    st.plotly_chart(EDA.cancellation_by_day(df))

    st.header("3- Are there any patterns in delays or cancellations based on the geographic location of airports?")

    st.plotly_chart(EDA.delay_by_hour_line(df))

    st.header("4- Are there any patterns in delays or cancellations based on the time of year?")

    st.plotly_chart(EDA.delay_by_season(df))


with tab_airlines:
    st.title("Airline Analysis")

    st.write("This tab answers the following questions:")
    st.write("    1- Which airline has the best overall on-time performance ?")
    st.write("    2- What are the average air time and elapsed time for each airline ?")

    st.header("1- Which airline has the best overall on-time performance ?")

    st.plotly_chart(EDA.on_time_by_airline(df))

    st.header("2- What are the average air time and elapsed time for each airline ?")

    st.plotly_chart(EDA.air_time_by_airline(df))


with tab_airports:
    st.title("Airport Analysis")

    st.write("This tab answers the following questions:")
    st.write("    1- Which airports have the highest volume of flights ?")
    st.write("    2- What is the average taxi time (out and in) for each airport ?")

    st.header("1- Which airports have the highest volume of flights ?")

    st.plotly_chart(EDA.volume_by_airport_analysis(df))

    st.header("2- What is the average taxi time (out and in) for each airport ?")

    st.plotly_chart(EDA.taxi_time_by_airport(df))




