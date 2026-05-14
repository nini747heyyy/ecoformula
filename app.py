from flask import Flask, request, jsonify
import pickle
import os
import sys

app = Flask(__name__)

# Define the prediction function
def predict_delivery_time(distance, weight):
    """Calculate delivery time using Eco-Formula"""
    return 0.5 + (distance * 0.2) + (weight * 0.1)

# Load model with multiple fallback strategies
loaded_model = None

# Try to load from pickle file
if os.path.exists('delivery_model.pkl'):
    try:
        with open('delivery_model.pkl', 'rb') as f:
            loaded_model = pickle.load(f)
        print("✓ Model loaded from delivery_model.pkl")
    except Exception as e:
        print(f"⚠ Could not load pickle: {e}")
        loaded_model = predict_delivery_time
else:
    print("⚠ delivery_model.pkl not found, using local function")
    loaded_model = predict_delivery_time

# Final fallback
if loaded_model is None:
    loaded_model = predict_delivery_time

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        distance = float(data.get('distance', 0))
        weight = float(data.get('weight', 0))
        
        if distance < 0 or weight < 0:
            return jsonify({'error': 'Distance and weight must be non-negative'}), 400
        
        # Calculate delivery time
        delivery_time = loaded_model(distance, weight)
        
        return jsonify({
            'distance_km': distance,
            'weight_kg': weight,
            'delivery_time_hours': round(delivery_time, 2),
            'formula': '0.5 + (distance × 0.2) + (weight × 0.1)',
            'calculation': f'0.5 + ({distance} × 0.2) + ({weight} × 0.1) = {delivery_time}'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'EcoFormula Delivery Time Estimator',
        'status': 'running',
        'python_version': sys.version,
        'endpoint': 'POST /predict',
        'example': {'distance': 10, 'weight': 5}
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'pickle_exists': os.path.exists('delivery_model.pkl'),
        'model_loaded': loaded_model is not None
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
