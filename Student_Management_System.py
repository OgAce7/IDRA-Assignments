def add_student(students):
    stud_id = input("Enter ID: ")
    name = input("Enter Name: ")
    age = input("Enter Age: ")
    course = input("Enter Course: ")
    marks = input("Enter Marks: ")
    
    student = {
        "id": stud_id,
        "name": name,
        "age": age,
        "course": course,
        "marks": marks
    }
    students.append(student)
    print("Student added successfully!")

def view_students(students):
    if not students:
        print("No student records found.")
        return
    print("\n--- Student Records ---")
    for s in students:
        print(f"ID: {s['id']} | Name: {s['name']} | Age: {s['age']} | Course: {s['course']} | Marks: {s['marks']}")

def search_student(students):
    query = input("Enter ID or Name to search: ").lower()
    found = [s for s in students if s['id'].lower() == query or s['name'].lower() == query]
    if found:
        print("\n--- Search Results ---")
        for s in found:
            print(f"ID: {s['id']} | Name: {s['name']} | Age: {s['age']} | Course: {s['course']} | Marks: {s['marks']}")
    else:
        print("No matching student found.")

def update_student(students):
    stud_id = input("Enter ID of the student to update: ")
    for s in students:
        if s['id'] == stud_id:
            print("Leave blank to keep existing value.")
            name = input(f"Enter new Name ({s['name']}): ")
            age = input(f"Enter new Age ({s['age']}): ")
            course = input(f"Enter new Course ({s['course']}): ")
            marks = input(f"Enter new Marks ({s['marks']}): ")
            
            if name: s['name'] = name
            if age: s['age'] = age
            if course: s['course'] = course
            if marks: s['marks'] = marks
            print("Student updated successfully!")
            return
    print("Student ID not found.")

def delete_student(students):
    stud_id = input("Enter ID of the student to delete: ")
    for s in students:
        if s['id'] == stud_id:
            students.remove(s)
            print("Student deleted successfully!")
            return
    print("Student ID not found.")

def main():
    students = []
    while True:
        print("\n=== Student Management System ===")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ")
        
        if choice == '1':
            add_student(students)
        elif choice == '2':
            view_students(students)
        elif choice == '3':
            search_student(students)
        elif choice == '4':
            update_student(students)
        elif choice == '5':
            delete_student(students)
        elif choice == '6':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()