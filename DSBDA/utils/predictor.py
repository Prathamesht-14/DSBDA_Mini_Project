import os
import joblib

def load_model(model_path):
    if os.path.exists(model_path):
        try:
            return joblib.load(model_path)
        except Exception:
            return None
    return None

def predict(model, region, category, sales_value):
    # This is a placeholder since we don't have the exact features of the model yet.
    # We apply a dummy logic to return a value, but ideally we would encode features
    # and use model.predict(X).
    if model is not None:
        try:
            # E.g., prediction = model.predict([[encoded_region, encoded_category, sales_value]])
            pass
        except:
            pass
            
    # Dummy mock prediction
    base_pred = sales_value * 1.15
    if region == 'West':
        base_pred *= 1.2
    
    return round(base_pred, 2)
