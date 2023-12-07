from flask import Blueprint, jsonify, request
from summarizer import Summarizer
from flask_cors import CORS

summary_app = Blueprint('summary_app', __name__)
CORS(summary_app)

@summary_app.route('/generate_summary', methods=['POST'])
def generate_summary():
    try:
        # Get Inputs from user
        data = request.json
        summary = data['summary']
        max_length = data['max_length']
        min_length = data['min_length']
        num_sentences = data['num_sentences']

        # Use BERT model to summarize our input
        summarizer = Summarizer()
        generated_summary = summarizer(summary, max_length=max_length, min_length=min_length, num_sentences=num_sentences)

        # Return as JSON
        return jsonify({"user_input": summary, "generated_summary": generated_summary})

    except Exception as e:
        return jsonify({"error": str(e)})
