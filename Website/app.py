from flask import Flask, render_template, request, redirect, session, url_for
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
# LOGIN PAGE
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
    role = request.form["role"]

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    sql = "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)"
    values = (username, hashed_password.decode("utf-8"), role)

    cursor.execute(sql, values)
    db.commit()

    session["username"] = username
    session["role"] = role
    return redirect("/home")

# =========================
# LOGIN USER LOGIC
# =========================
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    sql = "SELECT * FROM users WHERE username = %s"
    cursor.execute(sql, (username,))
    user = cursor.fetchone()

    if user:
        if bcrypt.checkpw(password.encode("utf-8"), user["password_hash"].encode("utf-8")):
            session["username"] = username
            session["role"] = user["role"]
            return redirect("/home")

    return "Invalid Username or Password"

# =========================
# CHANGE PASSWORD LOGIC
# =========================
@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    # 1. Check if user is logged in
    if "username" not in session:
        print("Redirecting: No user in session") # Debugging line
        return redirect("/")

    if request.method == "POST":
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        if new_password != confirm_password:
            return "Passwords do not match! <a href='/change_password'>Try again</a>"

        # Hash and Update
        hashed_password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())
        
        try:
            sql = "UPDATE users SET password_hash = %s WHERE username = %s"
            cursor.execute(sql, (hashed_password.decode("utf-8"), session["username"]))
            db.commit()
            return "Password updated! <a href='/home'>Go Home</a>"
        except Exception as e:
            return f"Database error: {e}"

    return render_template("change_password.html")

# =========================
# HOME PAGE
# =========================
@app.route("/home")
def home():
    if "username" not in session:
        return redirect("/")
    return render_template("home.html", user=session['username'], role=session['role'])

# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)