import pickle
import numpy as np

# Define the prediction function
def predict_delivery_time(distance, weight):
    """Calculate delivery time using Eco-Formula"""
    return 0.5 + (distance * 0.2) + (weight * 0.1)

# Save the function using pickle
with open('delivery_model.pkl', 'wb') as f:
    pickle.dump(predict_delivery_time, f)

print("Model saved as delivery_model.pkl")
