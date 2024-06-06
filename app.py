from flask import Flask, render_template, request
import requests
from gtts import gTTS
import speech_recognition as sr

app = Flask(__name__)

# Function to perform a Google search using the SERP API
def search_google(query):
    api_key = "eab3a4ff1eb26c3de63b0fc65dc266c4574acc21f4bf7db792a8dcbc3e319faf"
    params = {
        "engine": "google",
        "q": query,
        "google_domain": "google.com",
        "device": "mobile",
        "device": "desktop",
        "api_key": api_key
    }
    response = requests.get("https://serpapi.com/search", params=params)
    data = response.json()

    if "error" in data:
        return {"error": data["error"]}
    else:
        relevant_data = {
            "query": data["search_information"]["query_displayed"],
            "total_results": data["search_information"]["total_results"],
            "related_questions": []
        }
        for question in data["related_questions"]:
            relevant_question = {
                "question": question["question"],
                "snippet": question.get("snippet", ""),
                "link": question["link"]
            }
            relevant_data["related_questions"].append(relevant_question)

        return relevant_data

# Function to convert text to speech
def speak_answer(snippet):
    tts = gTTS(text=snippet, lang="en")
    tts.save("static/answer.mp3")

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle the search request
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')

    # Perform Google search
    search_result = search_google(query)

    if search_result and not search_result.get('error'):
        speak_answer(search_result["related_questions"][0]["snippet"])
        return render_template('result.html', result=search_result)
    else:
        return render_template('index.html', error="For This query please book a appoientment with our partered Docters ")

if __name__ == '__main__':
    app.run(debug=False)

