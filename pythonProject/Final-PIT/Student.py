import pyodbc
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, ttk
from pathlib import Path
import tkinter as tk

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Horve\Documents\Code Projects\pythonProject\PIT code\build\assets\frame2")

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


student_window = Tk()
student_window.geometry("1282x779")
student_window.configure(bg = "#E5E5E5")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)
def create_payments_table():
    for item in payment_tree.get_children():
        payment_tree.delete(item)

    # Correct query for students table (not payments)
    query = """
    SELECT StudentID, LRN, StudentFullName, Gender, Course, Department, Create_at
    FROM students 
    ORDER BY Create_at DESC;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    
    # Insert data into Treeview
    for row in rows:
        try:
            # Proper date formatting for MSSQL
            date_str = row[6].strftime('%Y-%m-%d') if row[6] else ''
        except AttributeError:
            date_str = str(row[6]) if row[6] else ''
            
        formatted_row = (
            row[0],  # StudentID
            row[1],  # LRN
            row[2] if row[2] else '',  # StudentFullName
            row[3] if row[3] else '',  # Gender
            row[4] if row[4] else '',  # Course
            row[5] if row[5] else '',  # Department
            date_str  # Formatted date
        )
        payment_tree.insert("", tk.END, values=formatted_row)
def search_students():
    search_term = entry_1.get().strip()  # Get and trim whitespace
    
    # Clear the current tree view
    for item in payment_tree.get_children():
        payment_tree.delete(item)
    
    # If search term is empty, refresh with all students (or leave empty)
    if not search_term:
        # You might want to call a function here to refresh with all students
        # or just return without showing anything
        return create_payments_table()
    
    # Correct SQL query with LIKE and parameter
    query = """
    SELECT * FROM students
    WHERE StudentFullName LIKE ?;
    """ 
    
    search_param = f'%{search_term}%'  # Search for term anywhere in name
    cursor.execute(query, (search_param,))  # Note the comma to make it a tuple
    rows = cursor.fetchall()
    
    for row in rows:
        try:
            # Proper date formatting for MSSQL
            date_str = row[6].strftime('%Y-%m-%d') if row[6] else ''
        except AttributeError:
            date_str = str(row[6]) if row[6] else ''
            
        formatted_row = (
            row[0],  # StudentID
            row[1],  # LRN
            row[2] if row[2] else '',  # StudentFullName
            row[3] if row[3] else '',  # Gender
            row[4] if row[4] else '',  # Course
            row[5] if row[5] else '',  # Department
            date_str  # Formatted date
        )
        payment_tree.insert("", tk.END, values=formatted_row)

canvas = Canvas(
    student_window,
    bg = "#E5E5E5",
    height = 779,
    width = 1282,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    333.0,
    63.0,
    1235.0,
    779.0,
    fill="#FFFFFF",
    outline="")

canvas.create_text(
    359.0,
    84.0,
    anchor="nw",
    text="Student Enrolled",
    fill="#818181",
    font=("IBMPlexMono Regular", 24 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=38.0,
    y=63.0,
    width=261.0,
    height=41.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=38.0,
    y=126.0,
    width=261.0,
    height=41.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=38.0,
    y=189.0,
    width=261.0,
    height=41.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
button_4.place(
    x=38.0,
    y=252.0,
    width=261.0,
    height=41.0
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_5 clicked"),
    relief="flat"
)
button_5.place(
    x=38.0,
    y=315.0,
    width=261.0,
    height=41.0
)

canvas.create_rectangle(
    331.99560546875,
    134.98435974121094,
    1235.0044555664062,
    135.98435974121094,
    fill="#C0C0C0",
    outline="")

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    515.5,
    166.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=1,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0,
    font=("Arial", 12)
)
entry_1.place(
    x=411.0,
    y=147.0,
    width=209.0,
    height=36.0
)

canvas.create_rectangle(
    361.0,
    147.0,
    411.0,
    185.0,
    fill="#E6E4E4",
    outline="")

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    386.0,
    166.0,
    image=image_image_1
)

button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_6 clicked"),
    relief="flat"
)
button_6.place(
    x=1090.0,
    y=152.0,
    width=127.0,
    height=41.0
)

button_search = Button(
    borderwidth=1,
    highlightthickness=0,
    command=search_students,
    relief="flat",
    text="Search",
    font=('Arial', 12),
    bg="#1fb957"
)
button_search.place(
    x=620.5,
    y=146,
    width=127.0,
    height=35.0
)


table_frame = tk.Frame(student_window, bg="#FFFFFF")
table_frame.place(x=350, y=230, width=875, height=520)

# Change the Treeview columns to match student data
payment_tree = ttk.Treeview(
    table_frame,
    columns=("ID", "LRN", "Student Name", "Gender", "Course", "Department", "Date"),
    show='headings'
)

# Update column configuration
columns = {
    "ID": {"width": 50, "anchor": tk.CENTER},
    "LRN": {"width": 120, "anchor": tk.CENTER},
    "Student Name": {"width": 180, "anchor": tk.W},
    "Gender": {"width": 60, "anchor": tk.CENTER},
    "Course": {"width": 150, "anchor": tk.W},
    "Department": {"width": 150, "anchor": tk.CENTER},
    "Date": {"width": 120, "anchor": tk.CENTER}
}

for col, config in columns.items():
    payment_tree.heading(col, text=col)
    payment_tree.column(col, **config)

# Add scrollbars
vsb = ttk.Scrollbar(table_frame, orient="vertical", command=payment_tree.yview)
hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=payment_tree.xview)
payment_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

# Grid layout
payment_tree.grid(row=0, column=0, sticky="nsew")
vsb.grid(row=0, column=1, sticky="ns")
hsb.grid(row=1, column=0, sticky="ew")

# Configure grid weights
table_frame.grid_rowconfigure(0, weight=1)
table_frame.grid_columnconfigure(0, weight=1)

# Load initial data
create_payments_table()


student_window.resizable(False, False)
student_window.mainloop()
connection.close()
