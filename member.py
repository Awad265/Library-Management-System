"""
member.py
---------
Defines the Member class for the Library Management System.
"""


class Member:
    """Represents a registered library member."""

    def __init__(self, member_id: str, name: str, email: str):
        """
        Initialise a Member instance.

        Args:
            member_id (str): Unique identifier for the member.
            name (str): Full name of the member.
            email (str): Email address of the member.
        """
        self.member_id = member_id
        self.name = name
        self.email = email
        self.borrowed_isbns: list = []  # List of ISBNs currently borrowed

    def borrow_book(self, isbn: str) -> bool:
        """
        Record that the member has borrowed a book.

        Args:
            isbn (str): ISBN of the book being borrowed.

        Returns:
            bool: True if added successfully, False if already borrowed.
        """
        if isbn not in self.borrowed_isbns:
            self.borrowed_isbns.append(isbn)
            return True
        return False

    def return_book(self, isbn: str) -> bool:
        """
        Remove a book from the member's borrowed list.

        Args:
            isbn (str): ISBN of the book being returned.

        Returns:
            bool: True if removed successfully, False if not found.
        """
        if isbn in self.borrowed_isbns:
            self.borrowed_isbns.remove(isbn)
            return True
        return False

    def has_borrowed(self, isbn: str) -> bool:
        """
        Check if the member currently has a specific book borrowed.

        Args:
            isbn (str): ISBN to check.

        Returns:
            bool: True if currently borrowed, False otherwise.
        """
        return isbn in self.borrowed_isbns

    def display(self) -> None:
        """Print a formatted summary of the member."""
        print(f"  Member ID : {self.member_id}")
        print(f"  Name      : {self.name}")
        print(f"  Email     : {self.email}")
        borrowed = ", ".join(self.borrowed_isbns) if self.borrowed_isbns else "None"
        print(f"  Borrowed  : {borrowed}")
        print()

    def to_csv_row(self) -> list:
        """
        Convert member data to a list for CSV storage.

        Returns:
            list: Member fields as a list of strings.
        """
        borrowed_str = "|".join(self.borrowed_isbns)
        return [self.member_id, self.name, self.email, borrowed_str]

    @classmethod
    def from_csv_row(cls, row: list) -> "Member":
        """
        Create a Member instance from a CSV row.

        Args:
            row (list): A list with fields [member_id, name, email, borrowed_isbns].

        Returns:
            Member: A reconstructed Member object.
        """
        member = cls(
            member_id=row[0],
            name=row[1],
            email=row[2],
        )
        # Restore borrowed list  
        member.borrowed_isbns = row[3].split("|") if row[3] else []
        return member
