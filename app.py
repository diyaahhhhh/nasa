from flask import Flask, jsonify
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "<h1>AuraCast API is Running!</h1><p>Visit /get_alert, /get_validation, or /get_map_data to see API data.</p>"

@app.route('/get_alert', methods=['GET'])
def get_alert_status():
    
    forecast_aqi = 118
    user_alert_threshold = 101
    
    if forecast_aqi <= 50:
        status = "Good"
        message = "Air Quality is Good. Enjoy the outdoors!"
        action = "No restrictions needed." 

    elif forecast_aqi <= 100:
        status = "Moderate"
        message = "Air Quality is Moderate."
        action = "Unusually sensitive people should consider limiting long outdoor time."

    elif forecast_aqi < 150: 
        status = "Unhealthy for Sensitive Groups"
        message = f"🚨 AQI Alert: {forecast_aqi}. Air is UNHEALTHY for sensitive groups."
        action = "Limit prolonged or heavy exertion outdoors."
    
    else:
        status = "Unhealthy or Worse"
        message = f"🛑 WARNING: AQI {forecast_aqi} is high. Health risk is elevated."
        action = "Everyone should avoid outdoor exertion."

    return jsonify({
        "aqi_value": forecast_aqi,
        "aqi_status": status,
        "alert_title": message,
        "recommended_action": action,
        "threshold_checked": user_alert_threshold
    })

@app.route('/get_validation', methods=['GET']) 
def get_validation_data():
    satellite_no2 = 15.5
    ground_no2 = 14.8
    difference = satellite_no2 - ground_no2
    
    if ground_no2 == 0:
        percent_difference = 0
    else:
        percent_difference = (abs(difference) / ground_no2) * 100

    if difference > 0:
        trend = "higher"
    else:
        trend = "lower"
        
    validation_text = (
        f"The TEMPO satellite reading is {percent_difference:.1f}% {trend} "
        f"than the closest ground sensor."
    )

    return jsonify({
        "satellite_value": satellite_no2,
        "ground_value": ground_no2,
        "difference_percent": f"{percent_difference:.1f}%",
        "validation_message": validation_text
    })

@app.route('/get_map_data', methods=['GET'])
def get_map_data():
    mock_data = [
        [40.78, -73.96, 125, 'forecast'], 
        [40.71, -74.01, 85, 'forecast'],  
        [40.69, -73.98, 45, 'forecast'],  
        [40.82, -73.94, 180, 'forecast']  
    ]
    return jsonify(mock_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
