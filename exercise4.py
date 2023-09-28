import sqlite3

# Create a database connection
conn = sqlite3.connect('library.db')

# Create a cursor object
cursor = conn.cursor()

# Create the Books table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Books (
        BookID INTEGER PRIMARY KEY AUTOINCREMENT,
        Title TEXT,
        Author TEXT,
        ISBN TEXT,
        Status TEXT
    )
''')

# Create the Users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        UserID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT,
        Email TEXT
    )
''')

# Create Reservations
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Reservations (
        ReservationID INTEGER PRIMARY KEY AUTOINCREMENT,
        BookID INTEGER,
        UserID INTEGER,
        ReservationDate TEXT,
        FOREIGN KEY (BookID) REFERENCES Books (BookID),
        FOREIGN KEY (UserID) REFERENCES Users (UserID)
    )
''')

# Add new book
def add_book():
    title = input("Enter the title of the book: ")
    author = input("Enter the author of the book: ")
    isbn = input("Enter the ISBN of the book: ")
    status = input("Enter the status of the book: ")

    cursor.execute('''
        INSERT INTO Books (Title, Author, ISBN, Status)
        VALUES (?, ?, ?, ?)
    ''', (title, author, isbn, status))

    conn.commit()
    print("Book added successfully.")

# Find book details based on BookID
def find_book_by_id():
    book_id = input("Enter the BookID: ")

    cursor.execute('''
        SELECT Books.Title, Books.Author, Books.ISBN, Books.Status, Users.Name, Users.Email
        FROM Books
        LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
        LEFT JOIN Users ON Reservations.UserID = Users.UserID
        WHERE Books.BookID = ?
    ''', (book_id,))

    book_details = cursor.fetchone()

    if book_details:
        title, author, isbn, status, user_name, user_email = book_details
        print("Title:", title)
        print("Author:", author)
        print("ISBN:", isbn)
        print("Status:", status)
        print("Reserved by:", user_name if user_name else "No reservation")
        print("Email:", user_email if user_email else "-")
    else:
        print("Book not found.")

# Find the reservation status of the book based on BookID, Title, UserID, and ReservationID
def find_reservation_status():
    identifier = input("Enter the identifier: ")

    if identifier.startswith("LB"):  # BookID
        cursor.execute('''
            SELECT Books.Title, Books.Status, Users.Name
            FROM Books
            LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
            LEFT JOIN Users ON Reservations.UserID = Users.UserID
            WHERE Books.BookID = ?
        ''', (identifier,))
    elif identifier.startswith("LU"):  # UserID
        cursor.execute('''
            SELECT Books.Title, Books.Status, Users.Name
            FROM Books
            LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
            LEFT JOIN Users ON Reservations.UserID = Users.UserID
            WHERE Users.UserID = ?
        ''', (identifier,))
    elif identifier.startswith("LR"):  # ReservationID
        cursor.execute('''
            SELECT Books.Title, Books.Status, Users.Name
            FROM Books
            LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
            LEFT JOIN Users ON Reservations.UserID = Users.UserID
            WHERE Reservations.ReservationID = ?
        ''', (identifier,))
    else:  # Title
        cursor.execute('''
            SELECT Books.Title, Books.Status, Users.Name
            FROM Books
            LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
            LEFT JOIN Users ON Reservations.UserID = Users.UserID
            WHERE Books.Title = ?
        ''', (identifier,))

    book_details = cursor.fetchall()

    if book_details:
        print("Reservation status:")
        for book in book_details:
            title, status, user_name = book
            print("Title:", title)
            print("Status:", status)
            print("Reserved by:", user_name if user_name else "No reservation")
            print()
    else:
        print("No matching records found.")

# Find all books
def find_all_books():
    cursor.execute('''
        SELECT Books.BookID, Books.Title, Books.Author, Books.ISBN, Books.Status, Users.Name, Users.Email
        FROM Books
        LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
        LEFT JOIN Users ON Reservations.UserID = Users.UserID
    ''')

    book_details = cursor.fetchall()

    if book_details:
        print("All books:")
        for book in book_details:
            book_id, title, author, isbn, status, user_name, user_email = book
            print("BookID:", book_id)
            print("Title:", title)
            print("Author:", author)
            print("ISBN:", isbn)
            print("Status:", status)
            print("Reserved by:", user_name if user_name else "No reservation")
            print("Email:", user_email if user_email else "-")
            print()
    else:
        print("No books found.")

# Modify book details
def update_book_details():
    book_id = input("Enter the BookID: ")

    cursor.execute('''
        SELECT * FROM Books WHERE BookID = ?
    ''', (book_id,))

    book_details = cursor.fetchone()

    if book_details:
        print("Current book details:")
        print("Title:", book_details[1])
        print("Author:", book_details[2])
        print("ISBN:", book_details[3])
        print("Status:", book_details[4])

        new_title = input("Enter the new title (leave blank to keep current): ")
        new_author = input("Enter the new author (leave blank to keep current): ")
        new_isbn = input("Enter the new ISBN (leave blank to keep current): ")
        new_status = input("Enter the new status (leave blank to keep current): ")

        if new_title:
            cursor.execute('''
                UPDATE Books SET Title = ? WHERE BookID = ?
            ''', (new_title, book_id))

        if new_author:
            cursor.execute('''
                UPDATE Books SET Author = ? WHERE BookID = ?
            ''', (new_author, book_id))

        if new_isbn:
            cursor.execute('''
                UPDATE Books SET ISBN = ? WHERE BookID = ?
            ''', (new_isbn, book_id))

        if new_status:
            cursor.execute('''
                UPDATE Books SET Status = ? WHERE BookID = ?
            ''', (new_status, book_id))

        conn.commit()
        print("Book details updated successfully.")
    else:
        print("Book not found.")

# Delete books
def delete_book():
    book_id = input("Enter the BookID: ")

    cursor.execute('''
        SELECT Status FROM Books WHERE BookID = ?
    ''', (book_id,))

    book_status = cursor.fetchone()

    if book_status:
        if book_status[0] == "Reserved":
            cursor.execute('''
                DELETE FROM Reservations WHERE BookID = ?
            ''', (book_id,))

        cursor.execute('''
            DELETE FROM Books WHERE BookID = ?
        ''', (book_id,))

        conn.commit()
        print("Book deleted successfully.")
    else:
        print("Book not found.")

# Update the book's pre-order status
def update_reservation_status():
    book_id = input("Enter the BookID: ")
    new_status = input("Enter the new status (Available or Reserved): ")

# Check if books exist
    cursor.execute('''
        SELECT Status FROM Books WHERE BookID = ?
    ''', (book_id,))

    book_status = cursor.fetchone()

    if book_status:
        if new_status == "Available" or new_status == "Reserved":
            cursor.execute('''
                UPDATE Books SET Status = ? WHERE BookID = ?
            ''', (new_status, book_id))

            # If the status is updated to "Available", the relevant booking record is deleted
            if new_status == "Available":
                cursor.execute('''
                    DELETE FROM Reservations WHERE BookID = ?
                ''', (book_id,))

            conn.commit()
            print("Reservation status updated successfully.")
        else:
            print("Invalid status. Status can only be 'Available' or 'Reserved'.")
    else:
        print("Book not found.")

# Menu Options
menu = '''
Library Management System:
1. Add a new book
2. Find a book's detail based on BookID
3. Find a book's reservation status based on BookID, Title, UserID, and ReservationID
4. Find all the books in the database
5. Modify/update book details based on its BookID
6. Delete a book based on its BookID
7. Change reservation status based on BookID
8. Exit
'''

# Run the program in an editor like VSCode
while True:
    print(menu)
    choice = input("Enter your choice (1-8): ")

    if choice == '1':
        add_book()
    elif choice == '2':
        find_book_by_id()
    elif choice == '3':
        find_reservation_status()
    elif choice == '4':
        find_all_books()
    elif choice == '5':
        update_book_details()
    elif choice == '6':
        delete_book()
    elif choice == '7':
        update_reservation_status()
    elif choice == '8':
        break
    else:
        print("Invalid choice. Please try again.")

# Close the database connection
conn.close()