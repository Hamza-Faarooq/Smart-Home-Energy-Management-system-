import paho.mqtt.client as mqtt
from flask import flask, request, jsonify
import sqlite3
import pandas as pd
from sklearn.linear_model import linearregression
import numpy as np

# initialize flask application
app = flask(__name__)

# initialize mqtt client
mqtt_client = mqtt.client()
mqtt_client.connect(“mqtt.eclipse.org”, 1883, 60)

# create sqlite database for storing energy usage data
conn = sqlite3.connect(‘energy_usage.db’)
cursor = conn.cursor()
cursor.execute(‘’’create table if not exists energy_usage (
                    timestamp text,
                    device_id integer,
                    energy_consumption real
                )’’’)
conn.commit()

# route for receiving real-time energy usage data
@app.route(‘/energy_usage’, methods=[‘post’])
def receive_energy_usage():
    # receive energy usage data from iot devices
    data = request.json
    timestamp = data[‘timestamp’]
    device_id = data[‘device_id’]
    energy_consumption = data[‘energy_consumption’]

    # insert data into the database
    cursor.execute(‘’’insert into energy_usage (timestamp, device_id, energy_consumption)
                      values (?, ?, ?)’’’, (timestamp, device_id, energy_consumption))
    conn.commit()

    # publish data to mqtt topic for further processing
    mqtt_client.publish(“energy_usage”, json.dumps(data))

    return jsonify({‘message’: ‘energy usage data received successfully’})

# route for generating energy insights
@app.route(‘/energy_insights’)
def generate_energy_insights():
    # fetch energy usage data from the database
    cursor.execute(‘’’select * from energy_usage’’’)
    rows = cursor.fetchall()
    df = pd.dataframe(rows, columns=[‘timestamp’, ‘device_id’, ‘energy_consumption’])

    # perform data analysis and generate insights
    isights = {}
    for device_id in df[‘device_id’].unique():
        device_data = df[df[‘device_id’] == device_id]
        avg_energy_consumption = device_data[‘energy_consumption’].mean()
        insights[device_id] = avg_energy_consumption

    # perform predictive analysis using linear regression
    x = df[[‘timestamp’]].apply(lambda x: pd.to_numeric(pd.to_datetime(x)))
    y = df[‘energy_consumption’]
    model = linearregression()
    model.fit(x, y)
    future_timestamp = pd.timestamp.now() + pd.timedelta(days=7)
    future_energy_demand = model.predict(np.array([[pd.timestamp.timestamp(future_timestamp)]]))

    return jsonify({‘insights’: insights, ‘future_energy_demand’: future_energy_demand})

# callback function for mqtt message reception
def on_message(client, userdata, msg):
    print(“message received on topic: “ + msg.topic)
    print(“message: “ + str(msg.payload))

# main function to run the flask application and mqtt client
if __name__ == ‘__main__’:
    # set up mqtt client
    mqtt_client.on_message = on_message
    mqtt_client.subscribe(“energy_control”)

    # start mqtt loop in a separate thread
    mqtt_client.loop_start()

    # run flask application
    app.run(debug=true)
