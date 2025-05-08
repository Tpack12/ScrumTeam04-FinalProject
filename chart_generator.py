import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for server
import matplotlib.pyplot as plt
from datetime import datetime
import os

def generate_chart(data, chart_type, start_date, end_date, symbol):
    # Identify the correct time series key
    time_series_key = next((key for key in data if 'Time Series' in key), None)
    if not time_series_key:
        print("Could not find time series data in API response.")
        return None

    raw_data = data[time_series_key]
    filtered_dates = []
    closing_prices = []

    for date_str in sorted(raw_data.keys()):
        if start_date <= date_str <= end_date:
            filtered_dates.append(datetime.strptime(date_str, "%Y-%m-%d"))
            closing_prices.append(float(raw_data[date_str]["4. close"]))

    if not filtered_dates:
        print("No stock data found in the selected date range.")
        return None

    # Plot the chart
    plt.figure(figsize=(12, 6))
    if chart_type == "line":
        plt.plot(filtered_dates, closing_prices, marker='o', linestyle='-', color='blue')
    elif chart_type == "bar":
        plt.bar(filtered_dates, closing_prices, color='skyblue')
    else:
        print("Unsupported chart type.")
        return None

    plt.xlabel("Date")
    plt.ylabel("Closing Price (USD)")
    plt.title(f"{symbol} Stock Prices ({start_date} to {end_date})")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)

    # Save to /static directory
    os.makedirs("static", exist_ok=True)
    filename = f"{symbol}_{start_date}_to_{end_date}.png"
    filepath = os.path.join("static", filename)
    plt.savefig(filepath)
    plt.close()

    return filepath
