from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from flask_cors import CORS  # Import CORS from flask_cors
import io
import base64

app = Flask(__name__)
CORS(app)  # Add CORS support to your Flask app

# Load the data and preprocess it
df = pd.read_csv(r'df.csv')
df['Offence_From_Date'] = pd.to_datetime(df['Offence_From_Date'])
df['Year'] = df['Offence_From_Date'].dt.year
df['Month'] = df['Offence_From_Date'].dt.month
df['Day'] = df['Offence_From_Date'].dt.day
df['Hour'] = df['Offence_From_Date'].dt.hour
print(df.head())

@app.route('/')
def index():
    return render_template('input.html')

@app.route('/predict', methods=['POST'])
def predict():
    
    month = int(request.form['month'])
    day = int(request.form['day'])
    category = request.form['category']

    category_df = df[df['CrimeGroup_Name'] == category]
    print(category_df.head())

    # Train model
    dftest1_month = pd.DataFrame(category_df['Month'].value_counts()).reset_index()
    dftest1_day = pd.DataFrame(category_df['Day'].value_counts()).reset_index()
    dftest1_hour = pd.DataFrame(category_df['Hour'].value_counts()).reset_index()

    model = LinearRegression()
    dftest1_year_train = pd.DataFrame(category_df['Year'].value_counts()).iloc[1:9, :].reset_index()
    print(dftest1_year_train.columns)
    print(dftest1_year_train.info())
    # print()
    model.fit(dftest1_year_train[['Year']], dftest1_year_train['Year'])

    predicted_value = model.predict([[2024]])

    # Generate prediction based on inputs
    value = np.zeros(24)
    for x in range(24):
        value[x] = predicted_value * (dftest1_month.loc[month, 'Month'] / dftest1_month['Month'].sum()) * \
                    (dftest1_day.iloc[day - 1]['Day'] / dftest1_day['Day'].sum()) * \
                    (dftest1_hour.loc[x, 'Hour'] / dftest1_hour['Hour'].sum())

    # Plot graph
    plt.bar(range(len(value)), value)
    plt.xlabel('Hour')
    plt.ylabel('Probability')
    plt.title('Crime distribution for given day and hour')

    # Convert plot to base64 encoded image
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.getvalue()).decode()

    plt.close()

    # Return HTML content with embedded image
    html_content = f"""
    <div>
        <h1>Prediction Result</h1>
        <img src="data:image/png;base64,{plot_data}" alt="Crime Distribution">
    </div>
    """ 
    return html_content
    # except Exception as e:
    #     return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
