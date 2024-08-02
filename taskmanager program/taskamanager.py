import datetime

# Function to request and verify user inputs for username and password
def add_new_user():    
    new_user = input("| Please type new username: ").lower()  
    while new_user in access_dict.keys():
        new_user = input("| Username already exists, try again: ").lower()  

    while True: 
        new_pass = input("| Please type in desired password: ")
        check_pass = input("| Please re-enter password: ")
        if check_pass == new_pass:
            # Write new username and password to user.txt file
            login.write(f"\n{new_user}, {new_pass}")
            print("| New user added successfully!\n|")
            break
        else:
            print("| Passwords do not match")   
    return access_dict

# Welcome message to be displayed on initiation
def welcome_msg():
    print("|======================================|")  
    print("|    T   A   S  K      ^       U   P   |")
    print("|======================================|")
    print("|            ~~ Welcome ~~             ")

# Function to check if user input date matches required format 
def check_date():
    format = "%Y-%m-%d"
    global test_date    
    task_due = input("| Type due date (please use yyyy-mm-dd format): ")
    try:
        test_date = bool(datetime.strptime(task_due, format))        
    except ValueError:    
        print("| Incorrect Format")
    return task_due

# Function for asking about new task inputs and writing them in specific format to txt file
def add_new_task():
    task_title = input("| Type task title here: ")
    task_descrip = input("| Type description of task below:\n| ")
    check_date()
    task_status = "No"    
    f.write(f"{task_title}, {user_task}, {current_time}, {check_date()}, {task_status}, {task_descrip}\n")    
    print("| Task added Successfully!\n|")

# Function for formatting how task information is displayed once read from txt file
def task_output():
    global i    
    task_list.append(lines.split(', ', 5))
    each_task = task_list[i]                                 
    print("--------------------------------------------------")
    print("")
    print(f"Task:              {each_task[0]}")
    print(f"Assigned to:       {each_task[1]}")
    print(f"Date assigned:     {each_task[2]}")
    print(f"Due date:          {each_task[3]}")
    print(f"Task complete?     {each_task[4]}")
    print(f"Task description:\n{each_task[5]}")
    print("--------------------------------------------------")
    i += 1

# Login Section
while True:
    with open('user.txt', 'r') as login:
        access_dict = {}
        details = login.readlines()
        # Create dictionary from lines in user.txt file
        # Storing username as key and password as value
        for deets in details:
            key, value = deets.split(', ')            
            access_dict[key] = value.strip()

        welcome_msg()                    
        user_name = input("| Username: ")
        if user_name in access_dict.keys():                             
           user_pass = input("| Password: ")
           if user_pass == access_dict[user_name]:
               print(f"| Login successful! Welcome {user_name}\n|")
               break
           else:               
               tries = 3
               while user_pass != access_dict[user_name]:
                   print(f"| Password Incorrect, {tries} attempts remaining\n|")
                   user_pass = input("| Please type in your password: ")
                   tries -= 1
                   if tries == 0:
                       print("| \n| Too many attempts...\n|")
                       break
               else:
                   break                      
        else:
            print("User login incorrect, try again..")
            continue

while True:
    with open('task.txt', 'a+') as f:
        if user_name == "admin":
            menu = input('''| Select one of the following options:
            | r - register a user
            | a - add task
            | va - view all tasks
            | vm - view my tasks
            | ta - Total users and tasks
            | e - exit
            | :  ''').lower()
        else:
            menu = input('''| Select one of the following options:
            | a - add task
            | va - view all tasks
            | vm - view my tasks            
            | e - exit
            | :  ''').lower()

        if menu == 'r':
            with open('user.txt', 'a+') as login:       
                if user_name == "admin":
                    # Add new user if user is admin
                    add_new_user()
                else:
                    print("| You have entered an invalid input. Please try again")
                    continue
                while True:
                    user_check = input("| Would you like to add another user? y/n: ").lower()
                    if user_check == "y":
                        add_new_user()
                    elif user_check == "n":
                        print("")
                        break
                    elif user_check != "y" or user_check != "n":
                        print("| Invalid input...")            
                          
        elif menu == 'a':
            current_time = date.today()
            access_dict = {}
            details = t.readlines()
            for deets in details:
                key, value = deets.split(', ')            
                access_dict[key] = value.strip()

            user_task = input("| Type the user you would like to assign this task: ")
            if user_task in access_dict.keys():                    
                add_new_task()
            else:
                while user_task not in access_dict.keys():
                    user_task = input("| User not found please re-enter username: ")                   
                add_new_task()
                continue

        elif menu == 'va':
            with open('task.txt', 'r') as t:
                task_list = []
                i = 0            
                for lines in t:
                    # Display all tasks
                    task_output()
                
        elif menu == 'vm':
            with open('task.txt', 'r') as t:
                task_list = []
                i = 0
                for lines in t:
                    if user_name in lines:
                        # Display tasks assigned to the current user
                        task_output()           

        elif menu == 'ta':
            if user_name == 'admin':            
                with open('user.txt', 'r') as login:
                    all_user = login.readlines()
                    print("----------------------------------------\n")
                    print(f"| Total users:         {len(all_user)}")
                with open('task.txt', 'r') as t:
                    all_task = t.readlines()
                    print(f"| Total current tasks: {len(all_task)}\n")
                    print("----------------------------------------")
            else:
                print("| You have entered an invalid input. Please try again")
                continue

        elif menu == 'e':
            print('|            ~~~ Goodbye ~~~')
            exit()

        else:
            print("| You have entered an invalid input. Please try again")
