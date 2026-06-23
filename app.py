from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)
ALERT_FILE = "alerts.json"

@app.route('/')
def index():
    """This route serves the main visual dashboard page."""
    return render_template('index.html')

@app.route('/api/alerts')
def get_alerts():
    """This secret route reads alerts.json and returns the data as clean JSON."""
    if not os.path.exists(ALERT_FILE):
        return jsonify([])
    
    try:
        with open(ALERT_FILE, "r") as f:
            alerts = json.load(f)
    except:
        alerts = []
        
    return jsonify(alerts)

if __name__ == '__main__':
    # Starts the web server on your local machine at port 5000
    print("🌐 Web Server Starting... Open http://127.0.0.1:5000 in your browser!")
    app.run(debug=True, host='127.0.0.1', port=5000)


