import sqlite3

# Function for checking valid qty input
def qty_check_int(book_aty):
    while True: # Loop to ensure valid int input for qty
            try:
                book_qty = int(input("\t\tBook quantity available: ")) # Prompting user to enter the quantity of books available
            except ValueError:
                print("\t\tInvalid input. Please enter a valid integer.")
            else:
                break
    return book_qty


# Function for searching for books in database
def search_for_books(book_title):

    split_title = book_title.split() # Splitting the book title into words       
    cursor.execute('''SELECT title from book WHERE title LIKE ?''', ('%' + split_title[0] + '%',)) # Executing SQL query to search for books with similar titles
    results = cursor.fetchall()
    if len(results) == 0: # Checking if there are no results
        for i in range(len(split_title)): # Looping through each word in the title
            cursor.execute('''SELECT title from book WHERE title LIKE ?''', ('%' + split_title[i] + '%',))
            results = cursor.fetchall()
    return results
 

db = sqlite3.connect('ebookstore.db') # Connecting to the database
cursor = db.cursor() # Creating a cursor object

cursor.execute('''
    CREATE TABLE IF NOT EXISTS book(id INTEGER PRIMARY KEY, title TEXT COLLATE NOCASE,
                   	author TEXT, qty INTEGER)
''')  # Creating a table 'book'
db.commit()

# List of book stock with tuples containing book details
book_stock = [(3001,'A Tale of Two Cities', 'Charles Dickens',30), (3002,'Harry Potter and the Philosopher\'s stone','J.K Rowling',40), 
              (3003,'The lion, the Witch and the Wardrobe','C.S Lewis',25), (3004,'The Lord of the Rings', 'J.R.R Tolkien',37), (3005,'Alice in Wonderland','Lewis Carroll',12)]

cursor.executemany('''INSERT OR IGNORE INTO book(id, title, author, qty) 
                  VALUES(?,?,?,?)''', book_stock) # Inserting book stock into the table

db.commit() # Commiting the data to the database


