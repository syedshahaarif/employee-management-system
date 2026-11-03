# Employee Management System

A web-based HR application to manage employees, departments and attendance, built with **MySQL**, **Python** and **Streamlit**. It also includes a **SQL Analytics** page that runs window-function and CTE queries on the data.

## Features

- **Dashboard** with headcount, average salary, monthly payroll and department charts
- **Employee CRUD**: add, search, filter, update and delete (with confirmation)
- **Input validation** for name, email, phone and salary, with friendly duplicate-email handling
- **Attendance** marking (Present / Absent / Leave) with a summary report
- **Departments** management
- **SQL Analytics**: salary ranking per department, above-average earners, hiring trend, attendance percentage
- **CSV export** of employee data
- **Optional password login** via environment variable
- **Secure by design**: parameterised queries (no SQL injection) and credentials kept in `.env`

## Tech Stack

| Layer | Technology |
|---|---|
| Database | MySQL 8 |
| Backend | Python 3.9+, mysql-connector-python (connection pooling) |
| UI | Streamlit |
| Data handling | Pandas |
| Testing | pytest |

## Project Structure

```
employee-management-system/
├── app.py                 # Entry point and navigation
├── ems/
│   ├── config.py          # Loads settings from .env
│   ├── db.py              # Connection pool and query helpers
│   ├── auth.py            # Optional password login
│   ├── utils.py           # Input validation
│   └── views/             # One file per page
├── sql/
│   ├── schema.sql         # Tables, constraints, indexes
│   ├── seed.sql           # Sample data
│   └── analytics.sql      # Analytical queries
├── tests/                 # Unit tests
├── docs/screenshots/      # Add your screenshots here
├── requirements.txt
└── .env.example
```

## Database Design

```
departments (1) ──< employees (1) ──< attendance
```

- `employees.dept_id` references `departments` with `ON DELETE SET NULL`
- `attendance.emp_id` references `employees` with `ON DELETE CASCADE`
- `UNIQUE (emp_id, att_date)` prevents duplicate attendance for a day
- `UNIQUE` email, `CHECK (salary >= 0)` and indexes on foreign key and date columns

## Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/employee-management-system.git
   cd employee-management-system
   ```
2. **Create the database** (MySQL 8 required)
   ```bash
   mysql -u root -p < sql/schema.sql
   mysql -u root -p < sql/seed.sql
   ```
3. **Create a virtual environment and install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
4. **Configure environment variables**
   ```bash
   cp .env.example .env            # Windows: copy .env.example .env
   ```
   Open `.env` and set your MySQL password.
5. **Run the app**
   ```bash
   streamlit run app.py
   ```
   Open http://localhost:8501

## Running Tests

```bash
pytest
```

## Screenshots

Add screenshots to `docs/screenshots/` and link them here:


<img width="1366" height="768" alt="Dashboard" src="https://github.com/user-attachments/assets/24d4b1f3-250c-4409-8016-d084efa8684d" />



## SQL Concepts Demonstrated

`PRIMARY KEY`, `FOREIGN KEY`, `UNIQUE`, `CHECK`, indexes, `JOIN` and `LEFT JOIN`, `GROUP BY` with aggregates, window functions (`RANK() OVER`), CTEs (`WITH`), `INSERT ... ON DUPLICATE KEY UPDATE`, and parameterised queries.

## Future Improvements

- Role-based access (admin / HR)
- Payroll and salary slip generation
- Leave request and approval workflow
- Excel / PDF report export
- Docker setup for one-command start

## License

MIT License. See [LICENSE](LICENSE).
