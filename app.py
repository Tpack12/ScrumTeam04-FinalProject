from flask import Flask, render_template, request, redirect, url_for, flash
from stock_api import fetch_stock_data
from chart_generator import generate_chart
from utils import validate_date_range
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Used for flash messages

# Load stock symbols from CSV
def load_stock_symbols():
    df = pd.read_csv("stocks.csv")
    return [f"{row['Symbol']} - {row['Name']}" for _, row in df.iterrows()]

@app.route('/', methods=['GET', 'POST'])
def index():
    chart_data = None
    stock_options = load_stock_symbols()

    if request.method == 'POST':
        selected = request.form.get('symbol')
        if " - " in selected:
            symbol = selected.split(" - ")[0].strip().upper()
        else:
            symbol = selected.strip().upper()

        chart_type = request.form.get('chart_type', 'line')
        time_series = request.form.get('time_series', 'TIME_SERIES_DAILY')
        start_date = request.form.get('start_date', '')
        end_date = request.form.get('end_date', '')

        if not symbol:
            flash('Please select a stock symbol.')
            return redirect(url_for('index'))

        if not validate_date_range(start_date, end_date):
            flash('Invalid date range. Please try again.')
            return redirect(url_for('index'))

        data = fetch_stock_data(symbol, time_series)
        if data:
            chart_data = generate_chart(data, chart_type, start_date, end_date, symbol)
            if not chart_data:
                flash('No chart generated for that range.')
        else:
            flash('Failed to retrieve stock data.')

    return render_template('index.html', chart_data=chart_data, stock_options=stock_options)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
