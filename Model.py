import joblib
import pandas as pd

Airline_list = joblib.load('models/Airline_list.h5')
Origin_Airport_list = joblib.load('models/Origin_Airport_list.h5')
Destination_Airport_list = joblib.load('models/Destination_Airport_list.h5')
inputs=joblib.load('models/input.h5')
pipeline=joblib.load('models/pipeline.h5')

def predict_delay(
        airline, origin_airport, destination_airport, distance,
        day, month, departure_delay, scheduled_time, elapsed_time, airtime,
        taxi_in, taxi_out
        ):
    test_df = pd.DataFrame(columns=inputs)
    test_df.at[0, 'Airline'] = airline
    test_df.at[0, 'Origin_Airport'] = origin_airport
    test_df.at[0, 'Destination_Airport'] = destination_airport
    test_df.at[0, 'Distance'] = distance
    test_df.at[0, 'Day'] = day
    test_df.at[0, 'Month'] = month
    test_df.at[0, 'Departure_Delay'] = departure_delay
    test_df.at[0, 'Scheduled_Time'] = scheduled_time
    test_df.at[0, 'Elapsed_Time'] = elapsed_time
    test_df.at[0, 'Air_Time'] = airtime
    test_df.at[0, 'Taxi_In'] = taxi_in
    test_df.at[0, 'Taxi_Out'] = taxi_out

    result = pipeline.predict(test_df)
    return result

print(inputs)



