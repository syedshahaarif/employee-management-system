USE employee_db;

-- 1. Salary rank of every employee inside their department (window function)
SELECT d.dept_name, e.name, e.salary,
       RANK() OVER (PARTITION BY e.dept_id ORDER BY e.salary DESC) AS dept_rank
FROM employees e
JOIN departments d ON e.dept_id = d.dept_id
ORDER BY d.dept_name, dept_rank;

-- 2. Employees earning more than their department average (CTE)
WITH dept_avg AS (
    SELECT dept_id, AVG(salary) AS avg_salary
    FROM employees
    GROUP BY dept_id
)
SELECT e.name, d.dept_name, e.salary, ROUND(a.avg_salary, 0) AS dept_avg_salary
FROM employees e
JOIN dept_avg a ON e.dept_id = a.dept_id
JOIN departments d ON e.dept_id = d.dept_id
WHERE e.salary > a.avg_salary
ORDER BY e.salary DESC;

-- 3. Hiring trend: number of hires per year
SELECT YEAR(hire_date) AS hire_year, COUNT(*) AS hires
FROM employees
GROUP BY YEAR(hire_date)
ORDER BY hire_year;

-- 4. Attendance percentage per employee
SELECT e.name,
       COUNT(a.att_id) AS days_recorded,
       ROUND(100 * SUM(a.status = 'Present') / COUNT(a.att_id), 1) AS attendance_pct
FROM employees e
JOIN attendance a ON e.emp_id = a.emp_id
GROUP BY e.emp_id, e.name
ORDER BY attendance_pct DESC;

-- 5. Total salary cost and headcount by department
SELECT d.dept_name, COUNT(e.emp_id) AS headcount, SUM(e.salary) AS total_salary_cost
FROM departments d
LEFT JOIN employees e ON d.dept_id = e.dept_id
GROUP BY d.dept_name
ORDER BY total_salary_cost DESC;
