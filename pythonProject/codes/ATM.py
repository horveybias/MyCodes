from tkinter import*
from tkinter import messagebox


def Withdraw():
    global balance
    amount = float(Enter_withdraw.get())
    try:
        if amount > 0:
            balance-=amount
            messagebox.showinfo("Withdraw", f"${amount:.2f} is successfully withdraw! ")
        else:
            messagebox.showwarning("Withdraw", "Please enter a valid amount!")
    except ValueError:
        messagebox.showwarning("Withdraw", "Please enter a valid amount!")
    Enter_withdraw.delete(0, END)

def Diposit():
    global balance
    amount = float(Enter_Deposit.get())
    try:
        if amount > 0:
            balance+=amount
            messagebox.showinfo("Deposit", f"${amount:.2f} is successfully deposit!")
        else:
            messagebox.showwarning("Deposit", "Please enter a valid amount!")
    except ValueError:
        messagebox.showwarning("Deposit", "Please enter a valid amount!")
    Enter_Deposit.delete(0, END)

def check_balance():
    messagebox.showinfo("Check Balance", f"Your current balance is: ${balance:.2f}")

def Activate_withdraw():
    Enter_withdraw.config(state=NORMAL)

def Activate_deposite():
    Enter_Deposit.config(state=NORMAL)

def Deactivate_Both():
    Enter_withdraw.config(state=DISABLED)
    Enter_Deposit.config(state=DISABLED)


root = Tk()
root.title("ATM")
root.geometry("450x200")

balance = 1000.0

lbl_wel = Label(root, text="Welcome to ATM", font=("Arial",17))
lbl_wel.grid(row=0, column=0, columnspan=3)

lbl_withdraw = Label(root, text="Withdraw", font=("Arial", 11))
lbl_withdraw.grid(row=1, column=0)

lbl_deposit = Label(root, text="Deposit", font=("Arial", 11))
lbl_deposit.grid(row=2, column=0)

Enter_withdraw = Entry(root, width=35, state=DISABLED)
Enter_withdraw.grid(row=1, column=1)

Enter_Deposit = Entry(root, width=35, state=DISABLED)
Enter_Deposit.grid(row=2, column=1)

Bttn_Activate_Withdraw = Button(root, text="Activate", padx=10, command=Activate_withdraw)
Bttn_Activate_Withdraw.grid(row=1, column=2, pady=10)

Bttn_Activate_Deposit = Button(root, text="Activate", padx=10, command=Activate_deposite)
Bttn_Activate_Deposit.grid(row=2, column=2, pady=10)

Bttn_Withdraw = Button(root, text="Withdraw", padx=10, command=Withdraw)
Bttn_Withdraw.grid(row=1, column=3, pady=10)

Bttn_Deposit = Button(root, text="Deposit",padx=16, command=Diposit)
Bttn_Deposit.grid(row=2, column=3, pady=10)

Bttn_CheckBalance = Button(root, text="Check Balance", padx=40, command=check_balance)
Bttn_CheckBalance.grid(row=3, column=0, columnspan=3, pady=10)

Bttn_Deactivate_Withdraw_Deposit = Button(root, text="Deactivate", padx=20, command=Deactivate_Both)
Bttn_Deactivate_Withdraw_Deposit.grid(row=3, column=2, columnspan=2, pady=10)


root.mainloop()
