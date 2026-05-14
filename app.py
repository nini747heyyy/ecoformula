from flask import Flask, request, jsonify
import pickle
import os

app = Flask(__name__)

# Define the prediction function
def predict_delivery_time(distance, weight):
    """Calculate delivery time using Eco-Formula"""
    return 0.5 + (distance * 0.2) + (weight * 0.1)

# Load the pickle model
loaded_model = None
model_path = 'delivery_model.pkl'

if os.path.exists(model_path):
    try:
        with open(model_path, 'rb') as f:
            loaded_model = pickle.load(f)
        print(f"✓ Model loaded from {model_path}")
    except Exception as e:
        print(f"⚠ Could not load pickle: {e}")
        loaded_model = predict_delivery_time
else:
    print(f"⚠ {model_path} not found, using local function")
    loaded_model = predict_delivery_time

# This is the PREDICT endpoint - make sure it's exactly this
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Extract distance and weight
        distance = float(data.get('distance', 0))
        weight = float(data.get('weight', 0))
        
        # Validate inputs
        if distance < 0 or weight < 0:
            return jsonify({'error': 'Distance and weight must be non-negative'}), 400
        
        # Calculate delivery time
        delivery_time = loaded_model(distance, weight)
        
        # Return response
        return jsonify({
            'distance_km': distance,
            'weight_kg': weight,
            'delivery_time_hours': round(delivery_time, 2),
            'formula': '0.5 + (distance × 0.2) + (weight × 0.1)',
            'calculation': f'0.5 + ({distance} × 0.2) + ({weight} × 0.1) = {delivery_time}'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Home endpoint
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'EcoFormula Delivery Time Estimator API',
        'endpoints': {
            'POST /predict': 'Calculate delivery time',
            'GET /health': 'Check service health'
        },
        'example': {
            'url': 'https://ecoformula.onrender.com/predict',
            'method': 'POST',
            'body': {'distance': 10, 'weight': 5}
        }
    })

# Health check endpoint
@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'model_loaded': loaded_model is not None,
        'pickle_exists': os.path.exists('delivery_model.pkl')
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
