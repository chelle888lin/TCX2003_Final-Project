-- DATABASE SETUP

CREATE DATABASE tcx2003;

USE tcx2003;


-- =========================
-- STUDENTS TABLE
-- =========================

CREATE TABLE students (

    username VARCHAR(50) PRIMARY KEY,

    password_hash TEXT NOT NULL

);


-- =========================
-- SESSIONS TABLE
-- =========================

CREATE TABLE sessions (

    session_id INT AUTO_INCREMENT PRIMARY KEY,

    username VARCHAR(50),

    session_token VARCHAR(255),

    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (username)
    REFERENCES students(username)

);