#====imported modules====
import datetime


#new user function requests and verifies user inputs for user and pass
#Then writes values with ", " seperator to user.txt file
def add_new_user():    
    new_user = input("| Please type new username: ").lower()  
    while new_user in access_dict.keys():
        new_user = input("| Username already exists try again: ").lower()  

    while True: 
        new_pass = input("| Please type in desired password: ")
        check_pass = input("| Please re-enter pasword: ")
        if check_pass == new_pass:
            login.write(f"\n{new_user}, {new_pass}")
            print("| New user added successfully!\n|")
            break
        else:
            print("| Passwords do not match")   
    return access_dict

#welcome message to be displayed up initiation
def welcome_msg():
    print("|======================================|")  
    print("|    T   A   S  K      ^       U   P   |")
    print("|======================================|")
    print("|            ~~ Weclome ~~             ")

#function to check user input date matches format required 
def check_date():
    from datetime import datetime
    format = "%Y-%m-%d"
    global test_date    
    task_due = input("| Type due date (please use yyyy-mm-dd format): ")
    try:
        test_date = bool(datetime.strptime(task_due, format))        
    except ValueError:    
        print("| Incorrect Format")
    return task_due
    
#function for asking about new task inputs and writes them in specific format to txt file
def add_new_task():
    task_title = input("| Type task title here: ")
    task_descrip = input("| Type description of task below:\n| ")
    check_date()
    task_status = "No"    
    f.write(f"{task_title}, {user_task}, {current_time}, {check_date()}, {task_status}, {task_descrip}\n")    
    print("| Task added Successfully!\n|")

#function for formating how task infomation is displayed once read from txt file
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

#====Login Section====
while True:
    #create dictionary from lines in txt file
    #storing username as key and pass as value
    with open('user.txt', 'r') as login:
        access_dict = {}
        details = login.readlines()
        for deets in details:
            key, value = deets.split(', ')            
            access_dict[key] = value.strip()

        #checking that username and pass in dictionary
        welcome_msg()                    
        user_name = input("| Username: ")
        if user_name in access_dict.keys():                             
           user_pass = input("| Password: ")
           if user_pass == access_dict[user_name]:
               print(f"| login successful! Welcome {user_name}\n|")
               break
           else:               
               tries = 3
               #if pass incorrect user is allowed the attempts
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
            print("User login incorrect try again..")
            continue

    
while True:
    with open('task.txt', 'a+') as f:
        #presenting users with login menu
        #admins get a separate menu
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
            #if r is selected confirms user is admin before following sequence
            #admin is allowed to add multiple users
            with open('user.txt', 'a+') as login:       
                if user_name == "admin":
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
            #set date and time to current date/time of pc
            #recreates dictionary of users.txt and verifies new task is assigned to registered user
            #user is asked it input various task variables. once complete all info is written to task.txt
            with open('user.txt', 'r') as t:
                test_date = True
                from datetime import date
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
            #reads each line of task.txt then splits lines and stores values in a list
            #list items are run through function to be displayed in a pleasant format
            with open('task.txt', 'r') as t:
                task_list = []
                i = 0            
                for lines in t:
                    task_output()
                
        elif menu == 'vm':
            #read task.txt and splits lines to make list
            #lines that include the username are taken and printed in pleasant format
            with open('task.txt', 'r') as t:
                task_list = []
                i = 0
                for lines in t:
                    if user_name in lines:
                        task_output()           

        elif menu == 'ta':
            #only admin function
            #reads all lines in user.txt and task.txt calculates length of lines and prints out the value
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