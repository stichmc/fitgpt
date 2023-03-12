import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

responses = [] # Initialize empty list to store responses

@app.route("/", methods=("GET", "POST"))
def index():
    global responses # Allow access to global variable

    if request.method == "POST":
        fitness = request.form["fitness"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(fitness),
            temperature=0.6,
            max_tokens=1024
        )
        response_text = response.choices[0].text
        responses.append(response_text) # Add new response to list
        return redirect(url_for("index", result=response_text))

    result = request.args.get("result")
    return render_template("index.html", result=result, responses=responses)

def generate_prompt(fitness):
    return """Answer the following question related to fitness, if the question is not related to fitness find a way to relate it to fitness:

Question: {}

Answer:""".format(
        fitness.capitalize()
    )


