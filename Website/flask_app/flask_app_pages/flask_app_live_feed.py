from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
import pandas as pd
import requests
from bs4 import BeautifulSoup
import yfinance as yf
import os
import joblib

live_feed_app = Blueprint('live_feed_app', __name__)

# Get today's date and format it
today = datetime.now().strftime("%Y-%m-%d")

current_directory = os.path.dirname(__file__)
model_path_movement = os.path.join(current_directory, 'Logistic Regression_accuracy_0.61.joblib')
loaded_model_movement = joblib.load(model_path_movement)

# Define time intervals for the user
intervals = {'1d': today,
             '1w': (datetime.now() - timedelta(weeks=1)).strftime("%Y-%m-%d"),
             '1m': (datetime.now() - timedelta(weeks=4)).strftime("%Y-%m-%d"),
             '3m': (datetime.now() - timedelta(weeks=12)).strftime("%Y-%m-%d"),
             '6m': (datetime.now() - timedelta(weeks=24)).strftime("%Y-%m-%d")}

@live_feed_app.route('/get_articles', methods=['POST'])
def get_articles():
    try:
        data = request.get_json()
        ticker = data.get('ticker', '')
        interval = data.get('interval', '')

        # Use code from Database
        # Store stock data
        stock_data = []

        # Use Alpha Vantage API call with ticker and key
        # Get JSON file
        api_key = '9NLUTD6I2QZTR2BZ'
        url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&apikey={api_key}&limit=1000'
        response = requests.get(url, verify=True)
        json_request_data = response.json()

        # If there is a feed
        if 'feed' in json_request_data:
            feed_data = json_request_data['feed']

            # For each article in the feed
            for article in feed_data:
                # Try the following (if there is an error, make sure this doesn't stop)
                # Use try and except
                try:
                    # Get the article URL
                    article_url = article.get('url', '')

                    # Store the following as None
                    article_text = None

                    # If there is an article URL
                    if article_url:
                        # Use BeautifulSoup to get the text from the website
                        article_response = requests.get(article_url, verify=True)
                        article_html = article_response.text
                        article_soup = BeautifulSoup(article_html, 'html.parser')
                        article_paragraphs = article_soup.find_all('p')
                        article_text = '\n'.join(paragraph.text.strip() for paragraph in article_paragraphs)

                    # Get the time published for the article
                    published_date = article.get('time_published', '')[:10]

                    # Format date so that we can use it
                    formatted_date = datetime.strptime(published_date, "%Y%m%dT%H").strftime("%Y-%m-%d") if published_date else 'NA'

                    # Skip articles not within the selected interval
                    print(formatted_date, today)
                    if interval == '1d' and formatted_date < intervals['1d']:
                        break
                    elif interval == '1w' and formatted_date < intervals['1w']:
                        break
                    elif interval == '1m' and formatted_date < intervals['1m']:
                        break
                    elif interval == '3m' and formatted_date < intervals['3m']:
                        break
                    elif interval == '6m' and formatted_date < intervals['6m']:
                        break

                    # Store the following as NA
                    article_price_open_stock = 'NA'
                    article_price_close_stock = 'NA'

                    # If there is a date, get article open and close price for stock from Yahoo finance
                    if formatted_date != 'NA':
                        stock = yf.Ticker(ticker)
                        historical_data_stock = stock.history(start=formatted_date, end=(datetime.strptime(formatted_date, "%Y-%m-%d") + timedelta(days=2)).strftime("%Y-%m-%d"))
                        article_price_open_stock = historical_data_stock.iloc[0]["Close"]
                        article_price_close_stock = historical_data_stock.iloc[-1]["Close"]

                    # Make a print statement stating that prices were collected
                    if article_price_open_stock != 'NA' and article_price_close_stock != 'NA':
                        print(f"For article on {formatted_date}, stock movement is available.")

                    # Calculate movement of the stock between article_price_open_stock and article_price_close_stock
                    if formatted_date >= today or formatted_date == (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"):
                        actual = "N/A"
                    else:
                        actual_movement = article_price_close_stock - article_price_open_stock
                        if actual_movement > 0:
                            actual = 1
                        elif actual_movement == 0:
                            actual = 'N/A'
                        else:
                            actual = 0

                    # Collect Model Prediction
                    if article_text is None:
                        model_prediction = loaded_model_movement.predict([article.get('summary', '')])[0]
                        likelihood = loaded_model_movement.predict_proba([article.get('summary', '')])[0][1] * 100
                    else:
                        model_prediction = loaded_model_movement.predict([article_text])[0]
                        likelihood = loaded_model_movement.predict_proba([article_text])[0][1] * 100

                    # Record everything
                    record = {
                        "Date Published": formatted_date,
                        "Stock Ticker": ticker,
                        "Title": article.get('title', ''),
                        "URL": article_url,
                        "Summary": article.get('summary', ''),
                        "Likelihood": likelihood,
                        "Model Prediction": model_prediction,
                        "Actual": actual,
                        "Open Price": article_price_open_stock,
                        "Close Price": article_price_close_stock,
                        "Difference": (article_price_close_stock - article_price_open_stock)
                    }

                    # Append into stock data
                    stock_data.append(record)

                # If there is an error at any point, run an exception so that the program doesn't break
                except Exception as e:
                    print(f"Error occurred: {e}")
                    continue

            # Store everything into a DataFrame
            df = pd.DataFrame(stock_data)
            df_excel = pd.DataFrame(stock_data)
            excel_file_path = os.path.join(current_directory, 'test.xlsx')
            df_excel.to_excel(excel_file_path, index=False)

            return jsonify({"success": True, "articles": df.to_dict(orient='records')})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
