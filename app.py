from flask import Flask, jsonify, request

# Create the Flask app instance
app = Flask(__name__)

# --- TEMPORARY SAMPLE DATA ---
# This dictionary represents the data you will eventually get from Member C's script.
sample_data = {
  "location": "AuraCast Default Location",
  "current_aqi": 75,
  "last_updated": "2025-10-04T18:00:00Z",
  "forecast_24hr": [
    {"hour": i, "aqi": 75 + (i % 5), "pollutant": "PM2.5"} 
    for i in range(24)
  ],
  "validation": {
    "satellite_reading": 82,
    "ground_sensor_reading": 78
  }
}

# 1. Define the main route (simple health check)
@app.route('/')
def home():
    """Returns a simple greeting to confirm the server is running."""
    return "AuraCast Backend API is running! Access forecast data at /api/forecast"

# 2. Define the working API endpoint for the forecast
@app.route('/api/forecast', methods=['GET'])
def get_forecast():
    """
    Handles GET requests to /api/forecast. 
    Currently returns temporary sample data. 
    In the final app, this will call the forecasting script.
    """
    # Later, you will get the location from the request arguments, like this:
    # location = request.args.get('location', 'default_location')
    
    # Return the dictionary converted to JSON format
    return jsonify(sample_data)

# 3. Run the server
if __name__ == '__main__':
    # Running with debug=True allows the server to automatically reload when you save changes.
    app.run(debug=True)
