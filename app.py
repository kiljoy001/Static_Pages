"""
This module is the main web app loop
"""
import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
from src.database.database import DatabaseOperation
from src.page import Page
from src.appointment import Appointment
from src.notification import NotificationService

app = Flask(__name__)
notification_service = NotificationService()
app.config['UPLOAD_FOLDER'] = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

database = DatabaseOperation("contacts.db")
database.create_leads_table("leads")
database.create_appointment_table("appointments")
database.create_pages_table("pages")

# Seed default pages if they don't exist
if not database.get_page_by_route("home"):
    database.insert_page(Page(route="home", title="Welcome", content="Welcome to our website!"))
if not database.get_page_by_route("services"):
    database.insert_page(Page(route="services", title="Our Services", content="Here are our services."))
if not database.get_page_by_route("gallery"):
    database.insert_page(Page(route="gallery", title="Gallery", content="Check out our work."))


@app.route("/")
def home():
    """
    Returns index template located in templates folder
    @return: str
    """
    page = database.get_page_by_route("home")
    return render_template("index.html", page=page)

@app.route("/services")
def services():
    """
    Returns services template
    @return: str
    """
    page = database.get_page_by_route("services")
    return render_template("services.html", page=page)


@app.route("/gallery")
def gallery():
    """
    Returns gallery template
    @return: str
    """
    page = database.get_page_by_route("gallery")
    return render_template("gallery.html", page=page)


@app.route("/appointments")
def appointments():
    """
    Returns appointments template
    @return: str
    """
    return render_template("appointments.html")


@app.route("/save_appointment", methods=["POST"])
def save_appointment():
    """
    Saves a new appointment
    """
    data = request.json
    try:
        # Expected date format YYYY-MM-DD from the frontend
        # But Appointment model expects datetime object and we store isoformat.
        # We need to decide what time to set or if just date is enough.
        # The calendar sends YYYY-MM-DD. Let's default to a time or just parse as date.
        # src/database/database.py expects Appointment object.

        date_str = data.get("date")
        # Parse YYYY-MM-DD
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")

        appointment = Appointment(
            date=date_obj,
            event_name=data.get("event_name"),
            phone_number=data.get("phone_number"),
            location=data.get("location"),
            message=data.get("message")
        )

        if database.insert_appointment(appointment):
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "error": "Database error"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


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
    Returns admin page template with all contacts and pages
    @return:
    """
    contacts = database.get_all_contacts()
    pages = database.get_all_pages()
    return render_template("admin.html", contacts=contacts, pages=pages)


@app.route("/admin/notify", methods=["POST"])
def notify():
    """
    Sends notification via Twilio/SendGrid
    """
    contact_type = request.form.get("type") # email, sms, call
    to = request.form.get("to")
    message = request.form.get("message")
    subject = request.form.get("subject", "Notification") # Only for email

    if contact_type == "email":
        success = notification_service.send_email(to, subject, message)
    elif contact_type == "sms":
        success = notification_service.send_sms(to, message)
    elif contact_type == "call":
        success = notification_service.make_call(to, message)
    else:
        return jsonify({"success": False, "error": "Invalid notification type"})

    if success:
        return redirect(url_for('admin'))
    else:
        return "Failed to send notification", 500


@app.route("/admin/edit_page/<route>", methods=["GET", "POST"])
def edit_page(route):
    """
    Edit a page
    """
    page = database.get_page_by_route(route)
    if not page:
        return "Page not found", 404

    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        image = request.files.get("image")
        image_url = page.image_url

        if image and image.filename and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(filepath)
            image_url = url_for('static', filename=f'uploads/{filename}')

        updated_page = Page(route=route, title=title, content=content, image_url=image_url)
        database.update_page(updated_page)
        return redirect(url_for('admin'))

    return render_template("edit_page.html", page=page)


if __name__ == "__main__":
    app.run()
