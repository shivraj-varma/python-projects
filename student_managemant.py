import mysql.connector
from mysql.connector import Error
import json
from datetime import datetime

# Function for connect sql database 
def get_connection():
    try:                                        # try except for error heandling
        connection = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "shivraj@001M",
            database = "school_db"
        )
        return connection
    except Error as e:
        print(f"Datebase connection error {e}")
        return None
    
# Creating database tables
def create_tables():
    connection = get_connection()
    if connection:
        cursor = connection.cursor()

        # student table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS students(
            roll_no INT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            class VARCHAR(20) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                       )
        """)
        
        # Marks table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS marks(
            id INT AUTO_INCREMENT PRIMARY KEY,
            roll_no INT,
            subject VARCHAR(50) NOT NULL,
            marks INT CHECK (marks >= 0 AND marks <= 100),
            FOREIGN KEY (roll_no) REFERENCES students(roll_no)
                       )
        """)

        connection.commit()
        cursor.close()
        connection.close()
        print("✅ Tables created successfully! ")  



# 1. Function for Add Students
def add_students():
    connection = get_connection()
    if not connection:
        return
    try:
        curser = connection.cursor()
        
        roll_no = int(input("Enter Roll Number: "))

        # Check if student already exists in database
        curser.execute("SELECT roll_no FROM students WHERE roll_no = %s", (roll_no,))
        if curser.fetchone():
            print(f"❌ Student with this roll number already existe!")
            return
        
        name = input("Enter Name: ").strip().title()
        sclass = input("Enter Class: ").strip().title()

        # Insert Students
        curser.execute(
                "INSERT INTO students (roll_no, name, class) VALUES (%s, %s, %s)",(roll_no, name, sclass)
        )

        # Insert marks
        subjects = ["science", "math", "english"]
        marks = []

        for subject in subjects:
            mark = int(input(f"Enter {subject.title()} marks (0-100): "))
            marks.append((roll_no, subject, mark))

        curser.executemany(
            "INSERT INTO marks (roll_no, subject, marks) VALUES (%s, %s, %s)", marks
        )

        connection.commit()
        print(f"✅ Student {name} (Roll Nomber: {roll_no}) Add Successfully!")

    except Error as e:
        print(f"❌Error adding student {e}")
    finally:
        curser.close()
        connection.close()


# 2. Function for Update Students

def update_students():
    connection = get_connection()
    if not connection:
        return
    
    try:
        curser = connection.cursor()

        roll_no = int(input("Enter Roll Number to Update: "))

        # check if student Exists in database
        curser.execute("SELECT name FROM students WHERE roll_no =%s",(roll_no,))
        student = curser.fetchone()
        if not student:
            print("❌ Student Not Found!")
            return
        print(f"Updating {student[0]}...")

        # Update Student Information
        name = input("Enter New Name (or press Enter to keep current): ").strip().title()
        sclass = input("Enter New Class (or press Enter to keep current): ").strip().title()

        if name:
            curser.execute("UPDATE students SET name = %s WHERE roll_no = %s",(name, roll_no))
        if sclass:
            curser.execute("UPDATE students SET class = %s WHERE roll_no = %s",(sclass, roll_no))

        # Updating Marks
        subjects = ["science", "math", "english"]
        for subject in subjects:
            new_marks = int(input(f"Enter New {subject.title()} Marks (or press Enter to keep current): "))

            if new_marks:
                curser.execute("UPDATE marks SET marks = %s WHERE roll_no = %s AND subject = %s",
                (new_marks, roll_no, subject))
        
        connection.commit()
        print("✅ Student updated successfully!")

    except Error as e:
        print(f"❌ Error updating student: {e}")
    finally:
        curser.close()
        connection.close()

# 3. DELETE Student
def delete_student():
    connection = get_connection()
    if not connection:
        return
    try:
        curser = connection.cursor()
        roll_no = int(input("Enter Roll Number to Delete: "))

        # check if student Exists in database
        curser.execute("SELECT name FROM students WHERE roll_no =%s",(roll_no,))
        student = curser.fetchone()
        if not student:
            print("❌ Student Not Found!")
            return

        curser.execute("DELETE FROM marks WHERE roll_no = %s",(roll_no,))
        curser.execute("DELETE FROM students WHERE roll_no = %s",(roll_no,))

        connection.commit()
        print("✅ Student Deleted Successfully!")

    except Error as e:
        print(f"❌ Error deleting Student: {e}")
    finally:
        curser.close()
        connection.close()

