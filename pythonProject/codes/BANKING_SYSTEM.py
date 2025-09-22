from tkinter import*

# mian screen
root = Tk()
root.title("BANKING SYSTEM")

all_accounts = []
# Functions
def finish_register():
    global all_accounts

    name = temp_name.get()
    address = temp_address.get()
    phoneNumber = temp_phoneNumber.get()
    PIN = temp_pin.get()
    balance = int(temp_accountBalance.get())

    if name == "" or address == "" or phoneNumber == "" or PIN == "":
        notif.config(fg="red", text="All fields are required!")
        return

    try:
        for account_exist in all_accounts:
            if account_exist["name"] != name:
                if account_exist["PIN"] != PIN:
                    continue
                else:
                    notif.config(fg="red", text="password is already used!")
                    return
            else:
                notif.config(fg="red", text="Account already exists!")
                return
    except ValueError:
        notif.config(fg="red", text="password is already used!")
        return

    new_account = {"name": name, "address": address, "phoneNumber": phoneNumber, "PIN": PIN, "balance": balance}
    all_accounts.append(new_account)
    print(new_account)
    register_screen.destroy()

def register():
    global temp_name
    global temp_address
    global temp_phoneNumber
    global temp_pin
    global temp_accountBalance
    global notif
    global register_screen

    temp_name = StringVar()
    temp_address = StringVar()
    temp_phoneNumber = StringVar()
    temp_pin =StringVar()
    temp_accountBalance = IntVar()

    register_screen = Toplevel(root)
    register_screen.title("Register")

    # Label
    Label(register_screen, text="Pls enter your details below to register", font=("Arial", 11)).grid(row=0, sticky=N, pady=10)
    Label(register_screen, text="Name: ", font=("Arial", 11)).grid(row=1, stick=W)
    Label(register_screen, text="Address: ", font=("Arial", 11)).grid(row=2, stick=W)
    Label(register_screen, text="Phone Number: ", font=("Arial", 11)).grid(row=3, stick=W)
    Label(register_screen, text="Account Number: ", font=("Arial", 11)).grid(row=4, stick=W)
    Label(register_screen, text="Account Balance: ", font=("Arial", 11)).grid(row=5, stick=W)
    notif = Label(register_screen, font=("Arial", 11))
    notif.grid(row=8, sticky=N, pady=5)

    # Entry
    Entry(register_screen, textvariable=temp_name).grid(row=1, sticky=E)
    Entry(register_screen, textvariable=temp_address).grid(row=2, sticky=E)
    Entry(register_screen, textvariable=temp_phoneNumber).grid(row=3, sticky=E)
    Entry(register_screen, textvariable=temp_pin).grid(row=4, sticky=E)
    Entry(register_screen, textvariable=temp_accountBalance).grid(row=5, sticky=E)

    # Button
    Button(register_screen, text="Register", font=("Arial", 11), command=finish_register, bg="green").grid(row=6, sticky=E, padx=30)

def LogIn_session():
    global Entryname
    global EntryPIN

    Entryname = temp_username.get()
    EntryPIN = temp_password.get()

    if Entryname == "" or EntryPIN == "":
        notif.config(fg="red", text="All fields are required!")
        return

    for account_exist in all_accounts:
        if account_exist["name"] == Entryname:
            if account_exist["PIN"] == EntryPIN:
                notif.config(fg="green", text="Successfully logged in")
                account_screenDisplay = Toplevel(root)
                account_screenDisplay.title("Account Display")

                # Labels
                Label(account_screenDisplay, text="Account Dashboard").grid(row=0, sticky=N, pady=10)
                Label(account_screenDisplay, text=f"Hello! {account_exist['name']}").grid(row=1, sticky=N, pady=10)

                # Buttons
                Button(account_screenDisplay, text="Personal Details", padx=20, command=personal_Detail, bg="green").grid(row=2, sticky=W, pady=2)
                Button(account_screenDisplay, text="Withdraw", padx=35, command=withdraw, bg="skyblue").grid(row=3, sticky=N, pady=2)
                Button(account_screenDisplay, text="Deposit", padx=40, command=deposit, bg="pink").grid(row=4, sticky=N, pady=2)
                Login_screen.destroy()
                return
            else:
                notif.config(fg="red", text="Invalid password\n pass is your Account number.")
                return
    notif.config(fg="red", text="Your account does not exist\nPlease try again")

def personal_Detail():

    personal_screen = Toplevel(root)
    personal_screen.title("Personal Details")

    for account_exist in all_accounts:
        if account_exist["name"] == Entryname and account_exist["PIN"] == EntryPIN:
            # Label
            Label(personal_screen, text="Account Dashboard\t\t\t\t").grid(row=0, sticky=N)
            Label(personal_screen, text="Account Name:\t\t" + account_exist["name"], font=("Arial", 11)).grid(row=1, sticky=W)
            Label(personal_screen, text="Account address:\t\t" + account_exist["address"], font=("Arial", 11)).grid(row=2, sticky=W)
            Label(personal_screen, text="Phone Number:\t\t" + account_exist["phoneNumber"], font=("Arial", 11)).grid(row=3, sticky=W)
            Label(personal_screen, text="Account Number:\t\t" + account_exist["PIN"], font=("Arial", 11)).grid(row=4, sticky=W)
            Label(personal_screen, text="Account Balance:", font=("Arial", 11)).grid(row=5, sticky=W)
            Label(personal_screen, text= account_exist["balance"]).grid(row=5, sticky=N)
            return

