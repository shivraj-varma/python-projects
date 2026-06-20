# Student Management System

A simple Python + MySQL command-line project for managing student records, subject marks, and basic academic reports. It creates database tables automatically, stores student details in MySQL, and provides menu-driven operations such as add, update, delete, search, marks calculation, and JSON export.

## Project Overview

This project is a beginner-friendly student record management system built with Python and MySQL. The program connects to a local MySQL database named `school_db`, creates the required tables, and allows the user to manage student data from a terminal-based menu.

The system stores student identity data in a `students` table and subject-wise marks in a `marks` table. It then uses SQL queries to search records, calculate totals and averages, generate a full student report, and export data to a JSON file.

## What This Project Can Do

- Add a new student with roll number, name, class, and marks.
- Prevent duplicate roll numbers before inserting a student.
- Update existing student details and marks.
- Delete a student and that student's marks.
- Search a student by roll number.
- Calculate total marks, average marks, and grade.
- Show all students in a formatted report.
- Export student records to a JSON file.
- Create required MySQL tables automatically at startup.

## Features

| Feature | Description |
|---------|-------------|
| Database connection | Connects to MySQL using `mysql.connector` |
| Automatic table creation | Creates `students` and `marks` tables if they do not exist |
| Student CRUD operations | Add, update, search, and delete student records |
| Marks management | Stores marks for Science, Math, and English |
| Report generation | Shows student totals and averages |
| Grade system | Assigns grades based on total marks |
| JSON export | Saves records into `students_report.json` |
| Menu-driven interface | Easy to run in terminal for beginners |

## Tech Stack

- Python
- MySQL
- mysql-connector-python
- JSON

## Database Structure

### `students` table
- `roll_no` - Primary key
- `name` - Student name
- `class` - Student class
- `created_at` - Timestamp of record creation

### `marks` table
- `id` - Auto increment primary key
- `roll_no` - Foreign key linked to `students`
- `subject` - Subject name
- `marks` - Marks between 0 and 100

## Main Functions

### 1. `create_tables()`
Creates the required database tables when the program starts.

### 2. `add_students()`
Adds a new student record and inserts marks for Science, Math, and English.

### 3. `update_students()`
Updates existing student name, class, and subject marks.

### 4. `delete_student()`
Removes a student and related marks from the database.

### 5. `search_student()`
Fetches and displays student details by roll number.

### 6. `calculate_marks()`
Calculates total marks, average, and grade for a student.

### 7. `show_all_students()`
Displays all students in a tabular report with total and average marks.

### 8. `export_to_json()`
Exports student and marks data into a JSON file.

## Grade Logic

The project uses total marks out of 300 to assign grades:

- `A+` for 270 and above
- `A` for 240 to 269
- `B+` for 210 to 239
- `B` for 180 to 209
- `C` for 150 to 179
- `F` below 150

## How to Run

1. Install Python.
2. Install MySQL Server.
3. Create a database named `school_db`.
4. Install the required package:

```bash
pip install mysql-connector-python
```

5. Update the MySQL connection settings in `student_managemant.py` if needed:

```python
host = "localhost"
user = "root"
password = "your_password"
database = "school_db"
```

6. Run the project:

```bash
python student_managemant.py
```

## Menu Options

```text
1. Add Student
2. Update Student
3. Delete Student
4. Search Student
5. Calculate Total Marks
6. Show All Student
7. Export to JSON file
8. Exit
```

## Example Use Case

A school admin or beginner Python learner can use this project to manage student records from the terminal. It is useful for practicing Python functions, SQL integration, CRUD operations, joins, aggregates, and JSON export in one project.

## Strengths of This Project

- Good beginner project for Python + MySQL.
- Demonstrates real database connectivity.
- Covers CRUD operations clearly.
- Uses SQL joins, aggregate functions, and foreign keys.
- Can be shown in a GitHub portfolio as a database project.

## Current Limitations

- MySQL password is hardcoded in the source file.
- Input validation is limited.
- The update marks flow expects integer input and may fail if the user presses Enter.
- Export path is fixed to a local JSON file.
- No GUI or web interface yet.
- Only three subjects are currently supported.

## Suggested Improvements

- Move database credentials to environment variables.
- Add better exception handling and validation.
- Support more subjects dynamically.
- Add percentage and pass/fail status.
- Build a Tkinter or Flask interface.
- Add login/admin authentication.
- Generate CSV or PDF reports.
- Refactor into modules and classes for better structure.
