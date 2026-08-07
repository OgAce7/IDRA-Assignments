import csv
import os
from datetime import datetime, timedelta

FILENAME = "library_data.csv"

class Book:
    """Represents an individual book in the library."""
    def __init__(self, book_id, title, author, category, total_copies, available_copies=None):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.category = category
        self.total_copies = int(total_copies)
        self.available_copies = int(total_copies) if available_copies is None else int(available_copies)

    def to_list(self):
        return [self.book_id, self.title, self.author, self.category, self.total_copies, self.available_copies]

class Member:
    """Represents a library member."""
    def __init__(self, member_id, name, borrowed_books=None):
        self.member_id = member_id
        self.name = name
        # Stored as a dictionary or list of borrowed details: {book_id: due_date_str}
        self.borrowed_books = borrowed_books if borrowed_books is not None else {}

    def to_dict_string(self):
        # Convert borrowed_books dict to a formatted string for CSV storage (ID:Date;ID:Date)
        return ";".join([f"{b_id}:{due}" for b_id, due in self.borrowed_books.items()])

class Library:
    """Manages books, members, and all core library operations."""
    def __init__(self):
        self.books = {}
        self.members = {}
        self.load_data()

    def load_data(self):
        """Loads books and members data from the CSV file."""
        if not os.path.exists(FILENAME):
            return
        
        try:
            with open(FILENAME, mode="r", newline="") as file:
                reader = csv.reader(file)
                section = None
                for row in reader:
                    if not row:
                        continue
                    if row[0] == "#BOOKS":
                        section = "BOOKS"
                        continue
                    elif row[0] == "#MEMBERS":
                        section = "MEMBERS"
                        continue

                    if section == "BOOKS" and len(row) >= 6:
                        b_id, title, author, cat, total, avail = row
                        self.books[b_id] = Book(b_id, title, author, cat, total, avail)
                    elif section == "MEMBERS" and len(row) >= 3:
                        m_id, name, b_str = row[0], row[1], row[2]
                        borrowed = {}
                        if b_str:
                            for item in b_str.split(";"):
                                if ":" in item:
                                    b_id, due = item.split(":")
                                    borrowed[b_id] = due
                        self.members[m_id] = Member(m_id, name, borrowed)
        except IOError:
            print("Error: Could not load data from file.")

    def save_data(self):
        """Saves current state of books and members to the CSV file."""
        try:
            with open(FILENAME, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["#BOOKS"])
                for book in self.books.values():
                    writer.writerow(book.to_list())
                
                writer.writerow(["#MEMBERS"])
                for member in self.members.values():
                    writer.writerow([member.member_id, member.name, member.to_dict_string()])
        except IOError:
            print("Error: Could not save data to file.")

    def add_book(self):
        print("\n--- Add New Book ---")
        book_id = input("Enter Book ID: ").strip()
        if not book_id:
            print("Book ID cannot be empty.")
            return
        if book_id in self.books:
            print("A book with this ID already exists.")
            return

        title = input("Enter Title: ").strip().title()
        author = input("Enter Author: ").strip().title()
        category = input("Enter Category (e.g., Fiction, Science, History): ").strip().capitalize()
        
        while True:
            try:
                total_copies = int(input("Enter Total Copies: "))
                if total_copies < 1:
                    print("Copies must be at least 1.")
                    continue
                break
            except ValueError:
                print("Invalid input! Please enter an integer.")

        self.books[book_id] = Book(book_id, title, author, category, total_copies)
        self.save_data()
        print(f"Book '{title}' added successfully!")

    def register_member(self):
        print("\n--- Register New Member ---")
        member_id = input("Enter Member ID: ").strip()
        if not member_id:
            print("Member ID cannot be empty.")
            return
        if member_id in self.members:
            print("A member with this ID already exists.")
            return

        name = input("Enter Member Name: ").strip().title()
        self.members[member_id] = Member(member_id, name)
        self.save_data()
        print(f"Member '{name}' registered successfully!")

    def view_books(self):
        print("\n--- Library Catalog ---")
        if not self.books:
            print("No books available in the library.")
            return

        print(f"{'ID':<10} | {'Title':<25} | {'Author':<20} | {'Category':<15} | {'Avail/Total'}")
        print("-" * 85)
        for book in self.books.values():
            print(f"{book.book_id:<10} | {book.title:<25} | {book.author:<20} | {book.category:<15} | {book.available_copies}/{book.total_copies}")

    def search_books(self):
        print("\n--- Search Books ---")
        query = input("Enter keyword (Title, Author, or Category): ").strip().lower()
        if not query:
            print("Search query cannot be empty.")
            return

        results = [b for b in self.books.values() if query in b.title.lower() or query in b.author.lower() or query in b.category.lower()]
        
        if not results:
            print("No matching books found.")
            return

        print(f"\nFound {len(results)} match(es):")
        print(f"{'ID':<10} | {'Title':<25} | {'Author':<20} | {'Category':<15} | {'Available'}")
        print("-" * 85)
        for book in results:
            print(f"{book.book_id:<10} | {book.title:<25} | {book.author:<20} | {book.category:<15} | {book.available_copies}")

    def issue_book(self):
        print("\n--- Issue Book ---")
        member_id = input("Enter Member ID: ").strip()
        if member_id not in self.members:
            print("Member ID not found. Please register first.")
            return

        book_id = input("Enter Book ID to issue: ").strip()
        if book_id not in self.books:
            print("Book ID not found.")
            return

        book = self.books[book_id]
        member = self.members[member_id]

        if book_id in member.borrowed_books:
            print("This member has already borrowed a copy of this book.")
            return

        if book.available_copies > 0:
            book.available_copies -= 1
            due_date = datetime.now() + timedelta(days=14) # 2 weeks borrowing period
            member.borrowed_books[book_id] = due_date.strftime("%Y-%m-%d")
            self.save_data()
            print(f"Book '{book.title}' issued successfully! Due date: {due_date.strftime('%Y-%m-%d')}")
        else:
            print("Sorry, all copies of this book are currently checked out.")

    def return_book(self):
        print("\n--- Return Book ---")
        member_id = input("Enter Member ID: ").strip()
        if member_id not in self.members:
            print("Member ID not found.")
            return

        member = self.members[member_id]
        if not member.borrowed_books:
            print("This member has no books checked out.")
            return

        print("\nCurrently Borrowed Books:")
        for b_id, due in member.borrowed_books.items():
            book_title = self.books[b_id].title if b_id in self.books else "Unknown"
            print(f"Book ID: {b_id} | Title: {book_title} | Due Date: {due}")

        book_id = input("Enter Book ID to return: ").strip()
        if book_id not in member.borrowed_books:
            print("This book is not listed under this member's borrowed items.")
            return

        due_date_str = member.borrowed_books[book_id]
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
        current_date = datetime.now()

        # Fine calculation: $1 per day overdue
        fine = 0
        if current_date > due_date:
            overdue_days = (current_date - due_date).days
            fine = overdue_days * 1
            print(f"Book is overdue by {overdue_days} day(s). Late Fine: ${fine}")
        else:
            print("Book returned on time. No fine incurred.")

        # Update records
        del member.borrowed_books[book_id]
        if book_id in self.books:
            self.books[book_id].available_copies += 1

        self.save_data()
        print("Book returned successfully!")

def main():
    library = Library()
    
    while True:
        print("\n==============================")
        print("   LIBRARY MANAGEMENT SYSTEM  ")
        print("==============================")
        print("1. Add New Book")
        print("2. Register New Member")
        print("3. View Catalog")
        print("4. Search Books")
        print("5. Issue Book")
        print("6. Return Book")
        print("7. Exit")
        
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == '1':
            library.add_book()
        elif choice == '2':
            library.register_member()
        elif choice == '3':
            library.view_books()
        elif choice == '4':
            library.search_books()
        elif choice == '5':
            library.issue_book()
        elif choice == '6':
            library.return_book()
        elif choice == '7':
            print("Exiting Library System. Have a great day!")
            break
        else:
            print("Invalid choice! Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main()