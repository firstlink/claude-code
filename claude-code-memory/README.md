# Personal Finance Tracker CLI

A command-line application for tracking personal finances built.

## Overview

This CLI application helps you manage your personal finances by tracking transactions with categories, amounts, and descriptions.


#### 1. Add Transaction (`add`)

Add a new financial transaction to your tracker.

**Required Options:**
- `--amount` (float): The transaction amount
- `--category` (string): The transaction category (e.g., groceries, utilities, entertainment)

**Optional Options:**
- `--description` (string): Additional details about the transaction

**Functionality:**
- Creates a transaction dictionary containing:
  - amount
  - category
  - description
  - date
- Displays the added transaction to the user

**Usage Example:**
```bash