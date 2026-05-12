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
    password="yourpassword",
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
# REGISTER USER
# =========================

@app.route("/register", methods=["POST"])
def register():

    username = request.form["username"]
    password = request.form["password"]

    # HASH PASSWORD
    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

    sql = """
    INSERT INTO students (username, password_hash)
    VALUES (%s, %s)
    """

    values = (
        username,
        hashed_password.decode("utf-8")
    )

    cursor.execute(sql, values)
    db.commit()

    return "Student Registered Successfully"


# =========================
# LOGIN USER
# =========================

@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    sql = """
    SELECT * FROM students
    WHERE username = %s
    """

    cursor.execute(sql, (username,))
    user = cursor.fetchone()

    if user:

        stored_hash = user["password_hash"]

        # VERIFY HASHED PASSWORD
        if bcrypt.checkpw(
            password.encode("utf-8"),
            stored_hash.encode("utf-8")
        ):

            # CREATE SESSION TOKEN
            session_token = secrets.token_hex(16)

            session["username"] = username
            session["session_token"] = session_token

            # SAVE SESSION TO DATABASE
            sql2 = """
            INSERT INTO sessions
            (username, session_token)
            VALUES (%s, %s)
            """

            cursor.execute(sql2, (
                username,
                session_token
            ))

            db.commit()

            return redirect("/home")

    return "Invalid Username or Password"


# =========================
# HOME PAGE
# =========================

@app.route("/home")
def home():

    if "username" not in session:
        return redirect("/")

    return f"""
    <h1>Welcome {session['username']}</h1>
    <p>Login Successful</p>
    """


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