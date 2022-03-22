# -------------------------------------------------------------------------------------------------------------------- #
# TABLE OF CONTENTS
# Part A: Packages import
# Part B: Database class and manipulation functions
# Part C: Employee class
# Part D: ABC interface class
# Part E: Other functions
# Part F: Running the program
# -------------------------------------------------------------------------------------------------------------------- #


# Part A: Packages import
# -------------------------------------------------------------------------------------------------------------------- #
import sqlite3


# Part B: Database class and management commands.
# Defining a DBOperation class to manage all data into the database.
# -------------------------------------------------------------------------------------------------------------------- #
class DBOperations:
    # SQL queries for the different functionalities of the program.
    sql_create_table = '''CREATE TABLE Employee(
                          emp_id INTEGER PRIMARY KEY NOT NULL,
                          emp_title CHAR(2) NOT NULL,
                          emp_forename CHAR(20) NOT NULL,
                          emp_surname CHAR(20) NOT NULL,
                          emp_email VARCHAR(40) NOT NULL UNIQUE,
                          emp_salary INTEGER (20));
                       '''

    sql_insert = '''INSERT INTO employee(emp_id, emp_title, emp_forename, emp_surname, emp_email, emp_salary) VALUES
                    (?, ?, ?, ?, ?, ?);'''
    sql_select_all = "SELECT * FROM Employee ORDER BY emp_id;"
    sql_search_by_id = "SELECT * FROM Employee WHERE emp_id = ?;"
    sql_search_by_email = "SELECT * FROM Employee WHERE emp_email = ?;"
    sql_search_by_forename = "SELECT * FROM Employee WHERE emp_forename = ? ORDER BY emp_id;"
    sql_search_by_surname = "SELECT * FROM Employee WHERE emp_surname = ? ORDER BY emp_id;"
    sql_search_by_salary_greater = "SELECT * FROM Employee WHERE emp_salary >= ? ORDER BY emp_id;"
    sql_search_by_salary_less = "SELECT * FROM Employee WHERE emp_salary <= ? ORDER BY emp_id;"
    sql_update_data_forename = "UPDATE employee SET emp_forename = ? WHERE emp_id = ?;"
    sql_update_data_surname = "UPDATE employee SET emp_surname = ? WHERE emp_id = ?;"
    sql_update_data_salary = "UPDATE employee SET emp_salary = ? WHERE emp_id = ?;"
    sql_update_data_email = "UPDATE employee SET emp_email = ? WHERE emp_id = ?;"
    sql_update_data_all = '''UPDATE employee SET emp_title = ?, emp_forename = ?, emp_surname = ?,
                             emp_salary = ? WHERE emp_id = ?;'''
    sql_select_forename_by_id = "SELECT emp_forename FROM Employee WHERE emp_id = ?;"
    sql_select_surname_by_id = "SELECT emp_surname FROM Employee WHERE emp_id = ?;"
    sql_delete_data_by_id = "DELETE FROM Employee WHERE emp_id = ?;"
    sql_delete_data_all = "DELETE FROM Employee;"
    sql_drop_table = "DROP TABLE Employee;"
    sql_table_exist = '''SELECT count(name) FROM sqlite_master WHERE type = "table" AND name = "Employee";'''

    # Constructor method for DBOperation class.
    def __init__(self):
        try:
            self.conn = sqlite3.connect("ABC.db")
            self.cur = self.conn.cursor()
            self.conn.commit()
        except sqlite3.OperationalError as esql:
            print(esql)
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def get_connection(self):
        self.conn = sqlite3.connect("ABC.db")
        self.cur = self.conn.cursor()

    def table_exist(self):
        self.get_connection()
        self.cur.execute(self.sql_table_exist)
        if self.cur.fetchone()[0] == 1:
            return True
        else:
            return False

    # Creating table function.
    def create_table(self):
        try:
            self.get_connection()
            self.cur.execute(self.sql_create_table)
            self.conn.commit()
            print("\nEmployee table successfully created in ABC database.")
        except sqlite3.OperationalError:
            print("\nEmployee table already exists in ABC database.")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

        key = input('\n\nHit *Return* to exit to MAIN MENU...')

    # Inserting new employee data in the employee table.
    def insert_data(self):
        try:
            self.get_connection()
            # Creating an employee object with __init__ values from Employee class.
            emp = Employee()
            # Using setters defined in Employee class to define employee attributes.
            emp.set_emp_id(check_positive_integer("Enter Employee ID: ",
                                                  "Only positive integers are allowed, please try again",
                                                  "ID number too big, please try again."))

            emp.set_emp_title(check_alpha_title("Enter Employee Title (Mr/Ms): ",
                                                "Only alphabetical characters are accepted, please try again.",
                                                "Invalid input."))

            emp.set_emp_forename(check_alpha("Enter Employee Forename: ",
                                             "Only alphabetical characters are accepted, please try again.",
                                             "Employee forename too long, please try again."))
            emp.set_emp_surname(check_alpha("Enter Employee Surname: ",
                                            "Only alphabetical characters are accepted, please try again.",
                                            "Employee surname too long, please try again."))

            emp.set_emp_salary(check_positive_integer_sal("Enter Employee Salary(£): ",
                                                          "Only positive integers are allowed, please try again",
                                                          "Salary out of the limits, please try again."))

            # Automatic mail generation for employees.
            emp.set_emp_email((emp.get_emp_forename())[:3] + emp.get_emp_surname() + str(emp.get_emp_id()) + "@abc.com")
            # Executing SQL query for inserting data to employee table.
            # Catching error for Unique constraint error.
            try:
                self.cur.execute(self.sql_insert, tuple(str(emp).split("\n")))
                print("\nRecord successfully inserted into Employee table.")
            except sqlite3.IntegrityError as e:
                print("\nThe selected ID is already in use for a different employee in Employee table.")
                print("No employee record was inserted into Employee table.")
            self.conn.commit()
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

        key = input('\n\nHit *Return* to exit to MAIN MENU...')

    # Printing all the details for all the employees included in the employee database.
    def select_all(self):
        try:
            self.get_connection()
            self.cur.execute(self.sql_select_all)
            results = self.cur.fetchall()
            print_results(results)
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

        key = input('\n\nHit *Return* to exit to MAIN MENU...')

    # Printing the all the details of a specific employee by providing employee's ID.
    def search_data_by_id(self):
        try:
            self.get_connection()

            employeeID = check_positive_integer("Enter Employee ID: ",
                                                "Only positive integers are allowed, please try again.",
                                                "ID number too big, please try again.")
            self.cur.execute(self.sql_search_by_id, tuple(str(employeeID).split("\n")))
            result = self.cur.fetchone()
            if type(result) == type(tuple()):
                print_results([result])
            else:
                print("There is no employee with the specific ID.")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

        key = input('\n\nHit *Return* to exit to SEARCH RECORD MENU...')

    # Printing the all the details of the employee/employees by providing forename.
    def search_data_by_forename(self):
        try:
            self.get_connection()
            employeeForename = check_alpha("Enter Employee Forename: ",
                                           "Only alphabetical characters are accepted, please try again.",
                                           "Employee forename too long, please try again.")
            self.cur.execute(self.sql_search_by_forename, tuple(str(employeeForename).split("\n")))
            results = self.cur.fetchall()
            if results:
                print_results(results)
            else:
                print("There are no employees with such forename.")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

        key = input('\n\nHit *Return* to Search to SEARCH RECORD MENU...')

    # Printing the all the details of the employee/employees by providing forename.
    def search_data_by_surname(self):
        try:
            self.get_connection()
            employeeSurname = check_alpha("Enter Employee Surname: ",
                                          "Only alphabetical characters are accepted, please try again.",
                                          "Employee surname too long, please try again.")
            self.cur.execute(self.sql_search_by_surname, tuple(str(employeeSurname).split("\n")))
            results = self.cur.fetchall()
            if results:
                print_results(results)
            else:
                print("There are no employees with such surname.")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

        key = input('\n\nHit *Return* to exit to SEARCH RECORD MENU...')

    # Printing the all the details of the employee/employees by providing a salary (for value>salary).
    def search_data_by_salary_greater(self):
        try:
            self.get_connection()
            print("\nEmployee/employees with greater salary that the provided value will be printed. ")

            employeeSalary = check_positive_integer_sal("Enter Employee Salary(£): ",
                                                        "Only positive integers are allowed, please try again.",
                                                        "Salary out of the limits, please try again.")

            self.cur.execute(self.sql_search_by_salary_greater, tuple(str(employeeSalary).split("\n")))
            results = self.cur.fetchall()
            if results:
                print_results(results)
            else:
                print("There are no employees with salary equal or greater to £" + employeeSalary)
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

        key = input('\n\nHit *Return* to exit to SEARCH RECORD MENU...')

        # Printing the all the details of the employee/employees by providing a salary (for value>salary).

    def search_data_by_salary_less(self):
        try:
            self.get_connection()
            print("\nEmployee/employees with smaller salary that the provided value will be printed. ")

            employeeSalary = check_positive_integer_sal("Enter Employee Salary(£): ",
                                                        "Only positive integers are allowed, please try again.",
                                                        "Salary out of the limits, please try again.")

            self.cur.execute(self.sql_search_by_salary_less, tuple(str(employeeSalary).split("\n")))
            results = self.cur.fetchall()
            if results:
                print_results(results)
            else:
                print("There are no employees with salary equal or less to £" + employeeSalary)
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

        key = input('\n\nHit *Return* to exit to SEARCH RECORD MENU...')

    # Updating forename for an employee by providing a valid employee ID.
    def update_data_forename(self):
        try:
            self.get_connection()
            employeeID = check_positive_integer("Enter Employee ID: ",
                                                "Only positive integers are allowed, please try again.",
                                                "ID number too big, please try again.")

            self.cur.execute(self.sql_search_by_id, tuple(str(employeeID).split("\n")))
            result = self.cur.fetchone()
            if type(result) == type(tuple()):
                print_results([result])
                while True:
                    answer = input("\nWarning: Are you sure you want to update"
                                   " forename field for above employee (Y/N)? ")
                    answer = answer.lower()
                    if answer.casefold() == "y":
                        newforename = check_alpha("Enter New Employee Forename: ",
                                                  "Only alphabetical characters are accepted, please try again.",
                                                  "Employee forename too long, please try again.")
                        self.cur.execute(self.sql_update_data_forename, (newforename, employeeID))
                        self.conn.commit()
                        while True:
                            message = input("\nDo you also want to automatically update employee's mail (Y/N)?")
                            if message.casefold() == "y":
                                self.cur.execute(self.sql_select_surname_by_id, tuple(str(employeeID).split("\n")))
                                surname = "".join(self.cur.fetchone())
                                newmail = (newforename[:3] + surname + employeeID + "@abc.com")
                                print(newmail, type(newmail))
                                self.cur.execute(self.sql_update_data_email, (newmail, employeeID))
                                self.conn.commit()
                                break
                            elif message.casefold() == "n":
                                break
                            else:
                                print("Invalid answer.")
                        print("\nEmployee record successfully updated, as shown below.")
                        self.cur.execute(self.sql_search_by_id, tuple(str(employeeID).split("\n")))
                        result = self.cur.fetchone()
                        print_results([result])
                        break
                    elif answer.casefold() == "n":
                        break
                    else:
                        print("Invalid answer.")
            else:
                print("There is no employee with the specific ID.")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

        key = input('\n\nHit *Return* to exit to UPDATE RECORD MENU...')

    # Updating forename for an employee by providing a valid employee ID.
    def update_data_surname(self):
        try:
            self.get_connection()
            employeeID = check_positive_integer("Enter Employee ID: ",
                                                "Only positive integers are allowed, please try again.",
                                                "ID number too big, please try again.")

            self.cur.execute(self.sql_search_by_id, tuple(str(employeeID).split("\n")))
            result = self.cur.fetchone()
            if type(result) == type(tuple()):
                print_results([result])
                while True:
                    answer = input("\nWarning: Are you sure you want to update"
                                   " surname field for above employee (Y/N)? ")
                    answer = answer.lower()
                    if answer.casefold() == "y":

                        newsurname = check_alpha("Enter New Employee Surname: ",
                                                 "Only alphabetical characters are accepted, please try again.",
                                                 "Employee surname too long, please try again.")

                        self.cur.execute(self.sql_update_data_surname, (newsurname, employeeID))
                        self.conn.commit()
                        while True:
                            message = input("\nDo you also want to automatically update employee's mail (Y/N)?")
                            if message.casefold() == "y":
                                self.cur.execute(self.sql_select_forename_by_id, tuple(str(employeeID).split("\n")))
                                forename = "".join(self.cur.fetchone())
                                newmail = (forename[:3] + newsurname + employeeID + "@abc.com")
                                print(newmail, type(newmail))
                                self.cur.execute(self.sql_update_data_email, (newmail, employeeID))
                                self.conn.commit()
                                break
                            elif message.casefold() == "n":
                                break
                            else:
                                print("Invalid answer.")
                        print("\nEmployee record successfully updated, as shown below.")
                        self.cur.execute(self.sql_search_by_id, tuple(str(employeeID).split("\n")))
                        result = self.cur.fetchone()
                        print_results([result])
                        break
                    elif answer.casefold() == "n":
                        break
                    else:
                        print("Invalid answer.")
            else:
                print("There is no employee with the specific ID.")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

        key = input('\n\nHit *Return* to exit to UPDATE RECORD MENU...')

    # Updating salary for an employee by providing a valid employee ID.
    def update_data_salary(self):
        try:
            self.get_connection()

            employeeID = check_positive_integer("Enter Employee ID: ",
                                                "Only positive integers are allowed, please try again.",
                                                "ID number too big, please try again.")

            self.cur.execute(self.sql_search_by_id, tuple(str(employeeID).split("\n")))
            result = self.cur.fetchone()
            if type(result) == type(tuple()):
                print_results([result])
                while True:
                    answer = input("\nWarning: Are you sure you want to update salary field for above employee (Y/N)? ")
                    answer = answer.lower()
                    if answer.casefold() == "y":

                        newsalary = check_positive_integer_sal("Enter New Employee Salary(£): ",
                                                               "Only positive integers are allowed, please try again.",
                                                               "Salary out of the limits, please try again.")

                        self.cur.execute(self.sql_update_data_salary, (newsalary, employeeID))
                        self.conn.commit()
                        print("\nEmployee record successfully updated, as shown below.")
                        self.cur.execute(self.sql_search_by_id, tuple(str(employeeID).split("\n")))
                        result = self.cur.fetchone()
                        print_results([result])
                        break
                    elif answer.casefold() == "n":
                        break
                    else:
                        print("Invalid answer.")
            else:
                print("There is no employee with the specific ID.")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

        key = input('\n\nHit *Return* to exit to UPDATE RECORD MENU..')

    # Updating salary for an employee by providing a valid employee ID.
    def update_data_all(self):
        try:
            self.get_connection()

            employeeID = check_positive_integer("Enter Employee ID: ",
                                                "Only positive integers are allowed, please try again.",
                                                "ID number too big, please try again.")

            self.cur.execute(self.sql_search_by_id, tuple(str(employeeID).split("\n")))
            result = self.cur.fetchone()
            if type(result) == type(tuple()):
                print_results([result])
                while True:
                    answer = input("\nWarning: Are you sure you want to update all fields for above employee (Y/N)? ")
                    answer = answer.lower()
                    if answer.casefold() == "y":

                        newtitle = check_alpha_title("Enter Employee Title (Mr/Ms): ",
                                                     "Only alphabetical characters are accepted, please try again.",
                                                     "Invalid input.")

                        newforename = check_alpha("Enter New Employee Forename: ",
                                                  "Only alphabetical characters are accepted, please try again.",
                                                  "Employee forename too long, please try again.")

                        newsurname = check_alpha("Enter New Employee Surname: ",
                                                 "Only alphabetical characters are accepted, please try again.",
                                                 "Employee surname too long, please try again.")

                        newsalary = check_positive_integer_sal("Enter New Employee Salary(£): ",
                                                               "Only positive integers are allowed, please try again.",
                                                               "Salary out of the limits, please try again.")

                        self.cur.execute(self.sql_update_data_all,
                                         (newtitle, newforename, newsurname, newsalary, employeeID))
                        self.conn.commit()
                        while True:
                            message = input("\nDo you also want to automatically update employee's mail (Y/N)?")
                            if message.casefold() == "y":
                                newmail = (newforename[:3] + newsurname + employeeID + "@abc.com")
                                self.cur.execute(self.sql_update_data_email, (newmail, employeeID))
                                self.conn.commit()
                                break
                            elif message.casefold() == "n":
                                break
                            else:
                                print("Invalid answer.")
                        print("\nEmployee record successfully updated, as shown below.")
                        self.cur.execute(self.sql_search_by_id, tuple(str(employeeID).split("\n")))
                        result = self.cur.fetchone()
                        print_results([result])
                        break
                    elif answer.casefold() == "n":
                        break
                    else:
                        print("Invalid answer.")
            else:
                print("There is no employee with the specific ID.")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

        key = input('\n\nHit *Return* to exit to UPDATE RECORD MENU...')

    # Deleting specific data from the table.
    # The user will need to input the employee id to delete the corresponding record.
    def delete_data_by_id(self):
        try:
            self.get_connection()
            employeeID = check_positive_integer("Enter Employee ID: ",
                                                "Only positive integers are allowed, please try again.",
                                                "ID number too big, please try again.")

            self.cur.execute(self.sql_search_by_id, tuple(str(employeeID).split("\n")))
            result = self.cur.fetchone()
            if type(result) == type(tuple()):
                print_results([result])
                while True:
                    answer = input("\nWarning: Are you sure you want to delete the above employee"
                                   " from the records (Y/N)? ")
                    answer = answer.lower()
                    if answer.casefold() == "y":
                        self.cur.execute(self.sql_delete_data_by_id, tuple(str(employeeID).split("\n")))
                        self.conn.commit()
                        print("Employee successfully deleted from Employee table.")
                        break
                    elif answer.casefold() == "n":
                        break
                    else:
                        print("Invalid answer.")
            else:
                print("There is no employee with the specific ID.")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

        key = input('\n\nHit *Return* to exit to DELETE RECORD MENU..')

    # Deleting all records from Employee table.
    def delete_data_all(self):
        try:
            self.get_connection()
            while True:
                answer = input("\nWarning: Are you sure you want to delete all records from Employee table (Y/N)? ")
                answer = answer.lower()
                if answer == "y":
                    self.cur.execute(self.sql_delete_data_all)
                    self.conn.commit()
                    print("All records successfully deleted.")
                    break
                elif answer == "n":
                    break
                else:
                    print("Invalid answer.")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

        key = input('\n\nHit *Return* to exit to DELETE RECORD MENU...')

    # Dropping Employee table from database.
    def drop_table(self):
        try:
            self.get_connection()
            while True:
                answer = input("\nWarning: Are you sure you want to drop Employee table from ABC database (Y/N)? ")
                answer = answer.lower()
                if answer == "y":
                    self.cur.execute(self.sql_drop_table)
                    self.conn.commit()
                    print("Employee table successfully dropped from ABC database.")
                    break
                elif answer == "n":
                    break
                else:
                    print("Invalid answer.")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

        key = input('\n\nHit *Return* to exit to DELETE RECORD MENU...')


