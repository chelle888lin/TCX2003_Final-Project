from flask import Flask, render_template, request, redirect, session
import mysql.connector
import bcrypt
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# =========================
# DATABASE CONNECTION
# =========================
db = mysql.connector.connect(
    host="localhost",
    user="root",
    port=3306,
    password="root",
    database="tcx2003"
)
cursor = db.cursor(dictionary=True)

# =========================
# LANDING PAGE (LOGIN)
# =========================
@app.route("/")
def index():
    # If already logged in, go home
    if "username" in session:
        return redirect("/home")

    return render_template("login.html")


# =========================
# REGISTER PAGE
# =========================
@app.route("/register_page")
def register_page():
    return render_template("login-NewUser.html")


# =========================
# REGISTER USER
# =========================
@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    role = request.form.get("role", "user")

    if not username or not password:
        return "Missing username or password"

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)",
            (username, hashed_password.decode("utf-8"), role)
        )
        db.commit()
    except mysql.connector.IntegrityError:
        return "Username already exists"

    session["username"] = username
    session["role"] = role
    return redirect("/home")


# =========================
# LOGIN
# =========================
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user and bcrypt.checkpw(
        password.encode("utf-8"),
        user["password_hash"].encode("utf-8")
    ):
        session["username"] = user["username"]
        session["role"] = user["role"]
        return redirect("/home")

    return render_template("login.html", error="Invalid Username or Password")


# =========================
# HOME PAGE
# =========================
@app.route("/home")
def home():
    if "username" not in session:
        return redirect("/")

    return render_template(
        "home-student.html",
        user=session["username"],
        role=session["role"]
    )


# =========================
# CHANGE PASSWORD
# =========================
@app.route("/change_password", methods=["GET", "POST"])
def change_password():

    if "username" not in session:
        return redirect("/")

    if request.method == "POST":
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        if not new_password or not confirm_password:
            return "Missing fields"

        if new_password != confirm_password:
            return "Passwords do not match <a href='/change_password'>Try again</a>"

        hashed_password = bcrypt.hashpw(
            new_password.encode("utf-8"),
            bcrypt.gensalt()
        )

        try:
            cursor.execute(
                "UPDATE users SET password_hash = %s WHERE username = %s",
                (hashed_password.decode("utf-8"), session["username"])
            )
            db.commit()
            return redirect("/home")
        except Exception as e:
            return f"Database error: {e}"

    return render_template("change_password.html")


# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(debug=True)