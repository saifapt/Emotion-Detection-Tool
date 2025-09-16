"""
Flask server for Emotion Detection Application.

This server provides an API endpoint `/emotionDetector`
that accepts a text query parameter and returns the
detected emotions along with the dominant emotion.
"""

from flask import Flask, request, jsonify, redirect
from EmotionDetection import emotion_detector

app = Flask(__name__)


@app.route("/", methods=["GET"])
def root_redirect():
    """
    Redirect the root URL to /emotionDetector
    with a sample (empty) text parameter.
    """
    return redirect("/emotionDetector?text=")


@app.route("/emotionDetector", methods=["GET"])
def detect_emotion():
    """
    Detect emotions from the input text provided as a query parameter.

    Returns:
        JSON: Contains emotion scores, dominant emotion,
        and a formatted response text. Handles error cases where
        text is missing or invalid.
    """
    # Get the statement from query parameters
    text_to_analyze = request.args.get("text")

    if not text_to_analyze:
        return jsonify({"error": "Invalid text! Please try again!"}), 400

    # Call emotion detector
    result = emotion_detector(text_to_analyze)

    if result is None:
        return jsonify({"error": "Could not process the text"}), 500

    # Handle invalid dominant_emotion
    if not result.get("dominant_emotion"):
        return jsonify({
            "response_text": "Invalid text! Please try again!"
        }), 200

    # Create formatted response text
    response_text = (
        f"For the given statement, the system response is "
        f"'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, "
        f"'joy': {result['joy']} and "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )

    # Return JSON + text
    return jsonify({
        "anger": result["anger"],
        "disgust": result["disgust"],
        "fear": result["fear"],
        "joy": result["joy"],
        "sadness": result["sadness"],
        "dominant_emotion": result["dominant_emotion"],
        "response_text": response_text
    })


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
