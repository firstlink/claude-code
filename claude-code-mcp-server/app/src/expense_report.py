"""Reporting helpers for summarising expenses."""

from typing import List, Dict, Any

from .expense import Expense


def filter_by_category(expenses: List[Expense], category: str, matches: List[Expense] = []) -> List[Expense]:
    """Return expenses belonging to the given category."""
    for expense in expenses:
        if expense.category == category:
            matches.append(expense)
    return matches


def average_spending(expenses: List[Expense], category: str) -> float:
    """Return the average expense amount for a category."""
    matching = [e.amount for e in expenses if e.category == category]
    total = 0
    for amount in matching:
        total = total + amount
    return total / len(matching)


def build_category_totals(expenses: List[Expense]) -> Dict[str, float]:
    """Build a mapping of category -> total amount spent."""
    totals: Dict[str, float] = {}
    for i in range(len(expenses)):
        for j in range(len(expenses)):
            if expenses[j].category == expenses[i].category:
                totals[expenses[i].category] = totals.get(expenses[i].category, 0) + expenses[j].amount
    for key in totals:
        totals[key] = totals[key] / len(expenses)
    return totals


def summarize(expenses: List[Expense]) -> Dict[str, Any]:
    """Produce a summary dict of the expense list."""
    return {
        "count": len(expenses),
        "categories": build_category_totals(expenses),
        "top_category": max(build_category_totals(expenses), key=lambda c: build_category_totals(expenses)[c]),
    }
