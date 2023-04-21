"""
This module is the main web app loop
"""
from flask import Flask, render_template, request
from src.database.database import DatabaseOperation

app = Flask(__name__)
database = DatabaseOperation("contacts.db")


@app.route("/")
def home():
    """
    Returns index template located in templates folder
    @return: str
    """
    return render_template("index.html")


@app.route("/ContactMe", methods=["GET", "POST"])
def contact_me():
    """
    Returns contact page template & posts form data to the web app.
    @return:
    """
    if request.method == "POST":
        database.insert_contact_data(request.form)
        return render_template("contact.html")
    else:
        return render_template("contact.html")


if __name__ == "__main__":
    app.run()