while True:
    menu = input('''\t\t ~~Welcome To Bookworm~~\n
                What can the worm do for you today?
                1. Enter Book
                2. Update Book
                3. Delete Book
                4. Search Books
                0. Exit
                : ''') # Displaying menu options to the user

    if menu == "1":   
        book_title = input('''\t\tPlease enter the following to register a book to the database.
                Title: ''') # Prompting user to enter book details                   
        cursor.execute('''SELECT title FROM book WHERE title=?''', (book_title,))
        found_book = cursor.fetchone()                   
        book_result = bool(found_book) # Checking if the book exists        
        if book_result == True:
            while True: # Loop until a unique book title is entere
                print(f"\t\t{found_book} is already in the database")
                book_title = input("\t\tPlease input Book title: ")
                cursor.execute('''SELECT title FROM book WHERE title=?''', (book_title,))            
                book_result = bool(cursor.fetchone()) 
                if book_result == False:
                   break

        book_author = input("\t\tAuthor: ") # Prompting user to enter the author's name

        while True: # Loop to ensure valid int input for qty
            try:
                book_qty = int(input("\t\tBook quantity available: ")) # Prompting user to enter the quantity of books available
            except ValueError:
                print("\t\tInvalid input. Please enter a valid integer.")
            else:
                break
                 
        book_data = (book_title, book_author, book_qty)  # Creating a tuple containing book details
        cursor.execute(''' INSERT INTO book(title, author, qty)
                    VALUES(?,?,?)''', book_data) # Inserting data into table
        db.commit()
        print("\t\t~ Book added to database ~\n")

    elif menu == "2":
        book_title = input("\n\t\tLets update some book info!\n\t\tPlease enter name of the book: ") # Prompting user to enter the title of the book to update
        cursor.execute('''SELECT title FROM book WHERE title=?''', (book_title,))
        update_result = bool(cursor.fetchone())
        if update_result == True:
            while True: # Loop for updating book details
                update_menu = input(f'''\t\tWhat information you would like update about "{book_title}":\n
                1. Author
                2. Title
                3. Qty 
                0. Return to main menue 
                : ''')
                if update_menu == "1":
                    author_update = input("\t\tPlease input updated Author information: ")  # Prompting user to enter updated author information
                    cursor.execute(f''' UPDATE book SET author=? WHERE title =? ''', (author_update,book_title))
                    db.commit()
                    continue

                elif update_menu == "2":
                    title_update = input("\t\tEnter updated Title: ") # Prompting user to enter updated title
                    cursor.execute(f''' UPDATE book SET title=? WHERE title =? ''', (title_update,book_title))
                    db.commit()
                    print("Change in title successful, returning to main menu.")
                    break

                elif update_menu == "3":
                    while True: # Loop to ensure valid int input for qty
                        try:
                            qty_update = int(input("\t\tEnter updated quantity amount: ")) # Prompting user to enter the quantity of books available
                        except ValueError:
                            print("\t\tInvalid input. Please enter a valid integer.")
                        else:
                            break                    
                    cursor.execute(f''' UPDATE book SET qty=? WHERE title =? ''', (qty_update,book_title))
                    db.commit()
                    continue

                elif update_menu == "0":
                    break

                else:
                    print("\t\tIncorrect input choice please try again.\n")
                    continue
        else:
            print("\t\tBook is not in database") # Informing the user that the book is not found in the database


    elif menu == "3":
        book_title = input("\t\tPlease enter title of book you wish to delete: ") # Prompting user to enter the title of the book to delete
        cursor.execute('''SELECT title FROM book WHERE title=?''', (book_title,))            
        book_result = bool(cursor.fetchone()) # Checking if the book exists
        if book_result == True:
            cursor.execute('''DELETE FROM book WHERE title=?''', (book_title,))
            print("\t\tBook Deleted from database successfully.")
            db.commit
            continue
                            
        elif book_result == False: # If there was no exact matches           
            search_results = search_for_books(book_title)
            if len(search_results) == 0: # If no relevant matches
                print("\t\tThere were no matches in the database.") # Inform user that no book could be found
            
            elif len(search_results) >= 1: # If relevant match is found
                print("\t\tThere were no exact matches in the database but the following results are similar:\n")
                for i, books in enumerate(search_results): # Print out relevant matches for user to choose from
                    print(f"\t\t{i+1}. {books}")
                delete_choice = int(input("\n\t\tEnter number of book you would like to delete: "))
                if delete_choice >= 1 and delete_choice <= len(search_results): # Ensure user choice is a valid option
                    cursor.execute('''DELETE FROM book WHERE title=?''', (search_results[delete_choice - 1]))
                    db.commit
                    print(f"\t\t~{search_results[delete_choice - 1]} has been deleted from the database ~")
                    continue
                else:
                    print("\t\t~ Invalid choice ~")      

    elif menu == "4":
        book_title = input("\t\tPlease enter title of book you wish to search for: ") # Prompt user for title of book they want to search for
        cursor.execute('''SELECT title FROM book WHERE title=?''', (book_title,))
        book_result = bool(cursor.fetchone()) # Check if book is in database
        if book_result == True:
            cursor.execute('''SELECT id, title, author, qty FROM book WHERE title=?''', (book_title,))
            search_book = cursor.fetchone()
            print(f"\t\t{search_book}\n")
        else:
            search_results = search_for_books(book_title) # Use function to find relevant options
            if len(search_results) == 0: # Check if there are any relevant options
                print("\t\tThere were no matches in the database.")

            elif len(search_results) >= 1: # Show relevant options
                print("\t\tThere were no exact matches but the following books contain similarities:\n")    
                for i, books in enumerate(search_results):
                    print(f"\t\t{i+1}. {books}")
            
                search_choice = int(input("\n\t\tEnter number of book you would like more information on: "))
                if search_choice >= 1 and search_choice <= len(search_results): # Confirm user choice on which book they are searching
                    cursor.execute('''SELECT id, title, author, qty FROM book WHERE title=?''', (search_results[search_choice - 1]))
                    search_book = cursor.fetchone()
                    print(f"\t\t{search_book}\n")

                else:
                    print("\t\t ~ Invalid choice ~") # Prompt user of invalid input  

    elif menu == "0":
        db.close()
        exit() # Close database connectiona and exit program
    else:
        print("Invalid input please select valid number option..") # Prompt user of invalid input
        continue 
        