def withdraw():
    global option
    global amount_withdraw
    global withdraw_screen
    global notif_withdraw
    amount_withdraw = IntVar()

    withdraw_screen = Toplevel(root)
    withdraw_screen.title("Withdraw")
    # Label
    Label(withdraw_screen, text="Account Withdraw\t\t\t", font=("Arial", 11)).grid(row=0, column=0, columnspan=1)
    Label(withdraw_screen, text="Amount: ", font=("Arial", 11)).grid(row=1, sticky=W)
    notif_withdraw = Label(withdraw_screen, font=("Arial", 11))
    notif_withdraw.grid(row=4, sticky=N, pady=5)
    # Entry
    Entry(withdraw_screen, textvariable=amount_withdraw).grid(row=1, sticky=E)
    # Buttton
    Button(withdraw_screen, text="Withdraw", font=("Arial", 11), padx=30, command=finish_withdraw, bg="green").grid(row=2, sticky=N, pady=2)
    Button(withdraw_screen, text="Check Balance", font=("Arial", 11), padx=10, command=check_balance, bg="skyblue").grid(row=3, sticky=N, pady=2)
    option = "withdraw_check_balance"

def finish_withdraw():
    amount = float(amount_withdraw.get())

    for account_detail in all_accounts:
        if account_detail["name"] == Entryname and account_detail["PIN"] == EntryPIN:
            if account_detail["balance"] < amount:
                notif_withdraw.config(fg="red", text="Insufficient funds")
                return
            elif amount <= 0:
                notif_withdraw.config(fg="red", text="amount must greater than to 0")
                return
            else:
                account_detail["balance"] -= amount
                print("successfully withdraw")
                notif_withdraw.config(fg="green", text="successfully withdraw!")
                return

def deposit():
    global option
    global amount_deposit
    global deposit_screen
    global notif_deposit
    amount_deposit = IntVar()

    deposit_screen = Toplevel(root)
    deposit_screen.title("Deposit")
    # Label
    Label(deposit_screen, text="Account Deposit \t\t\t\t", font=("Arial", 11)).grid(row=0, column=0, columnspan=1)
    Label(deposit_screen, text="Amount: ", font=("Arial", 11)).grid(row=1, sticky=W)
    notif_deposit = Label(deposit_screen, font=("Arial", 11))
    notif_deposit.grid(row=4, sticky=N, pady=5)
    # Entry
    Entry(deposit_screen, textvariable=amount_deposit).grid(row=1, sticky=E)
    # Buttton
    Button(deposit_screen, text="Deposit", font=("Arial", 11), padx=30, command=finish_deposit, bg="green").grid(row=2, sticky=N,pady=2)
    Button(deposit_screen, text="Check Balance", font=("Arial", 11), padx=10, command=check_balance, bg="skyblue").grid(row=3,sticky=N,pady=2)
    option = "deposit_check_balance"

def finish_deposit():
    amount = float(amount_deposit.get())

    for account_detail in all_accounts:
        if account_detail["name"] == Entryname and account_detail["PIN"] == EntryPIN:
            if amount <= 0:
                notif_deposit.config(fg="red", text="amount must greater than to 0")
                return
            else:
                account_detail["balance"] += amount
                print("successfully Deposit")
                notif_deposit.config(fg="green", text="successfully deposit!")
                return

def check_balance():
    global current_balance

    if option == "deposit_check_balance":
        for account_detail in all_accounts:
            notif = Label(deposit_screen, font=("Arial", 11))
            notif.grid(row=5, sticky=N, pady=5)

            if account_detail["name"] == Entryname and account_detail["PIN"] == EntryPIN:
                notif.config(fg="green", text=f"your current balance is balance: {account_detail["balance"]:.2f}")
                current_balance = account_detail["balance"]
                return

    if option == "withdraw_check_balance":
        for account_detail in all_accounts:
            notif = Label(withdraw_screen, font=("Arial", 11))
            notif.grid(row=5, sticky=N, pady=5)

            if account_detail["name"] == Entryname and account_detail["PIN"] == EntryPIN:
                notif.config(fg="green", text=f"your current balance is balance: {account_detail["balance"]:.2f}")
                current_balance = account_detail["balance"]
                return

def LogIn():
    global temp_username
    global temp_password
    global notif
    global Login_screen

    temp_username = StringVar()
    temp_password = StringVar()

    Login_screen = Toplevel(root)
    Login_screen.title("Log In")

    # Label
    Label(Login_screen, text="Log in to your account", font=("Arial", 11)).grid(row=0, sticky=W, pady=10)
    Label(Login_screen, text="Username:", font=("Arial", 11)).grid(row=1, sticky=W)
    Label(Login_screen, text="password:", font=("Arial", 11)).grid(row=2, sticky=W)
    notif = Label(Login_screen, font=("Arial", 11))
    notif.grid(row=4, column=0, columnspan=2,pady=5)

    # Entry
    Entry(Login_screen, textvariable=temp_username).grid(row=1, column=1)
    Entry(Login_screen, textvariable=temp_password, show="*").grid(row=2, column=1)

    # Button
    Button(Login_screen, text="Log In", font=("Arial", 11), command=LogIn_session, bg="green").grid(row=3, column=1)

def Exite_button():
    root.destroy()

# Label and Button
mylbl = Label(root, text="Welcome to Banking system", font=("Arial", 16), padx=15)
mylbl.grid(row=0, column=0, pady=10)

mybttn_register_account = Button(root, text="Register Account", font=("Arial", 11), padx=22, command=register, bg="green")
mybttn_register_account.grid(row=1, column=0, pady=2)

mybttn_LogIn_account = Button(root, text="Log In Account", font=("Arial", 11), padx=30, command=LogIn, bg="skyblue")
mybttn_LogIn_account.grid(row=2, column=0, pady=2)

mybttm_Exit = Button(root, text="Exit Program", font=("Arial", 11), padx=35, command=Exite_button, bg="red")
mybttm_Exit.grid(row=3, column=0, pady=2)

root.mainloop()