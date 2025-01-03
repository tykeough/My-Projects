import requests
import pandas as pd

def get_full_stock_data(symbol, api_key):
    url = f"https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": api_key,
        "outputsize": "full"  # Set outputsize to "full" for complete data
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad HTTP responses
        data = response.json()

        # Check if data is available
        if "Time Series (Daily)" not in data:
            return {"error": data.get("Note", "No data available for this stock.")}

        # Convert the JSON data into a DataFrame
        time_series = data["Time Series (Daily)"]
        df = pd.DataFrame.from_dict(time_series, orient='index')
        df.columns = ["Open", "High", "Low", "Close", "Volume"]
        df.index.name = "Date"
        df = df.reset_index()

        # Convert columns to appropriate data types
        df["Open"] = df["Open"].astype(float)
        df["High"] = df["High"].astype(float)
        df["Low"] = df["Low"].astype(float)
        df["Close"] = df["Close"].astype(float)
        df["Volume"] = df["Volume"].astype(int)

        return df
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

# Example usage
if __name__ == "__main__":
    API_KEY = "163M41VVR6RQ8JQT"  # Replace with your Alpha Vantage API key
    stock_symbol = "AAPL"  # Replace with your stock symbol

    result = get_full_stock_data(stock_symbol, API_KEY)
    if isinstance(result, dict) and "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Full Stock Data for {stock_symbol}:")
        print(result)
