# Library-Management-System
A Library Management System built as a part of B100 Module at Gisma University of Applied Sciences
---
# Purpose
This Library Management System allows to manage books, add new members, process returns and borrows and persist all data.
---
# Features
- Add, remove, and search books
- Register and remove members
- Borrow and return books with availability tracking
- Full transaction history
- Data persistence via CSV files (no database required)
- Robust exception handling for invalid inputs
---
# Key Files 
- book.py: Book class
- file_handler.py: CSV read/write helper and file paths
- library.py: Core; members, transactions and catalogue
- main.py: Main interface
- member.py: Member class
- transaction.py: Transaction class
---
# Usage 
Example are as the following
- Main menu
  
--- MAIN MENU ---
  1. Book Management
  2. Member Management
  3. Borrow a Book
  4. Return a Book
  5. View Transaction History
  0. Exit

- Member Registeration
  
--- MEMBER MANAGEMENT ---
  1. Register a Member
  2. Remove a Member
  3. List All Members
  0. Back

---
# Installation
- Python 3.8 or higher needed
---
# Running the program
- Clone the repositary
- Run main.py

