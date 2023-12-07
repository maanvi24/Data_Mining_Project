# Import the following
from flask import Flask
from flask_cors import CORS
from flask_app_pages.flask_app_home import home_app
from flask_app_pages.flask_app_live_feed import live_feed_app
from flask_app_pages.flask_app_summary import summary_app

# Run the App
app = Flask(__name__)
CORS(app)

# Get the blueprints from all the pages so that we can run
# All functions together and organize by page
app.register_blueprint(home_app)
app.register_blueprint(summary_app)
app.register_blueprint(live_feed_app)

if __name__ == '__main__':
    app.run(debug=True)
