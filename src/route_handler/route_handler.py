from flask import render_template, request
from flask_hcaptcha import hCaptcha


def config_routes(app_instance, database) -> None:
    """
    Allows for injection of routes into tests, and separates view part of application from run file.
    @param database: This parameter is for injecting the missing DATABASE constant
    @param app_instance: an instance of Flask
    @return:
    """
    hcaptcha = hCaptcha(app_instance)

    @app_instance.route("/")
    def home() -> str:
        """
        Returns index template located in templates folder
        @return: website data as string
        """
        return render_template("index.html")

    @app_instance.route("/ContactMe", methods=["GET", "POST"])
    def contact_me() -> str:
        """
        Returns contact page template & posts form data to the web app.
        @return:
        @return:
        """

        if request.method == "POST" and hcaptcha.verify():
            database.insert_contact_data(request.form)
            return render_template("thankyou.html")
        else:
            return render_template("contact.html")
