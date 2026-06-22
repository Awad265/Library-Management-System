"""
main.py
-------
Entry point for the Library Management System.
Provides an interactive, menu-driven command-line interface.
"""

from library import Library


def print_banner(library_name: str) -> None:
    """Print the welcome banner."""
    print("\n" + "=" * 50)
    print(f"   Welcome to {library_name}")
    print("=" * 50)


def print_main_menu() -> None:
    """Display the main menu options."""
    print("\n--- MAIN MENU ---")
    print("  1. Book Management")
    print("  2. Member Management")
    print("  3. Borrow a Book")
    print("  4. Return a Book")
    print("  5. View Transaction History")
    print("  0. Exit")
    print("-" * 20)


def print_book_menu() -> None:
    """Display the book management sub-menu."""
    print("\n--- BOOK MANAGEMENT ---")
    print("  1. Add a Book")
    print("  2. Remove a Book")
    print("  3. Search Books")
    print("  4. List All Books")
    print("  0. Back")
    print("-" * 25)


def print_member_menu() -> None:
    """Display the member management sub-menu."""
    print("\n--- MEMBER MANAGEMENT ---")
    print("  1. Register a Member")
    print("  2. Remove a Member")
    print("  3. List All Members")
    print("  0. Back")
    print("-" * 25)



##  Book management actions                                                      


def handle_add_book(lib: Library) -> None:
    """Prompt user for book details and add to the catalogue."""
    print("\n  -- Add New Book --")
    isbn = input("  ISBN      : ").strip()
    title = input("  Title     : ").strip()
    author = input("  Author    : ").strip()
    genre = input("  Genre     : ").strip()

    try:
        copies = int(input("  Copies    : ").strip())
        lib.add_book(isbn, title, author, genre, copies)
    except ValueError as e:
        print(f"  ✗ Error: {e}\n")


def handle_remove_book(lib: Library) -> None:
    """Prompt user for ISBN and remove the book."""
    isbn = input("\n  Enter ISBN to remove: ").strip()
    try:
        lib.remove_book(isbn)
    except (KeyError, ValueError) as e:
        print(f"  ✗ Error: {e}\n")


def handle_search_books(lib: Library) -> None:
    """Search books by keyword and display results."""
    keyword = input("\n  Enter search keyword (title/author/genre): ").strip()
    results = lib.search_books(keyword)
    if results:
        print(f"\n  Found {len(results)} result(s):\n")
        for book in results:
            book.display()
    else:
        print("  No books matched your search.\n")

##  Member management actions                                                    


def handle_register_member(lib: Library) -> None:
    """Prompt user for member details and register them."""
    print("\n  -- Register New Member --")
    name = input("  Name  : ").strip()
    email = input("  Email : ").strip()
    try:
        lib.register_member(name, email)
    except ValueError as e:
        print(f"  ✗ Error: {e}\n")


def handle_remove_member(lib: Library) -> None:
    """Prompt user for member ID and remove them."""
    member_id = input("\n  Enter Member ID to remove: ").strip()
    try:
        lib.remove_member(member_id)
    except (KeyError, ValueError) as e:
        print(f"  ✗ Error: {e}\n")


##  Borrow / Return actions                                                      


def handle_borrow(lib: Library) -> None:
    """Prompt for member ID and ISBN, then process borrow."""
    print("\n  -- Borrow a Book --")
    member_id = input("  Member ID : ").strip()
    isbn = input("  ISBN      : ").strip()
    try:
        lib.borrow_book(member_id, isbn)
    except (KeyError, ValueError) as e:
        print(f"  ✗ Error: {e}\n")


def handle_return(lib: Library) -> None:
    """Prompt for member ID and ISBN, then process return."""
    print("\n  -- Return a Book --")
    member_id = input("  Member ID : ").strip()
    isbn = input("  ISBN      : ").strip()
    try:
        lib.return_book(member_id, isbn)
    except (KeyError, ValueError) as e:
        print(f"  ✗ Error: {e}\n")


##  Sub-menu loops                                                               


def book_menu_loop(lib: Library) -> None:
    """Run the book management sub-menu loop."""
    while True:
        print_book_menu()
        choice = input("  Choice: ").strip()
        if choice == "1":
            handle_add_book(lib)
        elif choice == "2":
            handle_remove_book(lib)
        elif choice == "3":
            handle_search_books(lib)
        elif choice == "4":
            lib.list_all_books()
        elif choice == "0":
            break
        else:
            print("  ✗ Invalid option. Please try again.\n")


def member_menu_loop(lib: Library) -> None:
    """Run the member management sub-menu loop."""
    while True:
        print_member_menu()
        choice = input("  Choice: ").strip()
        if choice == "1":
            handle_register_member(lib)
        elif choice == "2":
            handle_remove_member(lib)
        elif choice == "3":
            lib.list_all_members()
        elif choice == "0":
            break
        else:
            print("  ✗ Invalid option. Please try again.\n")



##  Main entry point                                                             


def main() -> None:
    """Initialise the library and start the main menu loop."""
    lib = Library("Gisma City Library")
    print_banner(lib.name)

    while True:
        print_main_menu()
        choice = input("  Choice: ").strip()

        if choice == "1":
            book_menu_loop(lib)
        elif choice == "2":
            member_menu_loop(lib)
        elif choice == "3":
            handle_borrow(lib)
        elif choice == "4":
            handle_return(lib)
        elif choice == "5":
            lib.view_transaction_history()
        elif choice == "0":
            print("\n  Goodbye! All data has been saved.\n")
            break
        else:
            print("  ✗ Invalid option. Please try again.\n")


if __name__ == "__main__":
    main()
