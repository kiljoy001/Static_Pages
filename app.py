"""
This module is the main web app loop
"""
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    """
    Returns index template located in templates folder
    @return: str
    """
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
