import os
from flask import Flask, request, render_template
from flask_wtf.csrf import CSRFProtect
import openai

openai.api_key = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)

app.config.update(
    SECRET_KEY=os.environ.get("FLASK_SECRET"),
    SESSION_COOKIE_HTTPONLY=True,
    REMEMBER_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Strict",
)
csrf = CSRFProtect()
csrf.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/suggest", methods=["POST"])
def suggest():
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=request.json["prompt"][-1024:],
        max_tokens=16,
        temperature=0.5,
        top_p=1,
    )
    suggestion = response["choices"][0]["text"]
    print("Prompt:\n", request.json["prompt"])
    print("Suggestion:\n", suggestion)
    return {"suggestion": suggestion}


if __name__ == "__main__":
    app.run()
