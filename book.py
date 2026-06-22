"""
book.py
-------
Defines the Book class for the Library Management System.
"""


class Book:
    """Represents a book in the library."""

    def __init__(self, isbn: str, title: str, author: str, genre: str, total_copies: int):
        """
        Initialise a Book instance.

        Args:
            isbn (str): Unique identifier for the book.
            title (str): Title of the book.
            author (str): Author of the book.
            genre (str): Genre/category of the book.
            total_copies (int): Total number of copies owned by the library.
        """
        self.isbn = isbn
        self.title = title
        self.author = author
        self.genre = genre
        self.total_copies = total_copies
        self.available_copies = total_copies

    def borrow_copy(self) -> bool:
        """
        Reduce available copies by 1 if a copy is available.

        Returns:
            bool: True if borrowing was successful, False otherwise.
        """
        if self.available_copies > 0:
            self.available_copies -= 1
            return True
        return False

    def return_copy(self) -> bool:
        """
        Increase available copies by 1 if not exceeding total.

        Returns:
            bool: True if return was successful, False otherwise.
        """
        if self.available_copies < self.total_copies:
            self.available_copies += 1
            return True
        return False

    def is_available(self) -> bool:
        """
        Check if at least one copy is available.

        Returns:
            bool: True if available, False otherwise.
        """
        return self.available_copies > 0

    def display(self) -> None:
        """Print a formatted summary of the book."""
        status = "Available" if self.is_available() else "Not Available"
        print(f"  ISBN    : {self.isbn}")
        print(f"  Title   : {self.title}")
        print(f"  Author  : {self.author}")
        print(f"  Genre   : {self.genre}")
        print(f"  Copies  : {self.available_copies}/{self.total_copies}  [{status}]")
        print()

    def to_csv_row(self) -> list:
        """
        Convert book data to a list for CSV storage.

        Returns:
            list: Book fields as a list of strings.
        """
        return [
            self.isbn,
            self.title,
            self.author,
            self.genre,
            str(self.total_copies),
            str(self.available_copies),
        ]

    @classmethod
    def from_csv_row(cls, row: list) -> "Book":
        """
        Create a Book instance from a CSV row.

        Args:
            row (list): A list with fields [isbn, title, author, genre, total, available].

        Returns:
            Book: A reconstructed Book object.
        """
        book = cls(
            isbn=row[0],
            title=row[1],
            author=row[2],
            genre=row[3],
            total_copies=int(row[4]),
        )
        book.available_copies = int(row[5])
        return book
