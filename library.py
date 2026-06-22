"""
library.py
----------
Defines the Library class, which manages all books, members,
transactions, and persistence for the Library Management System.
"""

import uuid

from book import Book
from member import Member
from transaction import Transaction
import file_handler as fh


class Library:
    """Core management class for the library system."""

    def __init__(self, name: str):
        """
        Initialise the Library.

        Args:
            name (str): Name of the library.
        """
        self.name = name
        self.books: dict = {}         # isbn -> Book
        self.members: dict = {}       # member_id -> Member
        self.transactions: list = []  # list of Transaction objects

        fh.initialise_data_files()
        self._load_all()

   
     ## Private: load from CSV                                                  
    

    def _load_all(self) -> None:
        """Load books, members, and transactions from CSV files."""
        self._load_books()
        self._load_members()
        self._load_transactions()

    def _load_books(self) -> None:
        """Load books from the books CSV file."""
        try:
            rows = fh.read_csv(fh.BOOKS_FILE)
            for row in rows:
                book = Book.from_csv_row(row)
                self.books[book.isbn] = book
        except FileNotFoundError:
            pass  # First run — no file yet

    def _load_members(self) -> None:
        """Load members from the members CSV file."""
        try:
            rows = fh.read_csv(fh.MEMBERS_FILE)
            for row in rows:
                member = Member.from_csv_row(row)
                self.members[member.member_id] = member
        except FileNotFoundError:
            pass

    def _load_transactions(self) -> None:
        """Load transactions from the transactions CSV file."""
        try:
            rows = fh.read_csv(fh.TRANSACTIONS_FILE)
            for row in rows:
                txn = Transaction.from_csv_row(row)
                self.transactions.append(txn)
        except FileNotFoundError:
            pass


    ##  Private: save to CSV                                                     
 

    def _save_books(self) -> None:
        """Keep all book data to CSV."""
        rows = [book.to_csv_row() for book in self.books.values()]
        fh.write_csv(fh.BOOKS_FILE, fh.BOOKS_HEADERS, rows)

    def _save_members(self) -> None:
        """Keep all member data to CSV."""
        rows = [member.to_csv_row() for member in self.members.values()]
        fh.write_csv(fh.MEMBERS_FILE, fh.MEMBERS_HEADERS, rows)

    def _save_transaction(self, txn: Transaction) -> None:
        """Combine a single transaction to the transactions CSV."""
        fh.append_csv(fh.TRANSACTIONS_FILE, txn.to_csv_row())

 
    ##  Book management                                                          
    

    def add_book(self, isbn: str, title: str, author: str, genre: str, copies: int) -> None:
        """
        Add a new book to the library catalogue.

        Args:
            isbn (str): Unique ISBN.
            title (str): Book title.
            author (str): Book author.
            genre (str): Book genre.
            copies (int): Number of copies to stock.

        Raises:
            ValueError: If a book with the same ISBN already exists,
                        or if copies is not a positive integer.
        """
        if isbn in self.books:
            raise ValueError(f"A book with ISBN '{isbn}' already exists.")
        if copies < 1:
            raise ValueError("Number of copies must be at least 1.")

        book = Book(isbn, title, author, genre, copies)
        self.books[isbn] = book
        self._save_books()
        print(f"  ✓ Book '{title}' added successfully.\n")

    def remove_book(self, isbn: str) -> None:
        """
        Remove a book from the catalogue.

        Args:
            isbn (str): ISBN of the book to remove.

        Raises:
            KeyError: If the book is not found.
            ValueError: If the book still has copies borrowed out.
        """
        book = self._get_book(isbn)
        if book.available_copies < book.total_copies:
            raise ValueError("Cannot remove book — some copies are still borrowed.")
        del self.books[isbn]
        self._save_books()
        print(f"  ✓ Book '{book.title}' removed.\n")

    def search_books(self, keyword: str) -> list:
        """
        Search books by title, author, or genre (case-insensitive).

        Args:
            keyword (str): Search term.

        Returns:
            list: Matching Book objects.
        """
        keyword = keyword.lower()
        results = [
            book for book in self.books.values()
            if keyword in book.title.lower()
            or keyword in book.author.lower()
            or keyword in book.genre.lower()
        ]
        return results

    def list_all_books(self) -> None:
        """Print all books currently in the catalogue."""
        if not self.books:
            print("  No books in the catalogue.\n")
            return
        print(f"\n  {'='*40}")
        print(f"  Catalogue — {self.name}")
        print(f"  {'='*40}\n")
        for book in self.books.values():
            book.display()

  
    ##  Member management                                                        
   

    def register_member(self, name: str, email: str) -> str:
        """
        Register a new library member.

        Args:
            name (str): Member's full name.
            email (str): Member's email address.

        Returns:
            str: The newly generated member ID.

        Raises:
            ValueError: If a member with the same email already exists.
        """
        for member in self.members.values():
            if member.email.lower() == email.lower():
                raise ValueError(f"A member with email '{email}' already exists.")

        member_id = "M" + str(uuid.uuid4())[:6].upper()
        member = Member(member_id, name, email)
        self.members[member_id] = member
        self._save_members()
        print(f"  ✓ Member registered. ID: {member_id}\n")
        return member_id

    def remove_member(self, member_id: str) -> None:
        """
        Remove a member from the system.

        Args:
            member_id (str): ID of the member to remove.

        Raises:
            KeyError: If member is not found.
            ValueError: If member still has books borrowed.
        """
        member = self._get_member(member_id)
        if member.borrowed_isbns:
            raise ValueError("Cannot remove member — they still have borrowed books.")
        del self.members[member_id]
        self._save_members()
        print(f"  ✓ Member '{member.name}' removed.\n")

    def list_all_members(self) -> None:
        """Print all registered members."""
        if not self.members:
            print("  No members registered.\n")
            return
        print(f"\n  {'='*40}")
        print(f"  Registered Members — {self.name}")
        print(f"  {'='*40}\n")
        for member in self.members.values():
            member.display()

        ##  Borrow / Return                                                          
    

    def borrow_book(self, member_id: str, isbn: str) -> None:
        """
        Process a book borrowing request.

        Args:
            member_id (str): ID of the borrowing member.
            isbn (str): ISBN of the book to borrow.

        Raises:
            KeyError: If member or book is not found.
            ValueError: If no copies are available or member already has it.
        """
        member = self._get_member(member_id)
        book = self._get_book(isbn)

        if member.has_borrowed(isbn):
            raise ValueError(f"Member already has '{book.title}' borrowed.")
        if not book.is_available():
            raise ValueError(f"No available copies of '{book.title}'.")

        book.borrow_copy()
        member.borrow_book(isbn)

        txn = Transaction(
            transaction_id="T" + str(uuid.uuid4())[:8].upper(),
            member_id=member_id,
            isbn=isbn,
            action="BORROW",
        )
        self.transactions.append(txn)
        self._save_books()
        self._save_members()
        self._save_transaction(txn)
        print(f"  ✓ '{book.title}' borrowed by {member.name}.\n")

    def return_book(self, member_id: str, isbn: str) -> None:
        """
        Process a book return.

        Args:
            member_id (str): ID of the returning member.
            isbn (str): ISBN of the book to return.

        Raises:
            KeyError: If member or book is not found.
            ValueError: If the member has not borrowed this book.
        """
        member = self._get_member(member_id)
        book = self._get_book(isbn)

        if not member.has_borrowed(isbn):
            raise ValueError(f"Member '{member.name}' has not borrowed '{book.title}'.")

        book.return_copy()
        member.return_book(isbn)

        txn = Transaction(
            transaction_id="T" + str(uuid.uuid4())[:8].upper(),
            member_id=member_id,
            isbn=isbn,
            action="RETURN",
        )
        self.transactions.append(txn)
        self._save_books()
        self._save_members()
        self._save_transaction(txn)
        print(f"  ✓ '{book.title}' returned by {member.name}.\n")

    def view_transaction_history(self) -> None:
        """Print all recorded transactions."""
        if not self.transactions:
            print("  No transactions recorded yet.\n")
            return
        print(f"\n  {'='*40}")
        print("  Transaction History")
        print(f"  {'='*40}\n")
        for txn in self.transactions:
            txn.display()

    
    ##  Private helpers                                                          
    
    def _get_book(self, isbn: str) -> Book:
        """
        Retrieve a book by ISBN.

        Raises:
            KeyError: If book is not found.
        """
        if isbn not in self.books:
            raise KeyError(f"No book found with ISBN '{isbn}'.")
        return self.books[isbn]

    def _get_member(self, member_id: str) -> Member:
        """
        Retrieve a member by ID.

        Raises:
            KeyError: If member is not found.
        """
        if member_id not in self.members:
            raise KeyError(f"No member found with ID '{member_id}'.")
        return self.members[member_id]
