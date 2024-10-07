import pandas as pd
import numpy as np
import plotly.express as px

df = pd.read_csv('sources/data/flights_cleaned.csv')
airports_df = pd.read_csv('sources/data/airports.csv')
airlines_df = pd.read_csv('sources/data/airlines.csv')

df['Longitude'] = df.join(airports_df.set_index('IATA_CODE'), on='Origin_Airport')['LONGITUDE']
df['Latitude'] = df.join(airports_df.set_index('IATA_CODE'), on='Origin_Airport')['LATITUDE']
df['City'] = df.join(airports_df.set_index('IATA_CODE'), on='Origin_Airport')['CITY']
df['State'] = df.join(airports_df.set_index('IATA_CODE'), on='Origin_Airport')['STATE']
df['Origin_Airport'] = df.join(airports_df.set_index('IATA_CODE'), on='Origin_Airport')['AIRPORT']
df['Airline'] = df.join(airlines_df.set_index('IATA_CODE'), on='Airline')['AIRLINE']

del airports_df
del airlines_df

# functions for tab 1 (1. Flight Delays and Punctuality)

# 1.1 What is the average Arrival delay for each airline?

def delay_by_airline(df, dim):
    grouped_df = df.groupby('Airline')[dim].mean().reset_index().sort_values(by=dim, ascending=False)
    grouped_df[dim] = grouped_df[dim].round(2)
    fig = px.bar(grouped_df, x='Airline', y=dim, 
                title=f"Average {dim} by Airline",
                labels={dim: f'Average {dim} (minutes)', 'Airline': 'Airline'},
                color=dim,
                color_continuous_scale='Blues')

    fig.update_layout(
        xaxis_title="Airline",
        yaxis_title=f"Average {dim} (minutes)",
        title_x=0.5,
        template="plotly_dark"
    )
    del grouped_df
    return fig

### 1.2 Which airport has the highest average departure or arrival delay?

def delay_by_airport(df, n, dim):
    grouped_df = df.groupby('Origin_Airport')[dim].mean().reset_index().sort_values(by=dim, ascending=False)
    grouped_df[dim] = grouped_df[dim].round(2)

    fig = px.bar(grouped_df.head(n), x='Origin_Airport', y=dim, 
                title=f"Top 10 Average {dim} by Origin_Airport",
                labels={dim: f'Average {dim} (minutes)', 'Origin_Airport': 'Origin_Airport'},
                color=dim,
                color_continuous_scale='Blues')

    fig.update_layout(
        xaxis_title="Origin_Airport",
        yaxis_title=f"Average {dim} (minutes)",
        title_x=0.5,
        template="plotly_dark"
    )

    del grouped_df
    return fig

# 1.3 Delays By Day of week

