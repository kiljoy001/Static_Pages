"""
This module is the main web app loop
"""
from flask import Flask, render_template, request
from src.database.database import DatabaseOperation

app = Flask(__name__)
database = DatabaseOperation("contacts.db")
database.create_leads_table("leads")
database.create_appointment_table("appointments")


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
        data = dict(request.form)
        data["visible"] = 1
        database.insert_contact_data(data)
        return render_template("contact.html")
    else:
        return render_template("contact.html")


@app.route("/admin")
def admin():
    """
    Returns admin page template with all contacts
    @return:
    """
    contacts = database.get_all_contacts()
    return render_template("admin.html", contacts=contacts)


if __name__ == "__main__":
    app.run()
