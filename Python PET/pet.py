
import csv
import os
import sys
from datetime import datetime

if os.environ.get("DISPLAY", "") == "" and os.name != "nt":
    import matplotlib
    matplotlib.use("Agg")

import matplotlib.pyplot as plt

# Expense data file stored next to this script so it works from any working directory.
FILE_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expenses.csv")

# Available expense categories
CATEGORIES = [
    "Food",
    "Transport",
    "Education",
    "Shopping",
    "Entertainment",
    "Bills",
    "Others"
]


# MODULE 1: TRACK DAILY EXPENSES

def initialize_file():
    """Create CSV file if it does not exist."""
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                ["Date", "Amount", "Category", "Description"]
            )


def add_expense():
    """Add a new daily expense."""
    print("\n--- Add Daily Expense ---")

    while True:
        date = input(
            "Enter date (YYYY-MM-DD) or press Enter for today: "
        ).strip()

        if date == "":
            date = datetime.today().strftime("%Y-%m-%d")
            break

        try:
            datetime.strptime(date, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date! Example: 2026-10-13")

    while True:
        try:
            amount = float(input("Enter amount (Rs.): "))
            if amount <= 0:
                print("Amount must be greater than zero.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    print("\nAvailable Categories:")
    for i, category in enumerate(CATEGORIES, start=1):
        print(f"{i}. {category}")

    while True:
        try:
            choice = int(input("Choose category number: "))
            if 1 <= choice <= len(CATEGORIES):
                category = CATEGORIES[choice - 1]
                break
            print("Choose a number from the list.")
        except ValueError:
            print("Please enter a valid number.")

    description = input("Enter description: ").strip()

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, amount, category, description])

    print("Expense added successfully!")


def view_expenses():
    """Display all saved expenses."""
    print("\n--- All Expenses ---")

    with open(FILE_NAME, "r", newline="") as file:
        reader = csv.DictReader(file)
        expenses = list(reader)

    if not expenses:
        print("No expenses recorded yet.")
        return

    total = 0

    for expense in expenses:
        amount = float(expense["Amount"])
        total += amount

        print(
            f"Date: {expense['Date']} | "
            f"Amount: Rs. {amount:.2f} | "
            f"Category: {expense['Category']} | "
            f"Description: {expense['Description']}"
        )

    print(f"\nTotal Expenses: Rs. {total:.2f}")


# MODULE 2: CATEGORIZE EXPENSES

def categorize_expenses():
    """Display category-wise expense totals."""
    print("\n--- Category-wise Expenses ---")

    category_totals = {category: 0.0 for category in CATEGORIES}

    with open(FILE_NAME, "r", newline="") as file:
        reader = csv.DictReader(file)

        for expense in reader:
            category = expense["Category"]
            amount = float(expense["Amount"])

            if category in category_totals:
                category_totals[category] += amount

    for category, total in category_totals.items():
        print(f"{category}: Rs. {total:.2f}")


# MODULE 3: CALCULATE AND ANALYZE EXPENSES

def analyze_expenses():
    """Calculate total and monthly expenses."""
    print("\n--- Expense Analysis ---")

    expenses = []

    with open(FILE_NAME, "r", newline="") as file:
        reader = csv.DictReader(file)
        expenses = list(reader)

    if not expenses:
        print("No expenses available for analysis.")
        return

    total_expense = 0.0
    monthly_totals = {}

    for expense in expenses:
        amount = float(expense["Amount"])
        date = datetime.strptime(
            expense["Date"], "%Y-%m-%d"
        )

        month = date.strftime("%Y-%m")

        total_expense += amount
        monthly_totals[month] = (
            monthly_totals.get(month, 0.0) + amount
        )

    print(f"Total Spending: Rs. {total_expense:.2f}")

    average = total_expense / len(expenses)
    print(f"Average Expense per Entry: Rs. {average:.2f}")

    print("\nMonthly Spending:")
    for month, amount in sorted(monthly_totals.items()):
        print(f"{month}: Rs. {amount:.2f}")


# MODULE 4: MONTHLY VISUAL REPORT

def monthly_report():
    """Generate charts for a selected month."""
    print("\n--- Monthly Visual Report ---")

    month = input(
        "Enter month (YYYY-MM), e.g. 2026-10: "
    ).strip()

    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Invalid month! Use YYYY-MM format.")
        return

    category_totals = {category: 0.0 for category in CATEGORIES}
    daily_totals = {}

    with open(FILE_NAME, "r", newline="") as file:
        reader = csv.DictReader(file)

        for expense in reader:
            if expense["Date"].startswith(month):
                amount = float(expense["Amount"])
                category = expense["Category"]
                day = expense["Date"][-2:]

                if category in category_totals:
                    category_totals[category] += amount

                daily_totals[day] = (
                    daily_totals.get(day, 0.0) + amount
                )

    # Remove categories with no spending
    category_totals = {
        category: amount
        for category, amount in category_totals.items()
        if amount > 0
    }

    if not daily_totals:
        print("No expenses found for this month.")
        return

    # Create two charts
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Pie chart: category-wise spending
    if category_totals:
        axes[0].pie(
            category_totals.values(),
            labels=category_totals.keys(),
            autopct="%1.1f%%",
            startangle=90
        )
        axes[0].set_title("Category-wise Expenses")

    # Bar chart: day-wise spending
    days = sorted(daily_totals.keys())
    amounts = [daily_totals[day] for day in days]

    axes[1].bar(days, amounts)
    axes[1].set_title("Daily Expenses")
    axes[1].set_xlabel("Day of Month")
    axes[1].set_ylabel("Amount (Rs.)")

    fig.suptitle(f"Personal Expenses Report - {month}")
    plt.tight_layout()

    plt.savefig("monthly_report.png")
    print("Report saved as monthly_report.png")

    plt.show()


# MAIN MENU

def main():
    initialize_file()

    while True:
        print("\n===== PERSONAL EXPENSES TRACKER =====")
        print("1. Add Daily Expense")
        print("2. View All Expenses")
        print("3. Categorize Expenses")
        print("4. Analyze Expenses")
        print("5. Generate Monthly Visual Report")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            categorize_expenses()
        elif choice == "4":
            analyze_expenses()
        elif choice == "5":
            monthly_report()
        elif choice == "6":
            print("Thank you for using Personal Expenses Tracker!")
            break
        else:
            print("Invalid choice! Please select 1 to 6.")


# Program execution starts here
if __name__ == "__main__":
    main()