def delay_by_day(df, dim):
    grouped_df = df.groupby('Day_Of_Week')[dim].mean().reset_index().sort_values(by='Day_Of_Week', ascending=True)
    grouped_df[dim] = grouped_df[dim].round(2)
    grouped_df['Day_Of_Week'] = grouped_df['Day_Of_Week'].map({1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday'})

    # Average Delay by Day of the Week
    fig = px.bar(grouped_df, x='Day_Of_Week', y=dim,
                title=f"{dim} Delay by Day of the Week",
                labels={dim: f'{dim} Delay (minutes)', 'Day_Of_Week': 'Day of the Week'},
                color='Day_Of_Week',
                color_discrete_sequence=['aqua'])

    fig.update_layout(
        xaxis_title="Day of the Week",
        yaxis_title=f"{dim} Delay (minutes)",
        title_x=0.5,
        template="plotly_dark"
    )
    del grouped_df
    return fig

# 1.4 Delays By Hour
def delay_by_hour(df, dim):
    df['Hour'] = df['Scheduled_Departure'].apply(lambda x: x[0:2])
    grouped_df = df.groupby("Hour")[dim].mean().reset_index().sort_values(by='Hour', ascending=True)
    grouped_df['Hour'] = grouped_df['Hour'].astype(int)
    grouped_df[dim] = grouped_df[dim].round(2)
    df.drop('Hour', axis=1, inplace=True)

    fig = px.bar(grouped_df, x='Hour', y=dim, 
             title=f"{dim} by Hour of the Day",
             labels={dim: f'{dim} (minutes)', 'Hour': 'Hour of the Day'},
             color='Hour',
             color_continuous_scale='Cividis')

    fig.update_layout(
    xaxis_title="Hour of the Day",
    yaxis_title=f"{dim} (minutes)",
    title_x=0.5,
    template="plotly_dark"
    )
    del grouped_df
    return fig

### 1.5. What is the distribution of arrival delays
def arrival_delay_distribution(df):
    fig = px.histogram(df, x='Arrival_Delay', nbins=50, 
                    title="Distribution of Arrival Delays",
                    labels={'Arrival_Delay': 'Arrival Delay (minutes)'},
                    color_discrete_sequence=['aqua'])

    fig.update_layout(
        xaxis_title="Arrival Delay (minutes)",
        yaxis_title="Number of Flights",
        title_x=0.5,
        template="plotly_dark"
    )
    return fig

### 1.6. What is the distribution of arrivals ahead of time

def arrival_ahead_distribution(df):
    df_early = df[df['Arrival_Delay'] < 0]
    fig = px.histogram(df_early, x='Arrival_Delay', nbins=30, 
                    title="Flights Arriving Ahead of Schedule",
                    labels={'Arrival_Delay': 'Early Arrival (minutes)'},
                    color_discrete_sequence=['aqua'])

    fig.update_layout(
        xaxis_title="Early Arrival (minutes)",
        yaxis_title="Number of Flights",
        title_x=0.5,
        template="plotly_dark"
    )
    
    del df_early
    return fig

# functions for tab 2 (2. Cancellation)
# 1- What are the most common reasons for flight cancellations ?

def cancellation_reasons(df):
    df['Cancellation_Reason'] = df['Cancellation_Reason'].map({
        'A': 'Airline/Carrier', 
        'B': 'Weather', 
        'C': 'National Air System', 
        'D': 'Security'
    })

    df_cancel_reasons = df['Cancellation_Reason'].value_counts().reset_index()
    df_cancel_reasons.columns = ['Cancellation Reason', 'Count']

    fig = px.pie(df_cancel_reasons, names='Cancellation Reason', values='Count', 
                title="Reasons for Flight Cancellations",
                color_discrete_sequence=['blue', 'green', 'yellow', 'red'])

    fig.update_layout(
        title_x=0.5,
        template="plotly_dark"
    )

    del df_cancel_reasons
    return fig

# 2- Which airlines and airports have the highest cancellation rates ?

def cancellation_by_airport_airline(df, n, dim):
    df_cancel = df.groupby(dim)['Cancelled'].mean().reset_index().sort_values(by='Cancelled', ascending=False).head(n)
    fig = px.bar(df_cancel, x=dim, y='Cancelled', 
                title=f"Cancellation Rates by {dim}",
                labels={'Cancelled': 'Cancellation Rate', 'Airline': 'Airline', 'Origin_Airport': 'Airport'},
                color='Cancelled',
                color_continuous_scale='Blues')

    fig.update_layout(
        xaxis_title=dim,
        yaxis_title="Cancellation Rate",
        title_x=0.5,
        template="plotly_dark"
    )
    
    del df_cancel
    return fig

# 3- Are there any patterns in cancellations or diversions based on the time of year?

def cancellation_by_season(df, dim):
    df_cancel_month = df.groupby('Month')[dim].mean().reset_index()
    fig = px.line(df_cancel_month, x='Month', y=dim, 
                title="Monthly Cancellation/Diversion Rates",
                labels={dim: f'{dim} Rate', 'Month': 'Month'},
                color_discrete_sequence=['aqua'])

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Cancellation Rate",
        title_x=0.5,
        template="plotly_dark"
    )
    del df_cancel_month
    return fig


#functions for tab 3 (Geougraphic Analysis)

# 1 Which airports have the highest volume of flights

def volume_by_airport(df):
    # Count the number of flights from each airport
    df_airport_volume = df['Origin_Airport'].value_counts().reset_index()
    df_airport_volume.columns = ['Origin_Airport', 'Flight_Count']

    # Make sure the correct lat/lon are assigned to corresponding airports
    df_airport_volume[['Latitude', 'Longitude']] = df[['Latitude', 'Longitude']]

    # Add jitter to Latitude and Longitude
    df_airport_volume['Latitude_jitter'] = df_airport_volume['Latitude'] + np.random.normal(0, 1, size=len(df_airport_volume))
    df_airport_volume['Longitude_jitter'] = df_airport_volume['Longitude'] + np.random.normal(0, 1, size=len(df_airport_volume))

    # Create the map with jittered lat/lon
    fig = px.scatter_mapbox(df_airport_volume, lat='Latitude_jitter', lon='Longitude_jitter', 
                            size='Flight_Count',  # Vary size based on flight count
                            color='Flight_Count',  # Vary color based on flight count
                            hover_name='Origin_Airport',
                            title="Geographic Distribution of Flights by Airport",
                            labels={'Flight_Count': 'Number of Flights'},
                            color_continuous_scale='Turbo',
                            zoom=3)

    # Customize the layout and background
    fig.update_layout(
        mapbox_style="open-street-map",  
        mapbox_center={"lat": 37.0902, "lon": -95.7129},  
        title_x=0.5,
        paper_bgcolor='rgba(0,0,0,0)',  
        plot_bgcolor='rgba(0,0,0,0)',   
    )

    del df_airport_volume
    return fig

# 2 Which states or cities experience the most delays or cancellations?

def volume_by_state(df):
    df_state_delay = df.groupby('State')['Arrival_Delay'].mean().reset_index()

    # Create the choropleth map
    fig = px.choropleth(
        df_state_delay,
        locations='State',
        locationmode='USA-states',
        color='Arrival_Delay',
        scope='usa',
        title="Average Arrival Delay by State",
        labels={'Arrival_Delay': 'Average Arrival Delay (minutes)'},
        color_continuous_scale='Blues'
    )

    # Update the layout to fix the black box and enhance visibility
    fig.update_layout(
        title_x=0.5,
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',    # Transparent figure background
        plot_bgcolor='rgba(0,0,0,0)',     # Transparent plot background
        geo=dict(
            scope='usa',
            bgcolor='rgba(0,0,0,0)',      # Transparent geo background
            lakecolor='LightBlue',        # Optional: Set lake color
            landcolor='rgba(0,0,0,0)',    # Transparent land color or set to a specific color
            showlakes=True,
            showcountries=False,
            showcoastlines=False
        ),
        legend=dict(
            font=dict(color="white"),      # Legend text color
            bgcolor='rgba(0,0,0,0)'        # Transparent legend background
        ),
        title_font=dict(color='white')      # Title font color
    )

    # Update hover label styling
    fig.update_traces(
        hoverlabel=dict(
            bgcolor="white",
            font_color="black"
        )
    )

    del df_state_delay
    return fig

# 3 Are there any patterns in delays or cancellations based on the geographic location of airports?

def delay_by_airport_location(df):
    grouped_df = df.groupby('Origin_Airport')[['Arrival_Delay', 'Latitude', 'Longitude']].mean().reset_index().sort_values(by='Arrival_Delay', ascending=False)


    fig = px.scatter_mapbox(grouped_df, lat='Latitude', lon='Longitude', 
                            color='Arrival_Delay',
                            hover_name='Origin_Airport',
                            title="Geographic Distribution of Delays by Airport",
                            labels={'Arrival_Delay': 'Average Arrival Delay (minutes)'},
                            color_continuous_scale='Turbo',
                            zoom=3)

    fig.update_traces(marker=dict(size=15))
    fig.update_layout(
        mapbox_style="open-street-map",  
        mapbox_center={"lat": 37.0902, "lon": -95.7129},  
        title_x=0.5,
        paper_bgcolor='rgba(0,0,0,0)',  # Set the background of the whole figure to transparent
        plot_bgcolor='rgba(0,0,0,0)',   # Set the plot area background to transparent
    )

    del grouped_df
    return fig


# functions for tab 4 (Time based Analysis)
# 1 Which days of the week have the most frequent delays ?

def delay_by_day_time(df):
    df_day_delay = df.groupby('Day_Of_Week')[['Departure_Delay', 'Arrival_Delay']].mean().reset_index()

    fig = px.line(df_day_delay, x='Day_Of_Week', y=['Departure_Delay', 'Arrival_Delay'], 
                title="Average Delays by Day of the Week",
                labels={'value': 'Average Delay (minutes)', 'Day_Of_Week': 'Day of the Week'},
                markers=True,
                color_discrete_sequence=['aqua', 'blue']
                )

    fig.update_layout(
        xaxis_title="Day of the Week",
        yaxis_title="Average Delay (minutes)",
        title_x=0.5,
        template="plotly_dark",
    )

    del df_day_delay
    return fig

# 2 Which days of the week have the most frequent cancellations ?

def cancellation_by_day(df):
    df_day_cancel = df.groupby('Day_Of_Week')['Cancelled'].mean().reset_index()

    fig = px.bar(df_day_cancel, x='Day_Of_Week', y='Cancelled', 
                title="Cancellation Rates by Day of the Week",
                labels={'Cancelled': 'Cancellation Rate', 'Day_Of_Week': 'Day of the Week'},
                color='Cancelled',
                color_continuous_scale='Blues')

    fig.update_layout(
        xaxis_title="Day of the Week",
        yaxis_title="Cancellation Rate",
        title_x=0.5,
        template="plotly_dark"
    )

    del df_day_cancel
    return fig

# 3 How does the time of day impact departure and arrival delays ?

def delay_by_hour_line(df):
    df['Hour'] = df['Scheduled_Arrival'].apply(lambda x: str(x[0:2]).strip()).astype(int)
    df_hour_delay = df.groupby('Hour')[['Departure_Delay', 'Arrival_Delay']].mean().reset_index()
    df_hour_delay.drop(df_hour_delay[df_hour_delay['Hour'] == 24].index, inplace=True)

    fig = px.line(df_hour_delay, x='Hour', y=['Departure_Delay', 'Arrival_Delay'], 
                title="Average Delays by Hour of the Day",
                labels={'value': 'Average Delay (minutes)', 'Hour': 'Hour of the Day'},
                markers=True,
                color_discrete_sequence=['aqua', 'blue']
                )

    fig.update_layout(
        xaxis_title="Hour of the Day",
        yaxis_title="Average Delay (minutes)",
        title_x=0.5,
        template="plotly_dark"
    )

    del df_hour_delay
    return fig

# 4 Is there a specific time during the day when flights are more likely to be on time or delayed?

def delay_by_season(df):
    
    df['On_Time'] = df['Arrival_Delay'] <= 0
    df_on_time_rate = df.groupby('Hour')['On_Time'].mean().reset_index()
    df_on_time_rate.drop(df_on_time_rate[df_on_time_rate['Hour'] == 24].index, inplace=True)

    fig = px.line(df_on_time_rate, x='Hour', y='On_Time', 
                title="On-Time Performance by Hour of the Day",
                labels={'On_Time': 'On-Time Rate', 'Hour': 'Hour of the Day'},
                markers=True,
                color_discrete_sequence=['aqua'])

    fig.update_layout(
        xaxis_title="Hour of the Day",
        yaxis_title="On-Time Rate",
        title_x=0.5,
        template="plotly_dark"
    )
    
    del df_on_time_rate
    return fig


# functions for tab 5 (Airline Analysis)
# 1 Which airline has the best overall on-time performance?

def on_time_by_airline(df):
    df['On_Time'] = df['Arrival_Delay'] <= 0
    grouped_df = df.groupby('Airline')['On_Time'].aggregate(['sum', 'count']).reset_index()
    grouped_df['On_Time_Percentage'] = (grouped_df['sum'] / grouped_df['count']) * 100

    fig = px.histogram(grouped_df.sort_values(by='On_Time_Percentage', ascending=False), x='Airline', y='On_Time_Percentage', 
                    title="On-Time Performance by Airline",
                    labels={'On_Time': 'On-Time Arrival', 'Airline': 'Airline'},
                    color='Airline',
                    color_discrete_sequence=['aqua'])

    fig.update_layout(
        xaxis_title="Airline",
        yaxis_title="Number of Flights",
        title_x=0.5,
        template="plotly_dark"
    )

    del grouped_df
    return fig

# 2 What are the average air time and elapsed time for each airline?

def air_time_by_airline(df):
    df_airline_time = df.groupby('Airline')[['Air_Time', 'Elapsed_Time']].mean().reset_index()
    fig = px.bar(df_airline_time, x='Airline', y=['Air_Time', 'Elapsed_Time'], 
                title="Average Air Time and Elapsed Time by Airline",
                labels={'value': 'Time (minutes)', 'variable': 'Time Metric', 'Airline': 'Airline'},
                barmode='group',
                color_discrete_sequence=['blue', 'aqua'])

    fig.update_layout(
        xaxis_title="Airline",
        yaxis_title="Time (minutes)",
        title_x=0.5,
        template="plotly_dark"
    )

    del df_airline_time
    return fig

# functions for tab 6 (Airport Analysis)

# 1 Which airports have the highest volume of flights

def volume_by_airport_analysis(df):
    df_airport_volume = df['Origin_Airport'].value_counts().reset_index().head(10)
    df_airport_volume.columns = ['Origin_Airport', 'Flight Count']

    fig = px.bar(df_airport_volume, x='Origin_Airport', y='Flight Count', 
                title="Flight Volume by Airport",
                labels={'Flight Count': 'Number of Flights', 'Origin_Airport': 'Airport'},
                color='Flight Count',
                color_continuous_scale='Blues')

    fig.update_layout(
        xaxis_title="Airport",
        yaxis_title="Number of Flights",
        title_x=0.5,
        template="plotly_dark"
    )
    del df_airport_volume
    return fig


# 2 What is the average taxi time (out and in) for each airport

def taxi_time_by_airport(df):
    df_airport_taxi = df.groupby('Origin_Airport')[['Taxi_Out', 'Taxi_In', 'Arrival_Delay']].mean().reset_index()
    df_airport_taxi['Total_Taxi'] = df_airport_taxi['Taxi_Out'] + df_airport_taxi['Taxi_In']
    fig = px.bar(df_airport_taxi.sort_values(by='Total_Taxi', ascending=False).head(10), x='Origin_Airport', y="Total_Taxi", 
                title="Average Taxi Time by Airport",
                labels={'value': 'Taxi Time (minutes)', 'variable': 'Taxi Metric', 'Origin_Airport': 'Airport'},
                color='Total_Taxi',
                color_continuous_scale='blues')

    fig.update_layout(
        xaxis_title="Airport",
        yaxis_title="Taxi Time (minutes)",
        title_x=0.5,
        template="plotly_dark"
    )

    del df_airport_taxi
    return fig

