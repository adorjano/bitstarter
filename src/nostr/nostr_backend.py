from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Aktivieren Sie CORS für alle Ressourcen

cards = [
    {
        "name": "Eco-friendly City",
        "subtitle": "A vision for a greener urban environment",
        "message": "Let's build a city with more parks, green rooftops, and eco-friendly transportation.",
        "bannerImage": "https://as1.ftcdn.net/v2/jpg/04/48/29/76/1000_F_448297652_sYW6YiBR2RXxzjkHCEhgdQSrHOQBuUkf.jpg",
    },
    {
        "name": "Zero Waste Lifestyle",
        "subtitle": "Reducing our footprint one step at a time",
        "message": "Join the movement to eliminate single-use plastics and adopt sustainable practices.",
        "bannerImage": "https://as1.ftcdn.net/v2/jpg/02/68/81/22/1000_F_268812279_cVMsQJ8UWfV8k8HO2oqjhRY1XhopgE68.jpg",
    },
    # ...
]

@app.route('/cards', methods=['GET'])
def get_cards():
    return jsonify(cards)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
