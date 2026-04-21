import os
import pandas as pd
from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
from utils.data_loader import load_data, preprocess_data
from utils.analytics import generate_kpis, get_sales_by_region, get_sales_by_category, get_profit_by_segment, get_monthly_sales_trend
from utils.predictor import load_model, predict, train_model
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'data'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Global state to store the loaded dataframe (in a real app, use a database or caching mechanism)
app.config['DF'] = None

MODEL_PATH = 'model/sales_model.pkl'
METRICS_PATH = 'model/metrics.json'

@app.route('/')
def dashboard():
    df = app.config['DF']
    if df is None:
        # Try to load existing data
        data_path = os.path.join(app.config['UPLOAD_FOLDER'], 'superstore.csv')
        if os.path.exists(data_path):
            df = load_data(data_path)
            df = preprocess_data(df)
            app.config['DF'] = df
        else:
            return redirect(url_for('upload'))
            
    if df is not None:
        kpis = generate_kpis(df)
        return render_template('dashboard.html', kpis=kpis)
    return redirect(url_for('upload'))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and file.filename.endswith('.csv'):
            filename = 'superstore.csv' # Always save as superstore.csv for simplicity
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Load and preprocess
            df = load_data(filepath)
            df = preprocess_data(df)
            app.config['DF'] = df
            
            # Train the model on new data
            train_model(df, MODEL_PATH, METRICS_PATH)
            
            return redirect(url_for('dashboard'))
    return render_template('upload.html')

@app.route('/analysis')
def analysis():
    df = app.config['DF']
    if df is None:
        return redirect(url_for('upload'))
    return render_template('analysis.html')

@app.route('/api/chart-data')
def chart_data():
    df = app.config['DF']
    if df is None:
        return jsonify({"error": "No data available"}), 400
        
    region_sales = get_sales_by_region(df)
    category_sales = get_sales_by_category(df)
    segment_profit = get_profit_by_segment(df)
    monthly_trend = get_monthly_sales_trend(df)
    
    return jsonify({
        'region_sales': region_sales,
        'category_sales': category_sales,
        'segment_profit': segment_profit,
        'monthly_trend': monthly_trend
    })

@app.route('/predict')
def prediction():
    return render_template('prediction.html')

@app.route('/predict_sales', methods=['POST'])
def predict_sales():
    data = request.json
    region = data.get('region')
    category = data.get('category')
    sales_value = float(data.get('sales_value', 0))
    
    model = load_model(MODEL_PATH)
    # Simple mockup for prediction since we don't have the actual model file details yet
    predicted_sales = predict(model, region, category, sales_value)
    
    return jsonify({'predicted_sales': predicted_sales})

@app.route('/model')
def model_metrics():
    # Load metrics from file or use fallback
    if os.path.exists(METRICS_PATH):
        with open(METRICS_PATH, 'r') as f:
            metrics = json.load(f)
    else:
        metrics = {
            'r2_score': 'N/A',
            'mae': 'N/A'
        }
    return render_template('model_metrics.html', metrics=metrics)

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
