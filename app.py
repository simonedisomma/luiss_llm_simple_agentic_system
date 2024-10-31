from flask import Flask, jsonify
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

app = Flask(__name__)

# Create sample sales data
def create_sales_data():
    # Generate dates for the last 30 days
    dates = [(datetime.now() - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(30)]
    
    # Create sample data
    data = {
        'date': dates,
        'product': np.random.choice(['Laptop', 'Phone', 'Tablet', 'Desktop'], size=30),
        'quantity': np.random.randint(1, 50, size=30),
        'price': np.random.uniform(300, 2000, size=30).round(2),
        'region': np.random.choice(['North', 'South', 'East', 'West'], size=30)
    }
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Calculate total sales
    df['total_sales'] = df['quantity'] * df['price']
    
    return df

# Create global sales_data
sales_data = create_sales_data()

@app.route('/api/sales', methods=['GET'])
def get_sales():
    return jsonify(sales_data.to_dict(orient='records'))

@app.route('/api/sales/summary', methods=['GET'])
def get_sales_summary():
    summary = {
        'total_revenue': float(sales_data['total_sales'].sum()),
        'total_quantity': int(sales_data['quantity'].sum()),
        'avg_price': float(sales_data['price'].mean()),
        'sales_by_product': sales_data.groupby('product')['total_sales'].sum().to_dict(),
        'sales_by_region': sales_data.groupby('region')['total_sales'].sum().to_dict()
    }
    return jsonify(summary)

if __name__ == '__main__':
    app.run(debug=True)