# 4. SEARCH Student
def search_student():
    connection = get_connection()
    if not connection:
        return
    
    try:
        cursor = connection.cursor()
        roll_no = int(input("Enter Roll Number to Search Student: "))

        cursor.execute("SELECT name FROM students WHERE roll_no = %s", (roll_no,))
        student = cursor.fetchone()
        if not student:
            print("❌ Student Not Found!")
            return
        
        cursor.execute("""
        SELECT s.roll_no, s.name, s.class, m.subject, m.marks 
        FROM students s 
        LEFT JOIN marks m ON s.roll_no = m.roll_no 
        WHERE s.roll_no = %s
        """, (roll_no,))

        result = cursor.fetchall()

        if result:
            print(f"\n📋 Student Details (Roll Number {roll_no}):")
            print("-" * 50)
            for row in result:
                print(f"Name: {row[1]}, Class: {row[2]}, {row[3].title()}: {row[4]}")
        else:
            print("❌ Student not found!")

    finally:
        cursor.close()
        connection.close()


# 5. Calculate Total Marks
def calculate_marks():
    connection = get_connection()
    if not connection:
        return
    
    try:
        cursor = connection.cursor()
        roll_no = int(input("Enter Roll Number: "))

        cursor.execute("""
        SELECT s.name, SUM(m.marks) as total_marks, 
               AVG(m.marks) as average_marks
        FROM students s 
        JOIN marks m ON s.roll_no = m.roll_no 
        WHERE s.roll_no = %s
        GROUP BY s.roll_no, s.name
        """,(roll_no,))

        result = cursor.fetchone()
        if result:
            print(f"\n Marks Sumary for {result[0]}")
            print(f"Total Marks: {result[1]}/300")
            print(f"Average: {result[2]:.2f}/100")
            grade = get_grade(result[1])
            print(f"Grade {grade}")
        else:
            print(f"❌ Student Not Found!")
    except Error as e:
        print(e)

    finally:
        cursor.close()
        connection.close()


def get_grade(total_marks):
    if total_marks >= 270: 
        return "A+"
    elif total_marks >= 240:
        return "A"
    elif total_marks >= 210:
        return "B+"
    elif total_marks >= 180:
        return "B"
    elif total_marks >= 150:
        return "C"
    else:
        return "F"
    
# 6. Show All Students
def show_all_students():
    connection = get_connection()
    if not connection:
        return
    
    try:
        cursor = connection.cursor()
        cursor.execute("""
        SELECT s.roll_no, s.name, s.class,
        SUM(m.marks) as total, AVG(m.marks) as avg
        FROM students s
        LEFT JOIN marks m ON s.roll_no = m.roll_no
        GROUP BY s.roll_no
        """)

        result = cursor.fetchall()
        if result:
            print(f"\n📚 ALL STUDENTS REPORT")
            print("="*80)
            print(f"{'Roll No':<8} {'Name':<15} {'Class':<10} {'Total':<8} {'Avg':<8}")
            print("=" * 80)
            for row in result:
                print(f"{row[0]:<8} {row[1]:<15} {row[2]:<10} {row[3]:<8} {row[4]:<6.1f}")

        else:
            print("No Student found!")


    except Error as e:
        print(e)
    finally:
        cursor.close()
        connection.close()

# 7. Export to JSON 
def export_to_json():
    connection = get_connection()
    if not connection:
        return
    
    try:
        cursor = connection.cursor()
        cursor.execute("""
        SELECT s.roll_no, s.name, s.class, m.subject, m.marks 
        FROM students s 
        LEFT JOIN marks m ON s.roll_no = m.roll_no 
        ORDER BY s.roll_no
        """)
        
        data = {}
        for row in cursor.fetchall():
            roll_no = row[0]
            if roll_no not in data:
                data[roll_no] = {
                    "name": row[1],
                    "class": row[2],
                    "marks": {}
                }
            data[roll_no]["marks"][row[3]] = row[4]
        
        with open("students_report.json", "w") as f:
            json.dump(data, f, indent=4)
        
        print("✅ Data exported to students_report.json")
        
    finally:
        cursor.close()
        connection.close()


# main menu
def main():
    print("🎓 STUDENT MANAGEMENT SYSTEM")
    print("="*40)

                    # Create tables first time
    create_tables()

    while True:
        print("\n📋 MENU:")
        print("1. Add Student")
        print("2. Updete Student")
        print("3. Delete Student")
        print("4. Search Student")
        print("5. Calculate Total Marks")
        print("6. Show All Student")
        print("7. Export to JSON file")
        print("8. Exit")

        
        choice = input("\nEnter choice (0-7): ").strip()

        if choice == "1":
            add_students()
        elif choice == "2":
            update_students()
        elif choice == "3":
            delete_student()
        elif choice == "4":
            search_student()
        elif choice == "5":
            calculate_marks()
        elif choice == "6":
            show_all_students()
        elif choice == "7":
            export_to_json()
        elif choice == "8":
            break

        else:
            print("❌ Invalid Choice! Try Again")

if __name__ == "__main__":
    main()

