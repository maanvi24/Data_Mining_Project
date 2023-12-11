import streamlit as st
import requests
import pandas as pd
import base64  # Import base64 module

# Styling
st.markdown("""
    <style>
        body {
            background-color: #033673;
            color: white;
        }
        .custom-container {
            margin: 20px;
            margin-top: 90px;
        }
        /* Add other styles as needed */
    </style>
""", unsafe_allow_html=True)

# Streamlit app
def live_feed():
    st.title('LiveFeed')

    ticker = st.text_input('Ticker:')
    interval = st.selectbox('Interval:', ['1d', '1w', '1m', '3m', '6m'])

    if st.button('Get Articles'):
        st.write('Loading...')

        try:
            # Update the URL to point to your Flask app's endpoint
            response = requests.post('http://127.0.0.1:5000/get_articles', json={'ticker': ticker, 'interval': interval})
            # Note: Use json parameter instead of data, and specify the content type as JSON

            response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)

            articles = response.json().get('articles', [])

            if articles:
                # Create a list of dictionaries for the table
                table_data = []
                for index, article in enumerate(articles):
                    table_data.append({
                        'Date Published': article['Date Published'],
                        'Likelihood': article['Likelihood'],
                        'Model Prediction': article['Model Prediction'],
                        'Actual': article['Actual'],
                        'Open Price': article['Open Price'],
                        'Close Price': article['Close Price'],
                        'Link': f"{index + 1}. <a href='{article['URL']}' target='_blank'>Open Article</a>"
                    })

                # Create a DataFrame for the table
                df_table = pd.DataFrame(table_data)

                # Display the table with custom CSS to fit the page
                st.markdown(
                    f"""
                    <style>
                        table {{
                            width: 100%;
                        }}
                    </style>
                    """, unsafe_allow_html=True
                )

                # Display the DataFrame with links
                st.write(df_table.to_html(escape=False, index=False), unsafe_allow_html=True)

                # Add a button for downloading the table as an Excel file
                if st.button('Download Table as Excel'):
                    excel_file_path = response.json().get('excel_file_path', '')
                    print(f'Excel file path received: {excel_file_path}')  # Debugging line
                    if excel_file_path:
                        excel_file_encoded = base64.b64encode(open(excel_file_path, 'rb').read()).decode()
                        st.markdown(
                            f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{excel_file_encoded}" '
                            f'download="article_table.xlsx">Download Excel File</a>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.warning('No Excel file path provided.')

        except requests.exceptions.ConnectionError:
            st.error('Unable to connect to the server. Make sure the server is running.')

        except Exception as e:
            st.error(f'Error fetching articles. Please try again. Error: {e}')

if __name__ == '__main__':
    live_feed()
