USE employee_db;

INSERT IGNORE INTO departments (dept_name) VALUES
('Human Resources'), ('Engineering'), ('Sales'), ('Finance');

INSERT IGNORE INTO employees (name, email, phone, designation, salary, hire_date, dept_id)
SELECT s.name, s.email, s.phone, s.designation, s.salary, s.hire_date, d.dept_id
FROM (
    SELECT 'Rahul Sharma' AS name, 'rahul@example.com' AS email, '9876543210' AS phone, 'Software Engineer' AS designation, 60000 AS salary, '2023-04-10' AS hire_date, 'Engineering' AS dept
    UNION ALL SELECT 'Neha Gupta', 'neha@example.com', '9876500001', 'Senior Engineer', 95000, '2020-06-15', 'Engineering'
    UNION ALL SELECT 'Karan Mehta', 'karan@example.com', '9876500002', 'Data Engineer', 78000, '2022-02-01', 'Engineering'
    UNION ALL SELECT 'Priya Verma', 'priya@example.com', '9123456780', 'HR Executive', 45000, '2022-08-01', 'Human Resources'
    UNION ALL SELECT 'Sunita Rao', 'sunita@example.com', '9123400003', 'HR Manager', 72000, '2019-03-20', 'Human Resources'
    UNION ALL SELECT 'Amit Singh', 'amit@example.com', '9988776655', 'Sales Manager', 70000, '2021-01-15', 'Sales'
    UNION ALL SELECT 'Pooja Nair', 'pooja@example.com', '9988700004', 'Sales Executive', 38000, '2024-01-08', 'Sales'
    UNION ALL SELECT 'Vikram Joshi', 'vikram@example.com', '9988700005', 'Sales Executive', 41000, '2023-09-12', 'Sales'
    UNION ALL SELECT 'Anjali Desai', 'anjali@example.com', '9000000006', 'Accountant', 52000, '2021-11-05', 'Finance'
    UNION ALL SELECT 'Rohit Kulkarni', 'rohit@example.com', '9000000007', 'Finance Manager', 88000, '2018-07-23', 'Finance'
) s
JOIN departments d ON d.dept_name = s.dept;

-- Sample attendance for 5 days (deterministic pattern)
INSERT IGNORE INTO attendance (emp_id, att_date, status)
SELECT e.emp_id, d.dt,
       CASE WHEN (e.emp_id + DAY(d.dt)) % 7 = 0 THEN 'Absent'
            WHEN (e.emp_id + DAY(d.dt)) % 11 = 0 THEN 'Leave'
            ELSE 'Present' END
FROM employees e
CROSS JOIN (
    SELECT '2026-10-01' AS dt UNION ALL SELECT '2026-10-02'
    UNION ALL SELECT '2026-10-05' UNION ALL SELECT '2026-10-06'
    UNION ALL SELECT '2026-10-07'
) d;
