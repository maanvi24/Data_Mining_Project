# Import the following
from flask import Flask, request, jsonify
from summarizer import Summarizer

# Create app
app = Flask(__name__)

# Create generate_summary function
@app.route('/generate_summary', methods=['POST'])
def generate_summary():
    try:

        # Get Inputs from user
        data = request.json
        summary = data['summary']
        max_length = int(data['max_length'])
        min_length = int(data['min_length'])
        num_sentences = int(data['num_sentences'])

        # Use BERT model to summarize our input
        summarizer = Summarizer()
        generated_summary = summarizer(summary, max_length=max_length, min_length=min_length, num_sentences=num_sentences)

        # Return as JSON
        return jsonify({"user_input": summary, "generated_summary": generated_summary})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