# Part B: Employee Class
# -------------------------------------------------------------------------------------------------------------------- #
class Employee:

    # Constructor for Employee class - self represents the instance of the class.
    def __init__(self):
        self.employeeID = 0
        self.empTitle = ''
        self.forename = ''
        self.surname = ''
        self.email = ''
        self.salary = 0.0

    # Following functions set employee column values
    def set_emp_id(self, emp_id):
        self.employeeID = emp_id

    def get_emp_id(self):
        return self.employeeID

    def set_emp_title(self, emp_title):
        self.empTitle = emp_title

    def set_emp_forename(self, emp_forename):
        self.forename = emp_forename

    def get_emp_forename(self):
        return self.forename

    def set_emp_surname(self, emp_surname):
        self.surname = emp_surname

    def get_emp_surname(self):
        return self.surname

    def set_emp_email(self, emp_email):
        self.email = emp_email

    def set_emp_salary(self, emp_salary):
        self.salary = emp_salary

    def __str__(self):
        return str(self.employeeID) + "\n" + self.empTitle + "\n" + self.forename + "\n" + self.surname + \
               "\n" + self.email + "\n" + str(self.salary)


# Part D. ABC interface class
# -------------------------------------------------------------------------------------------------------------------- #
class ABCInterface:

    @staticmethod
    def main_menu():
        ABCInterface.print_logo()
        while True:
            print("\n")
            print("+--------------------------------------------+")
            print("|ABC ADMINISTRATOR MAIN MENU                 |")
            print("+--------------------------------------------+")
            print("|1. Create Table Employee                    |")
            print("|2. Insert New Employee Record               |")
            print("|3. Select All Employee Records              |")
            print("|4. Search Employee/Employees Records        |")
            print("|5. Update Employee Record                   |")
            print("|6. Delete Employee/Employees Records        |")
            print("|7. Open *HELP*                              |")
            print("|0. Exit                                     |")
            print("+--------------------------------------------+")

            # User's choice can only be an integer.
            __selection__ = input("Enter your choice: ")

            # Creating an object instance of the DBOperations class.
            db_ops = DBOperations()

            if __selection__ == "1":
                db_ops.create_table()
            elif __selection__ == "2":
                if db_ops.table_exist():
                    db_ops.insert_data()
                else:
                    print("No table has been created yet. Please create Employee table from the Main Menu options.")
            elif __selection__ == "3":
                if db_ops.table_exist():
                    db_ops.select_all()
                else:
                    print("No table has been created yet. Please create Employee table from the Main Menu options.")
            elif __selection__ == "4":
                if db_ops.table_exist():
                    ABCInterface.search_menu()
                else:
                    print("No table has been created yet. Please create Employee table from the Main Menu options.")
            elif __selection__ == "5":
                if db_ops.table_exist():
                    ABCInterface.update_menu()
                else:
                    print("No table has been created yet. Please create Employee table from the Main Menu options.")
            elif __selection__ == "6":
                if db_ops.table_exist():
                    ABCInterface.delete_menu()
                else:
                    print("No table has been created yet. Please create Employee table from the Main Menu options.")
            elif __selection__ == "7":
                ABCInterface.help()
            elif __selection__ == "0":
                print("\nConnection with the ABC database is now terminated.")
                exit(0)
            else:
                print("Invalid Choice")
                key = input('\n\nHit *Return* to exit to MAIN MENU...')

    @staticmethod
    def search_menu():

        while True:
            print("\n")
            print("+--------------------------------------------+")
            print("|ABC SEARCH RECORD MENU                      |")
            print("+--------------------------------------------+")
            print("|1. Search Employee                   (by ID)|")
            print("|2. Search Employee/Employees   (by Forename)|")
            print("|3. Search Employee/Employees    (by Surname)|")
            print("|4. Search Employee/Employees   (by Salary >)|")
            print("|5. Search Employee/Employees   (by Salary <)|")
            print("|0. Exit to Main Menu                        |")
            print("+--------------------------------------------+")

            # User's choice can only be an integer.
            __selection__ = input("Enter your choice: ")

            # Creating an object instance of the DBOperations class.
            db_ops = DBOperations()

            if __selection__ == "1":
                db_ops.search_data_by_id()
            elif __selection__ == "2":
                db_ops.search_data_by_forename()
            elif __selection__ == "3":
                db_ops.search_data_by_surname()
            elif __selection__ == "4":
                db_ops.search_data_by_salary_greater()
            elif __selection__ == "5":
                db_ops.search_data_by_salary_less()
            elif __selection__ == "0":
                break
            else:
                print("Invalid choice")
                key = input('\n\nHit *Return* to exit to SEARCH RECORD MENU...')

    @staticmethod
    def update_menu():

        while True:
            print("\n")
            print("+--------------------------------------------+")
            print("|ABC UPDATE RECORD MENU                      |")
            print("+--------------------------------------------+")
            print("|1. Update Employee Forename                 |")
            print("|2. Update Employee Surname                  |")
            print("|3. Update Employee Salary                   |")
            print("|4. Update Employee Entire Record            |")
            print("|0. Exit to Main Menu                        |")
            print("+--------------------------------------------+")

            # User's choice can only be an integer.
            __selection__ = input("Enter your choice: ")

            # Creating an object instance of the DBOperations class.
            db_ops = DBOperations()

            if __selection__ == "1":
                db_ops.update_data_forename()
            elif __selection__ == "2":
                db_ops.update_data_surname()
            elif __selection__ == "3":
                db_ops.update_data_salary()
            elif __selection__ == "4":
                db_ops.update_data_all()
            elif __selection__ == "0":
                break
            else:
                print("Invalid choice")
                key = input('\n\nHit *Return* to exit to UPDATE RECORD MENU..')

    @staticmethod
    def delete_menu():

        while True:
            print("\n")
            print("+--------------------------------------------+")
            print("|ABC DELETE RECORD MENU                      |")
            print("+--------------------------------------------+")
            print("|1. Delete Employee Record            (by ID)|")
            print("|2. Delete All Employees Records             |")
            print("|3. Delete/Drop Employee Table  (from ABC DB)|")
            print("|0. Exit to Main Menu                        |")
            print("+--------------------------------------------+")

            # User's choice can only be an integer.
            __selection__ = input("Enter your choice: ")

            # Creating an object instance of the DBOperations class.
            db_ops = DBOperations()

            if __selection__ == "1":
                db_ops.delete_data_by_id()
            elif __selection__ == "2":
                db_ops.delete_data_all()
            elif __selection__ == "3":
                db_ops.drop_table()
            elif __selection__ == "0":
                break
            else:
                print("Invalid choice")
                key = input('\n\nHit *Return* to exit to DELETE RECORD MENU...')

    @staticmethod
    def help():
        print("\n")
        print("+--------------------------------------------------------------------------------+")
        print("|WELCOME TO HELP MENU                                                            |")
        print("+--------------------------------------------------------------------------------+")
        print("|This is a help guide which explains how the users can interact with ABC program.|")
        print("|This program allows the management of employees' data for ABC company.          |")
        print("|Data manipulation is achieved through a variety of functionalities.             |")
        print("|ABC functionalities (for each MENU) are explained in the following section.     |")
        print("+--------------------------------------------------------------------------------+")
        key = input("\nHit *Return* to continue to MAIN MENU functionalities...")
        print("+--------------------------------------------------------------------------------+")
        print("|Functionalities that can be reached from MAIN MENU:                             |")
        print("|(1) Create initial table Employee in ABC database - a table should be created   |")
        print("|    prior trying to run any other functionality.                                |")
        print("|(2) Insert new employee record into the Employee table. The user is prompted to |")
        print("|    enter the following information:                                            |")
        print("|    > ID:       only positive integers are accepted - ID should be unique       |")
        print("|    > Title:    only Mr or Ms are accepted                                      |")
        print("|    > Forename: only alphabetical characters are accepted                       |")
        print("|    > Surname:  only alphabetical characters are accepted                       |")
        print("|    > Salary:   only positive integers are accepted                             |")
        print("|    Employee's mail is automatically generated by combining employee's forename,|")
        print("|    surname and ID.                                                             |")
        print("|(3) Print all information for all employees in Employees' table.                |")
        print("|(4) Search Employee/Employees records: opens SEARCH RECORD MENU.                |")
        print("|(5) Update Employee/Employees records: opens UPDATE RECORD MENU.                |")
        print("|(6) Delete Employee/Employees records: opens DELETE RECORD MENU.                |")
        print("+--------------------------------------------------------------------------------+")
        key = input("\nHit *Return* to continue to SEARCH RECORD MENU functionalities...")
        print("+--------------------------------------------------------------------------------+")
        print("|Functionalities that can be reached from SEARCH RECORD MENU:                    |")
        print("|(1) Search and print information for a specific employee by providing an ID.    |")
        print("|(2) Search and print information for employee/employees by providing a name.    |")
        print("|(3) Search and print information for employee/employees by providing a surname. |")
        print("|(4) Search and print information for employee/employees with salary great or    |")
        print("|    equal to the provided one by the user.                                      |")
        print("|(5) Search and print information for employee/employees with salary smaller or  |")
        print("|    equal to the provided one by the user.                                      |")
        print("+--------------------------------------------------------------------------------+")
        key = input("\nHit *Return* to continue to UPDATE RECORD MENU functionalities...")
        print("+--------------------------------------------------------------------------------+")
        print("|Functionalities that can be reached from UPDATE RECORD MENU:                    |")
        print("|(1) Update the forename of a specific employee by providing an  ID.             |")
        print("|    User can select if he also wants to automatically update email.             |")
        print("|(2) Update the surname of a specific employee by providing an  ID.              |")
        print("|    User can select if he also wants to automatically update email.             |")
        print("|(3) Update the salary of a specific employee by providing an  ID.               |")
        print("|(4) Update the entire record of a specific employee by providing an  ID.        |")
        print("|    User can select if he also wants to automatically update email.             |")
        print("+--------------------------------------------------------------------------------+")
        key = input("\nHit *Return* to continue TO DELETE RECORD MENU functionalities...")
        print("+--------------------------------------------------------------------------------+")
        print("|Functionalities that can be reached from DELETE RECORD MENU:                    |")
        print("|(1) Delete a specific employee record from Employee table by providing an ID.   |")
        print("|(2) Delete all employees records form Employee table (produces an empty table). |")
        print("|(3) Delete Employee table from ABC record (and all the stored employee records).|")
        print("+--------------------------------------------------------------------------------+")
        key = input("\nHit *Return* to exit HELP MENU and go back to MAIN MENU...")

    @staticmethod
    def print_logo():
        print('''
+-----------------------------------------------------+
|      AAAAAAA      BBBBBBBBBB    CCCCCCCCCCCC        |
|     AAA   AAA     BBB    BBB    CCC                 |
|    AAA     AAA    BBB    BBB    CCC                 |
|   AAAAAAAAAAAAA   BBBBBBBBBBBBB CCC                 |
|  AAA         AAA  BBB       BBB CCC                 |
| AAA           AAA BBBBBBBBBBBBB CCCCCCCCCCCC        |
|                                              LIMITED|
+-----------------------------------------------------+
        ''')


