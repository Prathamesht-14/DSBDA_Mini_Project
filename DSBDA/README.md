# SuperStore Sales Data Analysis & Prediction - Web Dashboard

## Overview
This repository contains a comprehensive data science and web application project focused on sales analytics and prediction. It integrates predictive modeling (Linear Regression and XGBoost) with a modern, responsive Flask-based web dashboard. Built as part of the #60DaysOfLearning2025 challenge, it includes extensive data analysis, interactive visualizations, and real-time predictions based on the Superstore Sales Dataset.

---

## Architecture & How It Works

This project is built using a **Flask Full-Stack Architecture** that seamlessly unifies a Python data-science backend with a dynamic HTML/CSS/JS frontend.

### 1. Application Flow
1. **Upload Mechanism:** The user starts by uploading a CSV file (`superstore.csv`) to the platform via the `Upload Dataset` page. 
2. **Data Processing:** The Flask backend catches the file upload, processes the data through `utils/data_loader.py` (which sanitizes columns, parses dates, and fills missing values like dynamically computing Profit), and stores the clean DataFrame securely in application memory for instantaneous querying.
3. **Analytics API:** When the user visits any dashboard page, the frontend JS queries `/api/chart-data`. The backend routes this to `utils/analytics.py`, which leverages the Pandas library to group, aggregate, and compute KPIs globally (Total Sales, Average Sales).
4. **Interactive Dashboard:** The frontend uses **Chart.js** to dynamically draw visually appealing trendlines, bar graphs, and doughnut charts without page refreshes.

### 2. File & Directory Structure
```text
project-root/
│
├── app.py                      # Main Flask application and API route definitions
├── requirements.txt            # Python dependencies (Flask, Pandas, scikit-learn, etc.)
│
├── data/                       # Directory containing user-uploaded datasets
│   └── superstore.csv
│
├── model/                      # Machine Learning models trained on historical data
│   └── sales_model.pkl         # Serialized Scikit-Learn / XGBoost models
│
├── static/                     # Frontend assets (publicly accessible)
│   ├── css/styles.css          # Custom styling, dark mode, animations
│   └── js/charts.js            # Chart.js initialization and JSON API async fetch logic
│
├── templates/                  # Jinja2 HTML blueprints
│   ├── layout.html             # Base layout (Sidebar, Top Navbar, Dark-Theme toggle)
│   ├── dashboard.html          # Main high-level KPIs and multi-chart view
│   ├── upload.html             # Drag-and-drop file upload UI
│   ├── analysis.html           # In-depth analytics with data filtering capability
│   ├── prediction.html         # Form to test the predictive model directly
│   └── model_metrics.html      # Displays live ML algorithm accuracy (MAE, R²)
│
└── utils/                      # Core backend utility scripts decoupled from Flask routing
    ├── data_loader.py          # Data ingestion, encoding rules, parsing Engine
    ├── analytics.py            # Pandas arithmetic, data grouping, summarization
    └── predictor.py            # Loads pkl files and executes model.predict()
```

---

## Key Features

1. **Modern BI Dashboard:** Similar to Tableau or Power BI. It displays KPI metrics dynamically derived from the latest data.
2. **Interactive Charting Engine:** Chart.js provides flawless visuals including Monthly Trend Lines, Category Doughnut Charts, Regional Bar Charts, and Profitability breakdowns.
3. **Machine Learning Integrations:** 
   - Uses Scikit-learn/XGBoost models to forecast metrics.
   - Live prediction UI allows users to input current `Region`, `Category`, and prior `Sales Value` to retrieve projected sales figures on the fly.
4. **Dark Mode Integration:** Full UI UX support for dark theme preferences built with CSS variables. 

---

## Dataset Variables
- **Source**: Superstore Sales Dataset ([Kaggle Link](https://www.kaggle.com/datasets/rohitsahoo/sales-forecasting/data))
- **Key Columns Engine Expects**: `Order Date`, `Sales`, `Region`, `Category`
- **Target Variable**: Continuous Sales figures.

## Instructions to Run

1. **Install Dependencies:**
   Ensure you have Python configured, then run:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Web Application:**
   Run the main execution script to build localhost server:
   ```bash
   python app.py
   ```

3. **Access the Output:**
   Open your browser and navigate to `http://localhost:5000/`. Upload your Superstore Dataset CSV file to instantiate the analytics!
