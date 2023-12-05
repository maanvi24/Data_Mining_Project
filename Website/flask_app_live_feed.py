from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import pandas as pd
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify
from flask_cors import CORS  # Import CORS
from flask_cors import cross_origin

app = Flask(__name__)
CORS(app)

# Get today's date and format it
today = datetime.now().strftime("%Y-%m-%d")

# Define time intervals for user 
intervals = {'1d': today,
             '1w': (datetime.now() - timedelta(weeks=1)).strftime("%Y-%m-%d"),
             '1m': (datetime.now() - timedelta(weeks=4)).strftime("%Y-%m-%d"),
             '3m': (datetime.now() - timedelta(weeks=12)).strftime("%Y-%m-%d"),
             '6m': (datetime.now() - timedelta(weeks=24)).strftime("%Y-%m-%d")}

# Create get_articles function
@app.route('/get_articles', methods=['POST'])
@cross_origin(origins="http://localhost:3000")
def get_articles():
    try:

        # User will input ticker and time internal
        ticker = request.json.get('ticker')
        selected_interval = request.json.get('selected_interval')
        start_date = intervals.get(selected_interval)

        # Store everything into stock data (use code from database)
        stock_data = []

        # Use Alpha Vantage API call with ticker and key
        # Get json file
        api_key = '9NLUTD6I2QZTR2BZ'
        url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&apikey={api_key}&limit=1000'
        response = requests.get(url, verify=True)
        json_request_data = response.json()

        # if there is a feed
        if 'feed' in json_request_data:
            
            # Get feed data and preserve count
            feed_data = json_request_data['feed']

            # For each article in the feed
            for article in feed_data:

                # Try the following (if there is an error, make sure this doesn't stop)
                # use try and except
                try:

                    # Get the article URL
                    article_url = article.get('url', '')

                    # If there is an article URL
                    if article_url:
                        
                        # Use BeautifulSoup to get the text from the website
                        article_response = requests.get(article_url, verify=True)
                        article_html = article_response.text
                        article_soup = BeautifulSoup(article_html, 'html.parser')
                        article_paragraphs = article_soup.find_all('p')
                        article_text = ''
                        for paragraph in article_paragraphs:
                            article_text += paragraph.text.strip() + '\n'

                    # Get the time published for the article
                    if 'time_published' in article and article['time_published']:
                        published_date = article['time_published'][:10]
                    else:
                        published_date = 'NA'

                    # Format date so that we can use it
                    if published_date != 'NA':
                        formatted_date = datetime.strptime(published_date, "%Y%m%dT%H").strftime("%Y-%m-%d")
                        if formatted_date < start_date:
                            break

                    else:
                        formatted_date = 'NA'

                    # Record everything
                    record = {
                        "date_published": formatted_date,
                        "stock": ticker,
                        "title": article.get('title', ''),
                        "url": article_url,
                        "summary": article.get('summary', ''),
                        "text": article_text
                    }

                    # Append into stock data
                    stock_data.append(record)


                # If there is an error at any point, run an exception so that the program doesn't break
                except Exception as e:
                    print(f"Error occurred: {e}")
                    continue

            # Store everything into a df
            df = pd.DataFrame(stock_data)

            # Return everything as a json
            return jsonify({"success": True, "articles": df.to_dict(orient='records')})

    # Show Error 
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
