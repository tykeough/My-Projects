from flask import Flask, request, jsonify
from flask_cors import CORS
import yfinance as yf

app = Flask(__name__)
CORS(app)

@app.route('/get-stock-history', methods=['GET'])
def get_stock_history():
    stock_symbol = request.args.get('symbol', 'AAPL')
    start_date = request.args.get('start', '2023-01-01')
    end_date = request.args.get('end', '2023-12-31')

    try:
        stock = yf.Ticker(stock_symbol)
        stock_data = stock.history(start=start_date, end=end_date)

        if stock_data.empty:
            return jsonify({"error": "No data found for the given dates"}), 404

        # Convert the DataFrame to a JSON-friendly format
        history = stock_data[['Close']].reset_index().to_dict(orient='records')
        return jsonify({"symbol": stock_symbol, "history": history})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
