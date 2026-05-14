import pickle

def predict_delivery_time(distance, weight):
    """Calculate delivery time using Eco-Formula"""
    return 0.5 + (distance * 0.2) + (weight * 0.1)

# Save the function using pickle
with open('delivery_model.pkl', 'wb') as f:
    pickle.dump(predict_delivery_time, f)

print("delivery_model.pkl created successfully!")
print(f"File saved at: delivery_model.pkl")
print("You can now commit this file to GitHub")