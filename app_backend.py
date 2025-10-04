# app_backend.py
from flask import Flask, jsonify, request, render_template
import pickle
import numpy as np
import pandas as pd
import os
from model_forecast import pm25_to_aqi_level # Import the helper function from the model script

# --- Configuration ---

# 1. Define the project root directory (D:\gryffinCoders)
# os.path.dirname(__file__) is the script folder. We use '..' to go one level up.
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# 2. Use the absolute path for file loading
MODEL_FILE = os.path.join(ROOT_DIR, 'model', 'air_quality_model.pkl')
MASTER_FILE = os.path.join(ROOT_DIR, 'data_processed', 'master_data_for_model.csv')

# 3. Explicitly define the template folder path (D:\gryffinCoders\templates)
template_dir = os.path.join(ROOT_DIR, 'templates')

app = Flask(__name__, template_folder=template_dir)

df_master = None
model = None

# Load the model and data when the server starts
def load_resources():
    """Loads the trained model and the master data for the API to use."""
    global model, df_master
    try:
        # 1. Load the trained model using the absolute path
        with open(MODEL_FILE, 'rb') as file:
            model = pickle.load(file)
        # 2. Load the master data file using the absolute path
        df_master = pd.read_csv(MASTER_FILE)
        print("Resources loaded: Model and Master Data Ready.")
    except Exception as e:
        print(f"CRITICAL ERROR: Failed to load resources. Path check:\nModel Path: {MODEL_FILE}\nMaster Data Path: {MASTER_FILE}\nError: {e}")
        model = None
        df_master = None
        print("Ensure 'model_forecast.py' was run successfully and files exist at the paths above.")

# ----------------------------------------------------
# --- API ROUTES ---
# ----------------------------------------------------

@app.route('/')
def index():
    """Serves the main HTML page for the frontend."""
    return render_template('index.html')

@app.route('/api/forecast', methods=['GET'])
def get_forecast():
    """
    API endpoint to get the predicted PM2.5 and AQI level for a location.
    """
    if model is None or df_master is None:
        return jsonify({"error": "Server not ready (model/data missing). Check terminal logs."}), 500
        
    # Get the last data point's features for a quick demonstration
    last_row = df_master.tail(1)
    
    # Extract the features used by the model
    features = last_row[[
        'NO2_column_density', 
        'current_temp_C', 
        'current_wind_speed_m_s', 
        'current_wind_direction_deg'
    ]].values
    
    if len(features) == 0:
        return jsonify({"error": "No valid data to generate prediction."}), 500
    
    # Predict PM2.5
    predicted_pm25 = model.predict(features)[0]
    predicted_pm25 = max(0, predicted_pm25) # Ensure prediction is not negative

    # Convert to AQI level
    aqi_data = pm25_to_aqi_level(predicted_pm25)

    return jsonify({
        "status": "success",
        "predicted_pm25": round(predicted_pm25, 2),
        "aqi_level": aqi_data["level"],
        "aqi_color": aqi_data["color"],
        "location_context": "Prediction based on the model's features from last data record." 
    })

@app.route('/api/validation', methods=['GET'])
def get_validation_data():
    """
    API endpoint to show recent data for validation/transparency.
    """
    if df_master is None:
        return jsonify({"error": "Server not ready (model/data missing)."}), 500

    # Get the last 10 rows for recent data comparison
    recent_data = df_master.tail(10).to_dict(orient='records')

    # Extract the key fields needed for the validation view
    validation_list = []
    for row in recent_data:
        validation_list.append({
            "timestamp": row['datetime'],
            "satellite_no2": round(row.get('NO2_column_density', np.nan), 4),
            "ground_pm25": round(row.get('nearest_openaq_pm25', np.nan), 2),
            "distance_km": round(row.get('distance_km_to_openaq', np.nan), 1)
        })

    return jsonify({
        "status": "success",
        "recent_validation_data": validation_list
    })

if __name__ == '__main__':
    load_resources()
    print("\n--- Flask Server Starting ---")
    app.run(debug=True)