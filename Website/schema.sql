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
-- 3. ASSESSMENTS TABLE (New)
-- =============================================
-- Groups multiple tasks together (e.g., "Lab 1", "Final Exam")
CREATE TABLE assessments (
    aid INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    due_date DATETIME NOT NULL,
    description TEXT
);

-- =============================================
-- 4. TASKS TABLE (New)
-- =============================================
-- Specific questions or coding challenges within an assessment
CREATE TABLE tasks (
    tid INT AUTO_INCREMENT PRIMARY KEY,
    aid INT NOT NULL,
    task_name VARCHAR(255) NOT NULL,
    max_score INT DEFAULT 10,
    CONSTRAINT fk_assessment_task FOREIGN KEY (aid) 
        REFERENCES assessments(aid) ON DELETE CASCADE
);

-- =============================================
-- 5. SUBMISSIONS TABLE (Modified for 3NF)
-- =============================================
CREATE TABLE submissions (
    submission_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    tid INT NOT NULL,  -- Linked to Task instead of Assessment to avoid transitive dependency
    query_text TEXT NOT NULL,
    score INT DEFAULT 0,
    status VARCHAR(20) DEFAULT 'Pending',
    attempt_number INT DEFAULT 1,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_user_submission FOREIGN KEY (username) 
        REFERENCES users(username) ON DELETE CASCADE,
    CONSTRAINT fk_task_submission FOREIGN KEY (tid) 
        REFERENCES tasks(tid) ON DELETE CASCADE
);