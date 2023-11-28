# Import the following
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import time

# API Key for Alpha Vantage
api_key = '9NLUTD6I2QZTR2BZ' 

# Get List of SP500 companies from wikipedia
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
data_url = pd.read_html(url)
sp500_companies = data_url[0]

# Convert the following into a list
sp500_symbols = sp500_companies['Symbol'].tolist()

# If program stops, update position here
sp500_symbols = sp500_symbols[21:]

# From Alpha Vantage, create a list of topics to analyze
topics = [
    "Blockchain", 
    "Earnings", 
    "IPO", 
    "Mergers & Acquisitions", 
    "Financial Markets",
    "Economy - Fiscal Policy", 
    "Economy - Monetary Policy", 
    "Economy - Macro/Overall",
    "Energy & Transportation", 
    "Finance", 
    "Life Sciences", 
    "Manufacturing", 
    "Real Estate & Construction",
    "Retail & Wholesale", 
    "Technology"
]

# Store everything into stock data
stock_data = []

# For ticker in SP500
for ticker in sp500_symbols:

    # Use Alpha Vantage API call with ticker and key
    # Get json file
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&apikey={api_key}&limit=1000'
    response = requests.get(url, verify=True)
    json_request_data = response.json()
    print(f'Looking at {ticker}')

    # if there is a feed
    if 'feed' in json_request_data:

        # Get feed data and preserve count
        feed_data = json_request_data['feed']
        count = 0

        # For each article in the feed
        for article in feed_data:

            # Try the following (if there is an error, make sure this doesnt stop)
            # use try and except
            try:
                print(f'Looking at Article {count}')

                # Get the article URL
                article_url = article.get('url', '')

                # Store the following as None
                article_text = None
                relevance_score = None

                # For now, fill in all topics relevance with 0
                topics_relevance = {}
                for topic in topics:
                    topics_relevance[topic] = 0

                # If there are any topics,
                if article.get('topics'):

                    # For topic in article topics, get the score
                    # if there is nothing, put 0
                    for topic in article['topics']:
                        if topic['topic'] in topics:
                            topics_relevance[topic['topic']] = topic.get('relevance_score', 0)

                # If there is an article url
                if article_url:

                    # Use BeautifulSoup to get the text from the webiste 
                    # https://www.geeksforgeeks.org/implementing-web-scraping-python-beautiful-soup/
                    article_response = requests.get(article_url, verify=True)
                    article_html = article_response.text
                    article_soup = BeautifulSoup(article_html, 'html.parser')
                    article_paragraphs = article_soup.find_all('p')
                    article_text = ''
                    for paragraph in article_paragraphs:
                        article_text += paragraph.text.strip() + '\n'

                # If there is a sentiment score
                if article.get('ticker_sentiment'):

                    # Find the relevance score for this stock
                    ticker_sentiments = article['ticker_sentiment']
                    for ticker_sentiment in ticker_sentiments:
                        if ticker_sentiment.get('ticker') == ticker:
                            relevance_score = ticker_sentiment.get('relevance_score')
                            break

                # Get the time published for article
                if 'time_published' in article and article['time_published']:
                    published_date = article['time_published'][:10]
                else:
                    published_date = 'NA'
                
                # Format date so that we can use it
                if published_date != 'NA':
                    formatted_date = datetime.strptime(published_date, "%Y%m%dT%H").strftime("%Y-%m-%d")
                else:
                    formatted_date = 'NA'

                # Store the following as NA
                article_price_open_stock = 'NA'
                article_price_close_stock = 'NA'
                article_price_open_spy = 'NA'
                article_price_close_spy = 'NA'

                # If there is a date, get article open and close price for stock from Yahoo finance
                if formatted_date != 'NA':
                    stock = yf.Ticker(ticker)
                    historical_data_stock = stock.history(start=formatted_date, end=(datetime.strptime(formatted_date, "%Y-%m-%d") + timedelta(days=2)).strftime("%Y-%m-%d"))
                    article_price_open_stock = historical_data_stock.iloc[0]["Close"]
                    article_price_close_stock = historical_data_stock.iloc[-1]["Close"]

                    # Get the data for SPY from yahoo finance 
                    spy = yf.Ticker('SPY')

                    # We want to set the delta to 2 here and get the close price
                    historical_data_spy = spy.history(start=formatted_date, end=(datetime.strptime(formatted_date, "%Y-%m-%d") + timedelta(days=2)).strftime("%Y-%m-%d"))
                    article_price_open_spy = historical_data_spy.iloc[0]["Close"]
                    article_price_close_spy = historical_data_spy.iloc[-1]["Close"]

                # Make a print statement stating that prices were collected
                if article_price_open_stock != 'NA' and article_price_close_stock != 'NA' and article_price_open_spy != 'NA' and article_price_close_spy != 'NA':
                    print(f"For article on {formatted_date}, all prices are available.")

                # Record everything
                record = {
                    "stock": ticker,
                    "title": article.get('title', ''),
                    "url": article_url,
                    "time_published": article.get('time_published', ''),
                    "authors": ', '.join(article.get('authors', [])),
                    "summary": article.get('summary', ''),
                    'text': article_text,
                    "source": article.get('source', ''),
                    "source_domain": article.get('source_domain', ''),
                    "overall_sentiment_score": article.get('overall_sentiment_score', ''),
                    "relevance_score": relevance_score,
                    **topics_relevance,
                    "article_price_open_stock": article_price_open_stock,
                    "article_price_close_stock": article_price_close_stock,
                    "article_price_open_spy": article_price_open_spy,
                    "article_price_close_spy": article_price_close_spy,
                    "Date": formatted_date
                }

                # Append into stock data
                stock_data.append(record)

                # Increase count by 1 to let us know how many 
                # articles we have looked at
                count += 1


            # If there is an error at any point, run an exception so that program doesnt break
            except Exception as e:
                print(f"Error occurred: {e}")
                continue

        # Store everything into a df
        df = pd.DataFrame(stock_data)

        
        # Update Excel file
        # I updated the excel file name to database manually
        try:
            df.to_excel(f'Final_Database_continue_2.xlsx', index=False)
            print(f'Excel sheet has been updated with {ticker}')
            print(len(df))
        except Exception as e:
            print(f'Error saving Excel file: {e}')
            print(f'Excel sheet was not updated due to an error.')