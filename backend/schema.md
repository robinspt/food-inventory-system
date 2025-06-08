# Database Schema for Food Inventory System (SQLite)

This document outlines the database schema for the Food Inventory System, using SQLite as the database.

## Table: `users`

Stores user information for authentication and authorization.

| Column Name    | Data Type  | Constraints                      | Description            |
| :------------- | :--------- | :------------------------------- | :--------------------- |
| `id`           | INTEGER    | PRIMARY KEY AUTOINCREMENT        | Unique user identifier |
| `username`     | TEXT       | UNIQUE NOT NULL                  | User's unique username |
| `password_hash`| TEXT       | NOT NULL                         | Hashed password        |
| `created_at`   | DATETIME   | DEFAULT CURRENT_TIMESTAMP NOT NULL | Record creation timestamp |
| `updated_at`   | DATETIME   | DEFAULT CURRENT_TIMESTAMP NOT NULL | Last update timestamp |

## Table: `food_items`

Stores details about each food item in the inventory.

| Column Name        | Data Type  | Constraints                      | Description                                |
| :----------------- | :--------- | :------------------------------- | :----------------------------------------- |
| `id`               | INTEGER    | PRIMARY KEY AUTOINCREMENT        | Unique food item identifier                |
| `name`             | TEXT       | NOT NULL                         | Name of the food item                      |
| `production_date`  | DATE       | NOT NULL                         | Date the food item was produced            |
| `expiry_period_value` | INTEGER    | NOT NULL                         | Numeric value for shelf life (e.g., 7, 1) |
| `expiry_period_unit`| TEXT       | NOT NULL (e.g., 'days', 'months')| Unit for shelf life (days or months)      |
| `quantity`         | INTEGER    | NOT NULL CHECK (`quantity` >= 0) | Quantity of the food item                  |
| `storage_location` | TEXT       |                                  | Where the food item is stored              |
| `expiration_date`  | DATE       | NOT NULL                         | Calculated expiration date                 |
| `status`           | TEXT       | NOT NULL (e.g., 'active', 'expired', 'warning') | Current status of the food item (active, expired, warning) |
| `created_at`       | DATETIME   | DEFAULT CURRENT_TIMESTAMP NOT NULL | Record creation timestamp                  |
| `updated_at`       | DATETIME   | DEFAULT CURRENT_TIMESTAMP NOT NULL | Last update timestamp                      |

## Relationships

- No explicit foreign key relationships are defined between `users` and `food_items` tables at this stage, adhering to the simplified scope. If user-specific inventory management is needed, a `user_id` column would be added to `food_items` referencing `users.id`.

## Notes on Data Types and Constraints

- **INTEGER PRIMARY KEY AUTOINCREMENT**: For auto-incrementing primary keys in SQLite.
- **TEXT**: For strings.
- **DATE**: For dates in 'YYYY-MM-DD' format.
- **DATETIME**: For timestamps in 'YYYY-MM-DD HH:MM:SS' format.
- **NOT NULL**: Ensures that a column cannot have a NULL value.
- **UNIQUE**: Ensures all values in a column are distinct.
- **CHECK**: Ensures that a value in a column satisfies a specific condition (e.g., `quantity` >= 0). 