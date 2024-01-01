import sqlite3

# Connect to SQLite database (creates a new file if it doesn't exist)
db = sqlite3.connect("atm_simulator.db")

# Create a cursor object to interact with the database
cursor = db.cursor()

# Create a table to store account information if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        account_number INTEGER PRIMARY KEY,
        pin INTEGER,
        balance REAL
    )
""")

# Function to create a new account
def create_account(account_number, pin, balance=0.0):
    cursor.execute("INSERT INTO accounts (account_number, pin, balance) VALUES (?, ?, ?)",
                   (account_number, pin, balance))
    db.commit()

# Function to check balance
def check_balance(account_number):
    cursor.execute("SELECT balance FROM accounts WHERE account_number = ?", (account_number,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None

# Function to deposit money
def deposit(account_number, amount):
    current_balance = check_balance(account_number)
    if current_balance is not None:
        new_balance = current_balance + amount
        cursor.execute("UPDATE accounts SET balance = ? WHERE account_number = ?", (new_balance, account_number))
        db.commit()
        return new_balance
    else:
        return None

# Function to withdraw money
def withdraw(account_number, amount):
    current_balance = check_balance(account_number)
    if current_balance is not None and current_balance >= amount:
        new_balance = current_balance - amount
        cursor.execute("UPDATE accounts SET balance = ? WHERE account_number = ?", (new_balance, account_number))
        db.commit()
        return new_balance
    else:
        return None

# Main ATM simulation
def atm_simulator():
    print("Welcome to the ATM Simulator!")
    print("1. Create New Account")
    print("2. Login")
    
    choice = int(input("Enter your choice (1-2): "))

    if choice == 1:
        account_number = int(input("Enter a new account number: "))
        pin = int(input("Enter a PIN: "))
        create_account(account_number, pin)
        print("Account created successfully. Please login.")
        return

    elif choice == 2:
        account_number = int(input("Enter your account number: "))
        pin = int(input("Enter your PIN:"))

        # Check if account exists
        cursor.execute("SELECT * FROM accounts WHERE account_number = ? AND pin = ?", (account_number, pin))
        account_info = cursor.fetchone()

        if account_info:
            while True:
                print("\nATM Menu:")
                print("1. Check Balance")
                print("2. Deposit Money")
                print("3. Withdraw Money")
                print("4. Exit")

                choice = int(input("Enter your choice (1-4): "))

                if choice == 1:
                    balance = check_balance(account_number)
                    print(f"Current Balance: ${balance:.2f}")
                elif choice == 2:
                    amount = float(input("Enter the deposit amount: $"))
                    new_balance = deposit(account_number, amount)
                    if new_balance is not None:
                        print(f"Deposit successful. New Balance: ${new_balance:.2f}")
                    else:
                        print("Unable to process deposit.")
                elif choice == 3:
                    amount = float(input("Enter the withdrawal amount: $"))
                    new_balance = withdraw(account_number, amount)
                    if new_balance is not None:
                        print(f"Withdrawal successful. New Balance: ${new_balance:.2f}")
                    else:
                        print("Insufficient funds or unable to process withdrawal.")
                elif choice == 4:
                    print("Thank you for using the ATM Simulator. Goodbye!")
                    break
                else:
                    print("Invalid choice. Please enter a number between 1 and 4.")

        else:
            print("Invalid account number or PIN. Please try again.")

    else:
        print("Invalid choice. Please enter either 1 or 2.")

# Close database connection when the program exits
atm_simulator()
cursor.close()
db.close()
