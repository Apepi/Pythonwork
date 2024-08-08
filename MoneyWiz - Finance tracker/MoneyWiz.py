import sqlite3
import datetime

# Function to check if target date is exceeded or not
def daysLeft(finalstr_datetime):    
    import datetime
    current_time = datetime.datetime.now()     
    if finalstr_datetime > current_time:   
        return f"with {(finalstr_datetime-current_time).days} days left."
    else:
        return f"target date exceeded by {(current_time-finalstr_datetime).days} days."
  

# Function to enumerate lists and print out for user to see
def listed_categories(x):    
    for i, catergories in enumerate(x):
        print(f"{i+1}. {catergories}")
    
# Function to check user input is valid float
def amount_for_table():
    while True:
        try:
            user_amount = float(input("Please input the amount: R"))
        except ValueError:
            print("Invalid input, it must be a numerical value.")
        else:
            break
    return user_amount

    
db = sqlite3.connect('moneywiz.db') # Connecting to the database
cursor = db.cursor() # Creating a cursor object

# Creating a table 'expenses'
cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses(id INTEGER PRIMARY KEY, category TEXT,
                   	amount INTEGER)
''')  

# Creating a table 'income'
cursor.execute('''
    CREATE TABLE IF NOT EXISTS income(id INTEGER PRIMARY KEY, category TEXT,
                   	amount INTEGER)
''')

# Creating a table 'budget'
cursor.execute('''
    CREATE TABLE IF NOT EXISTS budget(id INTEGER PRIMARY KEY, category TEXT,
                   	amount INTEGER)
''')

# Creating a table 'goals'
cursor.execute('''
    CREATE TABLE IF NOT EXISTS goals(id INTEGER PRIMARY KEY, name TEXT, category TEXT,
                   	target_amount INTEGER, current_goal_amount INTEGER, target_date TEXT)
''') 

db.commit()

# Creating two lists of categories for incomes and expenses
category_list = ["Entertainment", "Food", "Transport", "Medical", "Household", "Cash Withdraw", "Insurance", "Loans & Accounts", "Personal & Family", "Other"]
income_category_list = ["Allowance", "Insurance Payout", "Investment Income", "Other Income", "Rental Income", "Salary", "Transfers"]

while True:
    # Menu for user to choose from
    menu = input('''\t\t$ MoneyWiz $\n
