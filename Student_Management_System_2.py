import csv
import os
from datetime import datetime

FILENAME = "expenses.csv"

def initialize_file():
    """Ensure the CSV file exists with headers if it doesn't already."""
    if not os.path.exists(FILENAME):
        with open(FILENAME, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Amount", "Note"])

def add_expense():
    """Add a new expense record to the CSV file."""
    print("\n--- Add New Expense ---")
    
    # Date Input
    date_str = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
    if not date_str:
        date_str = datetime.now().strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Using today's date instead.")
            date_str = datetime.now().strftime("%Y-%m-%d")

    # Category Input
    category = input("Enter category (e.g., Food, Transport, Utilities): ").strip().capitalize()
    if not category:
        category = "General"

    # Amount Input
    while True:
        try:
            amount = float(input("Enter amount ($): "))
            if amount < 0:
                print("Amount cannot be negative. Try again.")
                continue
            break
        except ValueError:
            print("Invalid input! Please enter a valid number for the amount.")

    # Optional Note Input
    note = input("Enter an optional note (or leave blank): ").strip()

    # Save to CSV
    try:
        with open(FILENAME, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([date_str, category, f"{amount:.2f}", note])
        print("Expense added successfully!")
    except IOError:
        print("Error: Could not save expense to file.")

def view_expenses():
    """Display all recorded expenses and the total amount spent."""
    print("\n--- All Expenses ---")
    if not os.path.exists(FILENAME):
        print("No expense records found.")
        return

    total_spent = 0.0
    has_records = False

    try:
        with open(FILENAME, mode="r") as file:
            reader = csv.reader(file)
            header = next(reader, None)
            
            if not header:
                print("No expense records found.")
                return

            print(f"{'Date':<12} | {'Category':<15} | {'Amount ($)':<12} | {'Note'}")
            print("-" * 60)

            for row in reader:
                if len(row) < 4:
                    continue
                has_records = True
                date, category, amount, note = row
                total_spent += float(amount)
                print(f"{date:<12} | {category:<15} | {amount:<12} | {note}")

        if not has_records:
            print("No expense records found.")
        else:
            print("-" * 60)
            print(f"Total Amount Spent: ${total_spent:.2f}\n")

    except IOError:
        print("Error: Could not read expense file.")

def view_category_summary():
    """Display a category-wise spending summary."""
    print("\n--- Category-Wise Spending Summary ---")
    if not os.path.exists(FILENAME):
        print("No expense records found.")
        return

    category_totals = {}

    try:
        with open(FILENAME, mode="r") as file:
            reader = csv.reader(file)
            header = next(reader, None)
            
            if not header:
                print("No expense records found.")
                return

            for row in reader:
                if len(row) < 4:
                    continue
                _, category, amount, _ = row
                amount = float(amount)
                category_totals[category] = category_totals.get(category, 0.0) + amount

        if not category_totals:
            print("No expense records found.")
            return

        print(f"{'Category':<20} | {'Total Spent ($)'}")
        print("-" * 40)
        for category, total in category_totals.items():
            print(f"{category:<20} | ${total:.2f}")
        print("-" * 40)

    except IOError:
        print("Error: Could not read expense file.")

def main():
    initialize_file()
    while True:
        print("\n=== Expense Tracker Application ===")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. View Category-Wise Summary")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            view_category_summary()
        elif choice == '4':
            print("Exiting Expense Tracker. Goodbye!")
            break
        else:
            print("Invalid choice! Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()