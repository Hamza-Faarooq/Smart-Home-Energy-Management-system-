from sklearn.model_selection import train_test_split
from sklearn.linear_model import linearregression
import numpy as np

# route for generating energy insights
@app.route(‘/energy_insights’)
def generate_energy_insights():
    try:
        # fetch energy usage data from the database
        cursor.execute(‘’’select * from energy_usage’’’)
        rows = cursor.fetchall()
        df = pd.dataframe(rows, columns=[‘timestamp’, ‘device_id’, ‘energy_consumption’])

        # prepare data for model training
        x = df[[‘timestamp’]].apply(lambda x: pd.to_numeric(pd.to_datetime(x)))
        y = df[‘energy_consumption’]

        # split the data into training and testing sets
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

        # train the linear regression model
        model = linearregression()
        model.fit(x_train, y_train)

        # predict future energy demand
        future_timestamp = pd.timestamp.now() + pd.timedelta(days=7)
        future_energy_demand = model.predict(np.array([[pd.timestamp.timestamp(future_timestamp)]]))

        return jsonify({‘future_energy_demand’: future_energy_demand}), 200
    except exception as e:
        return jsonify({‘error’: ‘failed to generate energy insights’, ‘details’: str€}), 500
