import pyodbc
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from tkinter import messagebox

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Horve\Documents\Code Projects\pythonProject\PIT code\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = 'LAPTOP-47J5CLF8\SQLEXPRESS'
DATABASE_NAME = 'billingdb'

connection_string = f"""
DRIVER={DRIVER_NAME};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};
Trust_Connection=yes;
"""

connection = pyodbc.connect(connection_string)
cursor = connection.cursor()
print("Database connected successfully!")


Login_window = Tk()
Login_window.geometry("926x578")
Login_window.configure(bg = "#2D8CFF")

# def Functions
def Click_login():
    username = entry_1.get()
    password = entry_2.get()

    if username and password:
        # Query the database for the entered username and password
        query = f"""
        SELECT * FROM students WHERE LRN = ? AND LRN = ?
        """
        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        if result:
            messagebox.showinfo("Login Success", f"Welcome, {username}!")
            # Redirect to the dashboard or another page after successful login
            Login_window.destroy() 
            import Dashboard

        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")
    else:
        messagebox.showerror("Input Error", "Please enter both username and password.")

    


canvas = Canvas(
    Login_window,
    bg = "#2D8CFF",
    height = 578,
    width = 926,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    239.0,
    17.0,
    687.0,
    561.0,
    fill="#FFFFFF",
    outline="")

canvas.create_text(
    272.0,
    152.0,
    anchor="nw",
    text="Username",
    fill="#000000",
    font=("IBMPlexMono Regular", 24 * -1)
)

canvas.create_text(
    272.0,
    36.0,
    anchor="nw",
    text="Log",
    fill="#000000",
    font=("IBMPlexMono Bold", 32 * -1)
)

canvas.create_text(
    328.0,
    36.0,
    anchor="nw",
    text="In",
    fill="#0161D6",
    font=("IBMPlexMono Bold", 32 * -1)
)

canvas.create_text(
    272.0,
    258.0,
    anchor="nw",
    text="Password",
    fill="#000000",
    font=("IBMPlexMono Regular", 24 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    463.0,
    208.5,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#E1E1E1",
    fg="#000716",
    highlightthickness=0,
    font=("Arial", 12)
)
entry_1.place(
    x=277.0,
    y=188.0,
    width=372.0,
    height=39.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    463.0,
    314.5,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#E1E1E1",
    fg="#000716",
    highlightthickness=0,
    font=("Arial", 12)
)
entry_2.place(
    x=277.0,
    y=294.0,
    width=372.0,
    height=39.0
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=Click_login,
    relief="flat"
)
button_1.place(
    x=272.0,
    y=368.0,
    width=382.0,
    height=41.0
)

canvas.create_text(
    367.0,
    444.0,
    anchor="nw",
    text="Forgot your password?",
    fill="#000000",
    font=("IBMPlexMono Regular", 16 * -1)
)
Login_window.resizable(False, False)
Login_window.mainloop()


