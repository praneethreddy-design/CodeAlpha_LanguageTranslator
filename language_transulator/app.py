from flask import Flask, render_template, request
from google import genai
from config import API_KEY

app = Flask(__name__)

client = genai.Client(api_key=API_KEY)

LANGUAGES = {
    "auto": "Auto Detect",
    "en": "English",
    "te": "Telugu",
    "hi": "Hindi",
    "ta": "Tamil",
    "kn": "Kannada",
    "ml": "Malayalam",
    "mr": "Marathi",
    "bn": "Bengali",
    "gu": "Gujarati",
    "fr": "French",
    "de": "German",
    "es": "Spanish"
}


@app.route("/", methods=["GET", "POST"])
def home():
    translated = ""

    if request.method == "POST":
        text = request.form["text"]
        source_language = request.form["source_language"]
        target_language = request.form["language"]

        if source_language == "auto":
            prompt = f"""
Translate the following text into {LANGUAGES[target_language]}.

Only return the translated text.
Do not explain anything.

Text:
{text}
"""
        else:
            prompt = f"""
Translate the following text from {LANGUAGES[source_language]} to {LANGUAGES[target_language]}.

Only return the translated text.
Do not explain anything.

Text:
{text}
"""

        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )

            translated = response.text.strip()

        except Exception as e:
            translated = f"Error: {str(e)}"

    return render_template(
        "index.html",
        translated=translated
    )


if __name__ == "__main__":
    app.run(debug=True)