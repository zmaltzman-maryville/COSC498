-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS package;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE package (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  user_description TEXT,
  recipient TEXT,
  tracking_number TEXT,
  carrier TEXT,
  current_status TEXT,
  order_date TEXT,
  delivery_date TEXT,
  delivered BOOLEAN
);