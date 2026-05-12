-- =============================================
-- DATABASE SETUP
-- =============================================
CREATE DATABASE IF NOT EXISTS tcx2003;
USE tcx2003;

-- =============================================
-- 1. USERS TABLE (Modified)
-- =============================================
CREATE TABLE users (
    username VARCHAR(50) PRIMARY KEY,
    password_hash TEXT NOT NULL,
    role ENUM('student', 'teacher') NOT NULL DEFAULT 'student',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- Added to track password age for security policies
    password_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    -- Added to facilitate secure password recovery/reset flows
    reset_token VARCHAR(255) DEFAULT NULL,
    reset_token_expiry DATETIME DEFAULT NULL
);

-- =============================================
-- 2. SESSIONS TABLE
-- =============================================
CREATE TABLE sessions (
    session_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    session_token VARCHAR(255) NOT NULL,
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_user_session
        FOREIGN KEY (username) 
        REFERENCES users(username)
        ON DELETE CASCADE
);

-- =============================================
-- 3. SUBMISSIONS TABLE 
-- =============================================
CREATE TABLE submissions (
    submission_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    query_text TEXT NOT NULL,
    score INT DEFAULT 0,
    status VARCHAR(20) DEFAULT 'Pending',
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (username) 
    REFERENCES users(username)
    ON DELETE CASCADE
);