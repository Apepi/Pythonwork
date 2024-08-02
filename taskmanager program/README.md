# Task Management System

A simple command-line task management application using Python with text file-based data storage.

## Features

- User authentication
- Add new users (admin only)
- Add tasks and assign to users
- View all tasks
- View tasks assigned to the current user
- View total number of users and tasks (admin only)
- Basic error handling and input validation

## Quick Start

1. Ensure Python 3.x is installed
2. Place `user.txt` and `task.txt` in the same directory as the script
3. Run `python taskamanagement.py`
4. Log in with existing credentials or use admin account to add new users

## Usage

After logging in, choose from the following options:
- r - register a user (admin only)
- a - add task
- va - view all tasks
- vm - view my tasks
- ta - total users and tasks (admin only)
- e - exit

## Data Storage

- User data stored in `user.txt`
- Task data stored in `task.txt`

## Requirements

- Python 3.x
- No additional libraries needed

## Future Improvements

- Database integration
- Task editing and deletion
- User role management
- Improved data validation and error handling

Contributions are welcome!
