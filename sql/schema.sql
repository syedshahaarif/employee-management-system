CREATE DATABASE IF NOT EXISTS employee_db;
USE employee_db;

CREATE TABLE IF NOT EXISTS departments (
    dept_id   INT AUTO_INCREMENT PRIMARY KEY,
    dept_name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS employees (
    emp_id      INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    email       VARCHAR(100) NOT NULL UNIQUE,
    phone       VARCHAR(15),
    designation VARCHAR(50),
    salary      DECIMAL(10,2) NOT NULL CHECK (salary >= 0),
    hire_date   DATE,
    dept_id     INT,
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
        ON DELETE SET NULL,
    INDEX idx_employees_dept (dept_id)
);

CREATE TABLE IF NOT EXISTS attendance (
    att_id   INT AUTO_INCREMENT PRIMARY KEY,
    emp_id   INT NOT NULL,
    att_date DATE NOT NULL,
    status   ENUM('Present','Absent','Leave') NOT NULL,
    UNIQUE (emp_id, att_date),
    FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
        ON DELETE CASCADE,
    INDEX idx_attendance_date (att_date)
);
