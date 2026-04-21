import os
import joblib
import pandas as pd
import json
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

def train_model(df, model_path, metrics_path):
    """
    Trains a Linear Regression model on the dataset and saves it along with metrics.
    """
    if df is None or df.empty:
        return None
        
    # Select features and target
    # We'll predict 'sales' based on 'region' and 'category' for this demonstration
    # In a more complex scenario, we could use date features, etc.
    required_cols = ['region', 'category', 'sales']
    if not all(col in df.columns for col in required_cols):
        return None
        
    X = df[['region', 'category']]
    y = df['sales']
    
    # Preprocessing: One-hot encode the categorical variables
    categorical_features = ['region', 'category']
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])
        
    # Create a pipeline
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', LinearRegression())
    ])
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    
    # Save model
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)
    
    # Save metrics
    metrics = {
        'r2_score': round(float(r2), 4),
        'mae': round(float(mae), 2)
    }
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f)
        
    return metrics

def load_model(model_path):
    if os.path.exists(model_path):
        try:
            return joblib.load(model_path)
        except Exception:
            return None
    return None

def predict(model, region, category, sales_value):
    """
    Predicts using the trained model or falls back to dummy logic if no model exists.
    """
    if model is not None:
        try:
            # Create a dataframe for the input
            input_df = pd.DataFrame([[region, category]], columns=['region', 'category'])
            prediction = model.predict(input_df)[0]
            return round(float(prediction), 2)
        except Exception as e:
            print(f"Prediction error: {e}")
            
    # Dummy mock prediction fallback
    base_pred = sales_value * 1.15
    if region == 'West':
        base_pred *= 1.2
    
    return round(base_pred, 2)
