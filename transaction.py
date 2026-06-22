"""
transaction.py
--------------
Defines the Transaction class for the Library Management System.
"""

from datetime import date


class Transaction:
    """Records a single borrow or return event."""

    def __init__(
        self,
        transaction_id: str,
        member_id: str,
        isbn: str,
        action: str,
        transaction_date: str = None,
    ):
        """
        Initialise a Transaction instance.

        Args:
            transaction_id (str): Unique identifier for this transaction.
            member_id (str): ID of the member involved.
            isbn (str): ISBN of the book involved.
            action (str): Either 'BORROW' or 'RETURN'.
            transaction_date (str, optional): Date string (YYYY-MM-DD).
                                              Defaults to today's date.
        """
        self.transaction_id = transaction_id
        self.member_id = member_id
        self.isbn = isbn
        self.action = action.upper()
        self.transaction_date = transaction_date or str(date.today())

    def is_borrow(self) -> bool:
        """
        Check if this transaction is a borrow action.

        Returns:
            bool: True if action is BORROW.
        """
        return self.action == "BORROW"

    def is_return(self) -> bool:
        """
        Check if this transaction is a return action.

        Returns:
            bool: True if action is RETURN.
        """
        return self.action == "RETURN"

    def display(self) -> None:
        """Print a formatted summary of the transaction."""
        print(f"  Transaction ID : {self.transaction_id}")
        print(f"  Member ID      : {self.member_id}")
        print(f"  ISBN           : {self.isbn}")
        print(f"  Action         : {self.action}")
        print(f"  Date           : {self.transaction_date}")
        print()

    def to_csv_row(self) -> list:
        """
        Convert transaction data to a list for CSV storage.

        Returns:
            list: Transaction fields as a list of strings.
        """
        return [
            self.transaction_id,
            self.member_id,
            self.isbn,
            self.action,
            self.transaction_date,
        ]

    @classmethod
    def from_csv_row(cls, row: list) -> "Transaction":
        """
        Create a Transaction instance from a CSV row.

        Args:
            row (list): A list with fields
                        [transaction_id, member_id, isbn, action, date].

        Returns:
            Transaction: A reconstructed Transaction object.
        """
        return cls(
            transaction_id=row[0],
            member_id=row[1],
            isbn=row[2],
            action=row[3],
            transaction_date=row[4],
        )
