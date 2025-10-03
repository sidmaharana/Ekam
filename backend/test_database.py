import sqlite3

# Create a new SQLite database
conn = sqlite3.connect("D:\\SIDHARTH\\Projects\\Ekam\\backend\\test.db")
cursor = conn.cursor()

# Create employees table
cursor.execute("""
CREATE TABLE employees (
    emp_id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    dept_id INTEGER,
    position TEXT,
    annual_salary REAL,
    join_date DATE,
    office_location TEXT,
    FOREIGN KEY (dept_id) REFERENCES departments (dept_id)
);
""")

# Create departments table
cursor.execute("""
CREATE TABLE departments (
    dept_id INTEGER PRIMARY KEY,
    dept_name TEXT NOT NULL,
    manager_id INTEGER
);
""")

# Insert some data
cursor.execute("INSERT INTO departments (dept_id, dept_name, manager_id) VALUES (1, 'Engineering', 101)")
cursor.execute("INSERT INTO departments (dept_id, dept_name, manager_id) VALUES (2, 'HR', 102)")

cursor.execute("INSERT INTO employees (emp_id, full_name, dept_id, position, annual_salary, join_date, office_location) VALUES (1, 'John Doe', 1, 'Software Engineer', 100000, '2023-01-15', 'New York')")
cursor.execute("INSERT INTO employees (emp_id, full_name, dept_id, position, annual_salary, join_date, office_location) VALUES (2, 'Jane Smith', 1, 'Data Scientist', 120000, '2022-08-20', 'San Francisco')")
cursor.execute("INSERT INTO employees (emp_id, full_name, dept_id, position, annual_salary, join_date, office_location) VALUES (3, 'Peter Jones', 2, 'HR Manager', 90000, '2021-05-10', 'New York')")

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database created successfully.")
