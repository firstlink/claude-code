"""Command-line interface for the expense tracker."""

from typing import Optional

from .expense_tracker import ExpenseTracker


class ExpenseCLI:
    """Command-line interface for expense tracking."""

    def __init__(self) -> None:
        """Initialize the CLI with an expense tracker."""
        self.tracker = ExpenseTracker()

    def display_menu(self) -> None:
        """Display the main menu options."""
        total_expenses = len(self.tracker.get_all_expenses())
        total_spending = self.tracker.get_total_spending()

        print("\n" + "═" * 35)
        print("         💰 EXPENSE TRACKER 💰")
        print("═" * 35)
        print(f"📊 Total expenses: {total_expenses}")
        print(f"💷 Total spending: £{total_spending:.2f}")
        print("─" * 35)
        print("1. 📝 Add new expense")
        print("2. 📋 View all expenses")
        print("3. 📈 View last 30 days")
        print("4. 📊 View total spending")
        print("5. 🏷️  View spending by category")
        print("6. 🔍 Filter by category")
        print("7. 🚪 Exit")
        print("═" * 35)

    def add_expense_interactive(self) -> None:
        """Interactive prompt to add a new expense."""
        amount = self._get_valid_amount()
        if amount is None:
            return

        category = self._get_valid_category()
        if not category:
            return

        description = input("Enter description: ").strip()
        if not description:
            print("Description cannot be empty.")
            return

        self.tracker.add_expense(amount, category, description)
        print(f"✓ Added expense: £{amount:.2f} for {category}")

    def _get_valid_amount(self) -> Optional[float]:
        """Get and validate expense amount from user input.

        Returns:
            Valid amount or None if invalid
        """
        while True:
            try:
                amount_str = input("Enter amount (£): ").strip()

                if not amount_str:
                    print("Amount cannot be empty.")
                    continue

                # Remove £ symbol if present
                amount_str = amount_str.replace("£", "").replace(",", "")

                amount = float(amount_str)

                if amount <= 0:
                    print("Amount must be positive.")
                    continue

                if amount > 1000000:  # Reasonable upper limit
                    print("Amount seems unusually large. Please confirm.")
                    confirm = input("Continue? (y/N): ").strip().lower()
                    if confirm != 'y':
                        continue

                return round(amount, 2)  # Round to 2 decimal places

            except ValueError:
                print("Invalid amount. Please enter a valid number (e.g., 10.50).")
                retry = input("Try again? (Y/n): ").strip().lower()
                if retry == 'n':
                    return None

    def _get_valid_category(self) -> Optional[str]:
        """Get and validate category from user input.

        Returns:
            Valid category or None if cancelled
        """
        existing_categories = self.tracker.get_categories()

        if existing_categories:
            print(f"\nExisting categories: {', '.join(existing_categories)}")

        while True:
            category = input("Enter category: ").strip()

            if not category:
                print("Category cannot be empty.")
                continue

            if len(category) > 50:
                print("Category name too long (max 50 characters).")
                continue

            return category.title()  # Capitalise first letter of each word

    def view_all_expenses(self) -> None:
        """Display all expenses."""
        expenses = self.tracker.get_all_expenses()

        if not expenses:
            print("\n📭 No expenses found. Add your first expense!")
            return

        # Sort by date (newest first)
        expenses.sort(key=lambda x: x.date, reverse=True)

        print(f"\n📋 All Expenses ({len(expenses)} total)")
        print("─" * 65)
        print(f"{'Date':<12} {'Amount':<10} {'Category':<15} {'Description'}")
        print("─" * 65)

        for expense in expenses:
            date_str = expense.date.strftime("%Y-%m-%d")
            print(f"{date_str:<12} £{expense.amount:<9.2f} {expense.category:<15} {expense.description}")

        total = sum(exp.amount for exp in expenses)
        print("─" * 65)
        print(f"{'TOTAL:':<12} £{total:<9.2f}")

    def view_last_30_days(self) -> None:
        """Display expenses from the last 30 days."""
        expenses = self.tracker.get_expenses_last_30_days()

        if not expenses:
            print("\n📅 No expenses found in the last 30 days.")
            return

        # Sort by date (newest first)
        expenses.sort(key=lambda x: x.date, reverse=True)

        print(f"\n📈 Last 30 Days ({len(expenses)} expenses)")
        print("─" * 65)
        print(f"{'Date':<12} {'Amount':<10} {'Category':<15} {'Description'}")
        print("─" * 65)

        for expense in expenses:
            date_str = expense.date.strftime("%Y-%m-%d")
            print(f"{date_str:<12} £{expense.amount:<9.2f} {expense.category:<15} {expense.description}")

        total = sum(exp.amount for exp in expenses)
        print("─" * 65)
        print(f"{'TOTAL:':<12} £{total:<9.2f}")

    def view_total_spending(self) -> None:
        """Display total spending with breakdown."""
        expenses = self.tracker.get_all_expenses()
        total = self.tracker.get_total_spending()
        last_30_total = sum(exp.amount for exp in self.tracker.get_expenses_last_30_days())

        if not expenses:
            print("\n💷 No expenses recorded yet!")
            return

        print(f"\n💷 Spending Summary")
        print("─" * 30)
        print(f"{'All time total:':<20} £{total:.2f}")
        print(f"{'Last 30 days:':<20} £{last_30_total:.2f}")
        print(f"{'Total expenses:':<20} {len(expenses)}")

        if expenses:
            avg_expense = total / len(expenses)
            print(f"{'Average expense:':<20} £{avg_expense:.2f}")

    def view_spending_by_category(self) -> None:
        """Display spending totals by category."""
        category_totals = self.tracker.get_spending_by_category()

        if not category_totals:
            print("\n🏷️  No expenses found.")
            return

        total_spending = sum(category_totals.values())

        print(f"\n🏷️  Spending by Category")
        print("─" * 40)
        print(f"{'Category':<20} {'Amount':<10} {'%'}")
        print("─" * 40)

        for category, total in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
            percentage = (total / total_spending * 100) if total_spending > 0 else 0
            print(f"{category:<20} £{total:<9.2f} {percentage:>5.1f}%")

        print("─" * 40)
        print(f"{'TOTAL:':<20} £{total_spending:<9.2f} 100.0%")

    def filter_by_category_interactive(self) -> None:
        """Interactive prompt to filter expenses by category."""
        categories = self.tracker.get_categories()

        if not categories:
            print("No categories found. Add some expenses first!")
            return

        print(f"\nAvailable categories:")
        for i, category in enumerate(categories, 1):
            count = len(self.tracker.filter_by_category(category))
            total = sum(exp.amount for exp in self.tracker.filter_by_category(category))
            print(f"{i}. {category} ({count} expenses, £{total:.2f})")

        try:
            choice = input(f"\nEnter category number (1-{len(categories)}) or name: ").strip()

            # Check if it's a number
            if choice.isdigit():
                choice_num = int(choice)
                if 1 <= choice_num <= len(categories):
                    selected_category = categories[choice_num - 1]
                else:
                    print("Invalid category number.")
                    return
            else:
                # Find matching category (case insensitive)
                selected_category = None
                for category in categories:
                    if category.lower() == choice.lower():
                        selected_category = category
                        break

                if not selected_category:
                    print(f"Category '{choice}' not found.")
                    return

            self._display_category_expenses(selected_category)

        except (ValueError, IndexError):
            print("Invalid selection.")

    def _display_category_expenses(self, category: str) -> None:
        """Display expenses for a specific category.

        Args:
            category: Category to display expenses for
        """
        expenses = self.tracker.filter_by_category(category)

        if not expenses:
            print(f"No expenses found for category: {category}")
            return

        # Sort by date (newest first)
        expenses.sort(key=lambda x: x.date, reverse=True)

        print(f"\n📊 Expenses for category: {category}")
        print(f"{'Date':<12} {'Amount':<10} {'Description'}")
        print("─" * 50)

        for expense in expenses:
            date_str = expense.date.strftime("%Y-%m-%d")
            print(f"{date_str:<12} £{expense.amount:<9.2f} {expense.description}")

        total = sum(expense.amount for expense in expenses)
        print("─" * 50)
        print(f"{'Total:':<12} £{total:<9.2f} ({len(expenses)} expenses)")

    def get_menu_choice(self) -> Optional[int]:
        """Get and validate user menu choice.

        Returns:
            Selected menu option or None if invalid
        """
        try:
            choice = int(input("👉 Enter your choice (1-7): ").strip())
            if 1 <= choice <= 7:
                return choice
            else:
                print("❌ Please enter a number between 1 and 7.")
                return None
        except ValueError:
            print("❌ Please enter a valid number.")
            return None

    def run(self) -> None:
        """Run the main CLI loop."""
        print("🎉 Welcome to the Enhanced Expense Tracker!")

        while True:
            self.display_menu()
            choice = self.get_menu_choice()

            if choice is None:
                continue

            print()  # Add spacing

            if choice == 1:
                self.add_expense_interactive()
            elif choice == 2:
                self.view_all_expenses()
            elif choice == 3:
                self.view_last_30_days()
            elif choice == 4:
                self.view_total_spending()
            elif choice == 5:
                self.view_spending_by_category()
            elif choice == 6:
                self.filter_by_category_interactive()
            elif choice == 7:
                print("👋 Thank you for using the Expense Tracker!")
                print("💾 All your data has been saved automatically.")
                break

            # Pause after each action
            input("\n📎 Press Enter to continue...")