1. Add expense
2. View expenses
3. View expenses by category
4. Add income
5. View income
6. View income by category
7. Set budget for a category
8. View budget for a category
9. Set financial goals
10. View progress towards financial goals
11. Quit\n                 
Please choose an option from the menu: ''')

    if menu == "1":
        listed_categories(category_list)
        # Check to ensure user input is a int and within the required list range
        while True:
            try:
                expense_choice = int(input("\nPlease select from the expense categories: "))
            except ValueError:
                print("Invalid choice..")
            if expense_choice > 10 or expense_choice <  1:
                print("Please select from the available category options.")
            else:
                break        
        cursor.execute(''' INSERT INTO expenses(category, amount)
                    VALUES(?,?)''', (category_list[expense_choice-1], amount_for_table())) # Inserting data into table
        db.commit()

    # Code to collect all expenses and sum them
    elif menu =="2":
        cursor.execute('''SELECT amount FROM expenses''')
        total_expenses = cursor.fetchall()
        summed_expenses = round(sum(map(sum,total_expenses)), 2)# learned about this map() and round() function through: GeeksforGeeks (2023a) Python: Summation of tuples in list, GeeksforGeeks. Available at: https://www.geeksforgeeks.org/python-summation-of-tuples-in-list/ (Accessed: 20 May 2024). 
                                                                # GeeksforGeeks (2023b) Round() function in Python, GeeksforGeeks. Available at: https://www.geeksforgeeks.org/round-function-python/ (Accessed: 20 May 2024). 
        print("------------------------------------------")
        print(f"Total expenses = R{summed_expenses}")
        print("------------------------------------------") 

    # Code to select all expense data from database and list it for user to view
    elif menu =="3":
        print("------------------------------------------")
        print("\t\t Expense$\n")
        for items in category_list:
           cursor.execute('''SELECT amount FROM expenses WHERE category=?''', (items,))
           category_amount = cursor.fetchall()
           total_category_amount = round(sum(map(sum,category_amount)), 2)
           print(f"- {items} = R{total_category_amount}")
        print("------------------------------------------")

    # Code to add Income to the tracker app database
    elif menu =="4":
        listed_categories(income_category_list)
        # Again another validity check on the user input
        while True:
            try:
                income_choice = int(input("\nPlease select from the income categories: "))
            except ValueError:
                print("Invalid choice..")
            if income_choice > 7 or income_choice <  1:
                print("Please select from the available category options.")
            else:
                break        
        cursor.execute(''' INSERT INTO income(category, amount)
                    VALUES(?,?)''', (income_category_list[income_choice-1], amount_for_table())) # Inserting data into table
        db.commit()

    # Code to summize all income and display it for user
    elif menu =="5":
        cursor.execute('''SELECT amount FROM income''')
        total_income = cursor.fetchall()
        summed_income = round(sum(map(sum,total_income)), 2)
        print("------------------------------------------")
        print(f"Total income = R{summed_income}")
        print("------------------------------------------")

    # Code to List all logged incomes within tracker app database
    elif menu =="6":
        print("------------------------------------------")
        print("\t\t Income$\n")
        for items in income_category_list:
           cursor.execute('''SELECT amount FROM income WHERE category=?''', (items,))
           category_amount = cursor.fetchall()
           total_category_amount = round(sum(map(sum,category_amount)), 2)
           print(f"- {items} = R{total_category_amount}")
        print("------------------------------------------")

    # Code to allow user to add budget for expense categories
    elif menu =="7":
        print("\n\t\t$ MoneyWiz Budgeting $\n")
        listed_categories(category_list)
        while True:
            try:
                category_choice = int(input("\nPlease select from the categories above: "))
            except ValueError:
                print("Invalid choice..")
            if category_choice > 10 or category_choice <  1:
                print("Please select from the available category options.")
            else:
                break            
        cursor.execute(''' INSERT INTO budget(category, amount)
                    VALUES(?,?)''', (category_list[category_choice-1], amount_for_table())) # Inserting data into table
        db.commit()

    elif menu =="8":
        print("\n\t\t$ MoneyWiz Budgeting $\n")
        listed_categories(category_list)
        # lists all expense categories for user to choose from
        while True:
            try:
                category_choice = int(input("\nWhich budget would you like to look at?  "))
            except ValueError:
                print("Invalid choice..")
            if category_choice > 10 or category_choice <  1:
                print("Please select from the available budget options.")
            else:
                break
        cursor.execute('''SELECT amount FROM budget WHERE category=?''', (category_list[category_choice-1],))
        category_amount = cursor.fetchall()
        total_category_amount = round(sum(map(sum,category_amount)), 2)
        print("-----------------------------------------------------------")
        print(f"Current Budget for {category_list[category_choice-1]} is: R{total_category_amount}") # Prints budget name and allowcated budget for this category
        cursor.execute('''SELECt amount FROM expenses WHERE category=?''', (category_list[category_choice-1],))
        current_expense_amount = cursor.fetchall()
        overall_expense_amount = round(sum(map(sum,current_expense_amount)), 2)
        print(f"Current logged expenses within {category_list[category_choice-1]} is: R{overall_expense_amount}") # Prints all the summed logged expenses within the category
        if total_category_amount > overall_expense_amount: # Check if over or under budget and supply appropriate message
            print(f"Well done you are within the budget and have: R{total_category_amount - overall_expense_amount} left.")
        else:
            print(f"You have exceeded your budget by: R{overall_expense_amount - total_category_amount}")
        print("-----------------------------------------------------------")

    # Code to allow user to add new goal or add to an existing goal
    elif menu =="9":
        print("\t\t$ MoneyWiz Goalz $")
        print('''1. New Goal