# Part E. Other functions
# -------------------------------------------------------------------------------------------------------------------- #
def print_results(rows):
    # Printing results' table.
    print("+" + 5 * "-" + "+" + 6 * "-" + "+" + 25 * "-" + "+" + 25 * "-" + "+" + 35 * "-" + "+" + 10 * "-" + "+")
    print("|" + "ID" + 3 * " " + "|" + "TITLE" + 1 * " " + "|" + "FORENAME" + 17 * " " + "|" + "SURNAME"
          + 18 * " " + "|" + "EMAIL" + 30 * " " + "|" + "SALARY(£)" + 1 * " " + "|")
    print("+" + 5 * "-" + "+" + 6 * "-" + "+" + 25 * "-" + "+" + 25 * "-" + "+" + 35 * "-" + "+" + 10 * "-" + "+")
    for row in rows:
        print("|" + "%04d" % row[0], "|" + "%-5s" % row[1], "|" + "%-24s" % row[2], "|" + "%-24s" % row[3],
              "|" + "%-34s" % row[4], "|" + "%9d" % row[5], "|")
    print("+" + 5 * "-" + "+" + 6 * "-" + "+" + 25 * "-" + "+" + 25 * "-" + "+" + 35 * "-" + "+" + 10 * "-" + "+")


def check_positive_integer(prompt, message1, message2):
    while True:
        inp = input(prompt)
        try:
            number = int(inp)
            if number <= 0:
                print(message1)
                continue
            elif number > 999:
                print(message2)
                continue
            break
        except ValueError:
            print(message1)
    return inp


def check_positive_integer_sal(prompt, message1, message2):
    while True:
        inp = input(prompt)
        try:
            number = int(inp)
            if number <= 0:
                print(message1)
                continue
            elif number < 1000 or number > 1000000000:
                print(message2)
                continue
            break
        except ValueError:
            print(message1)
    return inp


def check_alpha(prompt, message1, message2):
    while True:
        inp = input(prompt)
        try:
            if not inp.isalpha():
                print(message1)
                continue
            elif len(inp) > 20:
                print(message2)
                continue
            break
        except Exception as e:
            print(message1)
    inp = inp.lower()
    inp = inp.capitalize()
    return inp


def check_alpha_title(prompt, message1, message2):
    while True:
        title = check_alpha(prompt, message1, message2)
        if title == "Mr" or title == "Ms":
            break
        else:
            print("Invalid input.")
            continue
    return title


# Part F. Running the program
# -------------------------------------------------------------------------------------------------------------------- #
ABCInterface.main_menu()
