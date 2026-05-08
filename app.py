from flask import Flask, render_template, request, redirect, session, url_for, flash
from user_registration import setup_database, register_user, get_user
from ml_model import load_model
from email_service import send_email, send_report_email

from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Initialize database
setup_database()

# Load ML model
model, vectorizer = load_model()


# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("login.html")


# ---------------- REGISTER ----------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        parent_name = request.form.get("parent_name")
        parent_email = request.form.get("parent_email")
        password = request.form.get("password")

        if not all([name, email, parent_name, parent_email, password]):
            flash("All fields required!", "danger")
            return redirect(url_for("register"))

        success = register_user(
            name,
            email,
            parent_name,
            parent_email,
            password
        )

        if not success:

            send_email(
                parent_email,
                "Registration Failed",
                f"Hello {parent_name},\n\nEmail already exists."
            )

            flash("Email already registered.", "danger")
            return redirect(url_for("register"))

        send_email(
            parent_email,
            "Registration Successful",
            f"Hello {parent_name},\n\n"
            f"Your child {name} has been registered successfully."
        )

        flash("Registration successful!", "success")

        return redirect(url_for("home"))

    return render_template("register.html")


# ---------------- LOGIN ----------------

@app.route("/login", methods=["POST"])
def login():

    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        flash("Enter email and password.", "danger")
        return redirect(url_for("home"))

    user = get_user(email, password)

    if user:
        session["user"] = user
        return redirect(url_for("dashboard"))

    flash("Invalid credentials", "danger")
    return redirect(url_for("home"))


# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect(url_for("home"))

    return render_template(
        "dashboard.html",
        user=session["user"]
    )


# ---------------- CHAT (FIXED — THIS WAS MISSING) ----------------

@app.route("/chat", methods=["GET", "POST"])
def chat():

    if "user" not in session:
        return redirect(url_for("home"))

    response = None

    if request.method == "POST":

        message = request.form.get("message")

        if message:

            vec = vectorizer.transform([message])
            pred = model.predict(vec)[0]

            response = (
                "Cyberbullying Detected"
                if pred == 1
                else "Safe Message"
            )

            if pred == 1:

                user = session["user"]

                parent_name = user[3]
                parent_email = user[4]

                send_email(
                    parent_email,
                    "Cyberbullying Alert",
                    f"Dear {parent_name},\n\n"
                    f"Cyberbullying message detected:\n\n"
                    f"\"{message}\""
                )

        else:
            flash("Enter message.", "danger")

    return render_template(
        "chat.html",
        response=response
    )


# ---------------- DETECT ----------------

@app.route("/detect", methods=["GET", "POST"])
def detect():

    if "user" not in session:
        return redirect(url_for("home"))

    if request.method == "POST":

        text = request.form.get("text")

        if text:

            vec = vectorizer.transform([text])
            pred = model.predict(vec)[0]

            prediction = (
                "Cyberbullying"
                if pred == 1
                else "Non-Cyberbullying"
            )

            session["last_text"] = text
            session["last_prediction"] = prediction

            return render_template(
                "result.html",
                text=text,
                prediction=prediction
            )

        flash("Enter text.", "danger")

    return render_template("detect.html")


# ---------------- REPORT ----------------

@app.route("/report")
def report():

    if "user" not in session:
        return redirect(url_for("home"))

    user = session["user"]

    child_name = user[1]
    parent_name = user[3]
    parent_email = user[4]

    text = session.get("last_text")
    prediction = session.get("last_prediction")

    date = datetime.now().strftime("%d-%m-%Y %H:%M")

    if not text or not prediction:

        flash(
            "Run detection first.",
            "warning"
        )

        return redirect(url_for("detect"))

    send_report_email(
        parent_email,
        parent_name,
        child_name,
        text,
        prediction,
        date
    )

    return render_template(
        "report.html",
        text=text,
        prediction=prediction,
        date=date
    )


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.pop("user", None)

    flash("Logged out.", "success")

    return redirect(url_for("home"))


# ---------------- MAIN ----------------

if __name__ == "__main__":
    app.run(debug=True)