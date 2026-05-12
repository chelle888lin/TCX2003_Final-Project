from flask import Flask, render_template, request, redirect, session
import mysql.connector
import bcrypt
import secrets

app = Flask(__name__)
app.secret_key = "your_secret_key"

# =========================
# DATABASE CONNECTION
# =========================
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pass1234",
    database="tcx2003"
)
cursor = db.cursor(dictionary=True)

# =========================
# LOGIN PAGE (Changed to "/" so it's the landing page)
# =========================
@app.route("/")
def index():
    return render_template("login.html")

# =========================
# NEW USER REGISTRATION PAGE
# =========================
@app.route("/register_page")
def register_page():
    return render_template("login-NewUser.html")

# =========================
# REGISTER USER LOGIC
# =========================
@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]

    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

    sql = "INSERT INTO students (username, password_hash) VALUES (%s, %s)"
    values = (username, hashed_password.decode("utf-8"))

    cursor.execute(sql, values)
    db.commit()

    # Log them in automatically and redirect to home
    session["username"] = username
    return redirect("/home")

# =========================
# LOGIN USER LOGIC
# =========================
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    sql = "SELECT * FROM students WHERE username = %s"
    cursor.execute(sql, (username,))
    user = cursor.fetchone()

    if user:
        stored_hash = user["password_hash"]
        if bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
            session["username"] = username
            return redirect("/home")

    return "Invalid Username or Password"

# =========================
# HOME PAGE
# =========================
@app.route("/home")
def home():
    if "username" not in session:
        return redirect("/")
    return render_template("home.html", user=session['username'])

# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)