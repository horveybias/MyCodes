import tkinter as tk
from tkinter import messagebox
import pyodbc

DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = 'LAPTOP-47J5CLF8\SQLEXPRESS'
DATABASE_NAME = 'billingdb'

connection_string = f"""
DRIVER={DRIVER_NAME};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};
Trust_Connection=yes;
"""
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

print("Database connected successfully!")

# Functions for login system
def add_account():
    username = username_entry.get()
    password = password_entry.get()

    if username and password:
        # Check if username already exists in the database
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()

        if result:
            messagebox.showerror("Account Error", "Username already exists.")
        else:
            # Insert new account into the 'users' table
            cursor.execute("INSERT INTO users (username, password, balance) VALUES (?, ?, ?)",
                           (username, password, 0.00))

            # Commit the changes to the database
            conn.commit()

            # Inform the user that the account has been created
            messagebox.showinfo("Success", "Account created successfully.")

            # Clear the entry fields
            username_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Input Error", "Please enter both username and password.")


def login():
    global current_user
    username = username_entry.get() 
    password = password_entry.get()

    if username and password:
        # Query the database for the entered username and password
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        result = cursor.fetchone()

        if result:
            current_user = username
            messagebox.showinfo("Login Success", f"Welcome, {username}!")
            show_billing_window()
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")
    else:
        messagebox.showerror("Input Error", "Please enter both username and password.")


def show_billing_window():
    login_frame.pack_forget()
    billing_frame.pack(fill='both', expand=True)

def calculate_bill():
    try:
        tuition = float(tuition_entry.get())
        misc = float(misc_entry.get())
        total = tuition + misc
        total_label.config(text=f"Total Bill: PHP {total:.2f}")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for fees.")

def clear_fields():
    tuition_entry.delete(0, tk.END)
    misc_entry.delete(0, tk.END)
    total_label.config(text="Total Bill: PHP 0.00")

def pay_bill():
    try:
        tuition = float(tuition_entry.get())
        misc = float(misc_entry.get())
        total = tuition + misc
        user_balances[current_user] += total
        messagebox.showinfo("Payment Successful", f"Payment of PHP {total:.2f} has been processed.")
        clear_fields()
    except ValueError:
        messagebox.showerror("Payment Error", "Please calculate the bill before paying.")

def check_balance():
    if current_user in user_balances:
        balance = user_balances[current_user]
        messagebox.showinfo("Tuition Balance", f"Current balance for {current_user}: PHP {balance:.2f}")
    else:
        messagebox.showerror("Balance Error", "User balance not found.")

# Create main window
root = tk.Tk()
root.title("Student Billing System")
root.geometry("300x400")

# Login Frame
login_frame = tk.Frame(root)
login_frame.pack(fill='both', expand=True)

tk.Label(login_frame, text="Username:").pack(pady=5)
username_entry = tk.Entry(login_frame)
username_entry.pack(pady=5)

tk.Label(login_frame, text="Password:").pack(pady=5)
password_entry = tk.Entry(login_frame, show='*')
password_entry.pack(pady=5)

tk.Button(login_frame, text="Login", command=login).pack(pady=5)
tk.Button(login_frame, text="Add Account", command=add_account).pack(pady=5)

# Billing Frame
billing_frame = tk.Frame(root)

# Labels and Entry Fields
tk.Label(billing_frame, text="Tuition Fee (PHP):").pack(pady=5)
tuition_entry = tk.Entry(billing_frame)
tuition_entry.pack(pady=5)

tk.Label(billing_frame, text="Miscellaneous Fee (PHP):").pack(pady=5)
misc_entry = tk.Entry(billing_frame)
misc_entry.pack(pady=5)

# Buttons
tk.Button(billing_frame, text="Calculate", command=calculate_bill).pack(pady=10)
tk.Button(billing_frame, text="Clear", command=clear_fields).pack(pady=5)
tk.Button(billing_frame, text="Pay Bill", command=pay_bill).pack(pady=5)
tk.Button(billing_frame, text="Check Balance", command=check_balance).pack(pady=5)

# Output Label
total_label = tk.Label(billing_frame, text="Total Bill: PHP 0.00", font=("Arial", 12, "bold"))
total_label.pack(pady=10)

# Run the main loop
root.mainloop()