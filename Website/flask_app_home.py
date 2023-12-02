# Import the Following
from flask import Flask, request, jsonify
import joblib
import os
from flask_cors import CORS

# Create App
app = Flask(__name__)
CORS(app)

# Use current Directory
current_directory = os.path.dirname(__file__)

# Get Model for Movement
model_path_movement = os.path.join(current_directory, 'Random Forest_accuracy_0.72.joblib')
loaded_model_movement = joblib.load(model_path_movement)

# Get Model for Sentiment
model_path_sentiment = os.path.join(current_directory, 'Random Forest Regression_mse_0.02_r2_0.22.joblib')
loaded_model_sentiment = joblib.load(model_path_sentiment)

# Get Models for Relevance (We will be able to call multiple models from this)
model_path_relevance = os.path.join(current_directory, 'best_models_dictionary.joblib')
models_path_relevance = joblib.load(model_path_relevance)

# Create Predict Relevance function
@app.route('/predict_relevance', methods=['POST'])
def predict_relevance():
    try:
        data = request.get_json()
        article_text = data.get('article', {}).get('text', '')
        topic = data.get('topic', '')

        if topic not in models_path_relevance:
            return jsonify({'Error': f'Model for topic "{topic}" not found'})

        best_model = models_path_relevance[topic]
        prediction = best_model.predict([article_text])[0]

        prediction = float(prediction)

        print(f"Prediction for {topic}: {prediction}")

        return jsonify({'prediction': prediction})

    except Exception as e:
        return jsonify({'Error': str(e)})


# Create Predict Sentiment Function
@app.route('/predict_sentiment', methods=['POST'])
def prediction_sentiment():
    try:
        data = request.get_json()
        article_text = data.get('article', {}).get('text', '')

        prediction = loaded_model_sentiment.predict([article_text])

        print(f"Sentiment Prediction: {prediction[0]}")

        result = {'sentiment': prediction[0]}

        return jsonify(result)

    except Exception as e:
        return jsonify({'Error': str(e)})


# Create Predict Movement Function
@app.route('/predict_movement', methods=['POST'])
def prediction_movement():
    try:
        data = request.get_json()
        article_text = data.get('article', {}).get('text', '')

        prediction = loaded_model_movement.predict([article_text])

        if prediction[0] == 1:
            output = 'up'
        else:
            output = 'down'

        print(f"Prediction: {output}")

        result = {'prediction': output}

        return jsonify(result)

    except Exception as e:
        return jsonify({'Error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
