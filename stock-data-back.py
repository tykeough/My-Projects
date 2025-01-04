from flask import Flask, jsonify, request
from flask_cors import CORS
import yfinance as yf

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

@app.route('/get_stock_data', methods=['GET'])
def get_stock_data():
    try:
        # Retrieve the stock symbol
        symbol = request.args.get('symbol')

        if not symbol:
            return jsonify({"error": "Missing required parameter: symbol"}), 400

        print(f"Fetching data for symbol: {symbol}")

        # Fetch all available stock data using yfinance
        stock_data = yf.download(symbol, period="max")

        if stock_data.empty:
            return jsonify({"error": f"No data found for {symbol}. It may be delisted or invalid."}), 404

        # Reset index to include the Date column
        stock_data.reset_index(inplace=True)

        # Convert the DataFrame to a JSON format with columns and data
        response_data = {
            "columns": stock_data.columns.tolist(),  # Column names
            "data": stock_data.values.tolist()       # Table data
        }

        return jsonify(response_data)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