2. Add to current Goal ''')
        goal_menu_choice = input(" Select menu option: ")
        # Code to add goal and check user amount input
        if goal_menu_choice == "1":
            print("---------------------------------------------------------")
            goal_name = input("Enter goal name: ")
            while True:
                try:
                    target_amount = int(input("Enter target goal amount: "))
                except ValueError:
                    print("Invalid Input, please try again.")
                else:
                    break
            current_goal_amount = 0
            listed_categories(category_list)
            goal_category = int(input("Choose a category: "))           
            # Loop to ensure user inputs correct date format for the target date on goal
            while True:
                from datetime import datetime                
                date_check = True
                format = "%Y-%m-%d"
                try:
                    goal_targetdate = input ("Enter target date (YYYY-MM-DD): ")
                    date_check = bool(datetime.strptime(goal_targetdate, format))
                except ValueError:
                    print("Incorrect Format pelase enter correct date format.")
                    date_check = False
                else:
                    break
            cursor.execute(''' INSERT INTO goals(name, category, target_amount, current_goal_amount, target_date)
                    VALUES(?,?,?,?,?)''', (goal_name, category_list[goal_category-1], target_amount, current_goal_amount, goal_targetdate)) # Inserting data into table
            db.commit()        
            print("Goal added successfully!")
            print("---------------------------------------------------------")
        # Code to add amount towards set goal
        elif goal_menu_choice == "2":                
            cursor.execute('''SELECT DISTINCT name FROM goals ''') # Use of DISTINCT name here to ensure it doesnt print duplciate goal names
            all_goals = cursor.fetchall()
            for i, goal in enumerate(all_goals):
                print(f"{i+1}. {''.join(goal)}")
            while True:
                    try:                    
                        user_choice = int(input("Please select goal to add to: "))                        
                    except ValueError:
                        print("Invalid input")
                    else:
                        break
            while True:
                try:
                    updated_amount = int(input("How much would you like to add towards your goal: R"))
                except ValueError:
                    print("Invalid input, it needs to be a numerical value")
                else:
                    break
            goal_list =[] # Create goal list
            # Loop to populate list
            for goal in all_goals:
                goal_list.append(''.join(goal))             
            cursor.execute(''' INSERT INTO goals(name, current_goal_amount)
                           VALUES(?,?)''', (goal_list[user_choice-1], updated_amount))
            cursor.execute(''' SELECT category FROM goals WHERE name =?''', (goal_list[user_choice-1],)) # Find the category of the relavent Goal thats being added to
            selected_goal_category = cursor.fetchone()
            cursor.execute(''' INSERT INTO expenses (category, amount)
                    VALUES(?,?)''', (''.join(selected_goal_category), updated_amount)) # Add added goal amount to its relavent expense category
            db.commit()

    elif menu =="10":
        cursor.execute('''SELECT DISTINCT name FROM goals ''')
        all_goals = cursor.fetchall()
        print("---------------------------------------------------------")
        print("\t\t\t WiZBudget$\n")
        # loop to fetch current and target amount then calculate completion % and if its within the dealine       
        for goals in all_goals:
            cursor.execute(''' SELECT current_goal_amount FROM goals WHERE name=? ''', (goals))
            total_goal_amounts = cursor.fetchall()            
            sum_amount = round(sum(map(sum,total_goal_amounts)), 2)            
            cursor.execute(''' SELECT target_amount FROM goals WHERE name=? ''', (goals))
            target = cursor.fetchone()            
            result_target = int(''.join(map(str, target))) 
            progress_sum = round((sum_amount/result_target * 100), 2)
            cursor.execute(''' SELECT target_date FROM goals WHERE name=? ''', (goals))
            target_date = cursor.fetchone()
            strdate = ''.join(target_date)
            import datetime            
            finalstr_datetime = datetime.datetime.strptime(strdate, "%Y-%m-%d")                                               
            print(f"- {''.join(goals)} is {progress_sum}% complete, {daysLeft(finalstr_datetime)}")
        print("---------------------------------------------------------")
        print()

    # Code to close connection to database at end of session
    elif menu =="11":
        print("Thank you for using $ MoneyWiz $")        
        db.close()
        exit()
    # Code to repeat the loop if invalid menue choice is chosen
    else:
        print("Invalid menu choice. Please select from the available options.")
        continue

