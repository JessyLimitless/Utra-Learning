import openai
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = "sk-"  # Replace with your API key


@app.route('/')
def index():
    """
    Render the main HTML page for the chatbot.
    """
    return render_template('index.html')


@app.route('/get_questions', methods=['POST'])
def get_questions():
    """
    Generate 10 thought-provoking questions based on user-provided keywords.
    """
    data = request.json
    keywords = data.get('keywords', '')

    if not keywords:
        return jsonify({"error": "No keywords provided."})

    try:
        prompt = f"Generate 10 thought-provoking questions about: {keywords}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        questions = response.choices[0].message.content.strip().split('\n')
        return jsonify(questions)
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/get_passage', methods=['POST'])
def get_passage():
    """
    Generate a detailed explanation for the selected question.
    """
    data = request.json
    question = data.get('question', '')

    if not question:
        return jsonify({"error": "No question provided."})

    try:
        prompt = f"Provide a detailed explanation about: {question}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        passage = response.choices[0].message.content.strip()
        return jsonify({"passage": passage})
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/evaluate_summary', methods=['POST'])
def evaluate_summary():
    """
    Evaluate the user's summary and provide feedback with a star rating (out of 10).
    """
    data = request.json
    summary = data.get('summary', '')
    passage = data.get('passage', '')

    if not summary or not passage:
        return jsonify({"error": "Missing summary or passage for evaluation."})

    try:
        prompt = (
            f"Evaluate the following summary:\n\nPassage: {passage}\n\n"
            f"Summary: {summary}\n\n"
            f"Provide constructive feedback and rate it out of 10 stars."
        )
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        feedback = response.choices[0].message.content.strip()

        # Extract star rating from the feedback text (assumes "Rating: X/10" format)
        try:
            rating = float(feedback.split('Rating: ')[-1].split('/')[0])
        except ValueError:
            rating = 0  # Default to 0 if parsing fails

        return jsonify({"feedback": feedback, "rating": rating})
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/get_exemplary_summary', methods=['POST'])
def get_exemplary_summary():
    """
    Generate a 5-line exemplary summary for the given passage.
    """
    data = request.json
    passage = data.get('passage', '')

    if not passage:
        return jsonify({"error": "No passage provided."})

    try:
        prompt = f"Provide a 5-line exemplary summary for the following passage:\n\n{passage}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        exemplary_summary = response.choices[0].message.content.strip()
        return jsonify({"exemplary": exemplary_summary})
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(debug=True)
