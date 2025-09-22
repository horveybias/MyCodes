import pyodbc
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, ttk, messagebox, StringVar, Listbox, Label, SINGLE
import tkinter as tk
from datetime import datetime
from tkinter import ttk


# Database Configuration
DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = 'LAPTOP-47J5CLF8\SQLEXPRESS'
DATABASE_NAME = 'billingdb'

class AppState:
    """Class to hold application state"""
    def __init__(self):
        self.current_user = None
        self.connection = None
        self.cursor = None
        
    def connect_db(self):
        """Establish database connection"""
        connection_string = f"""
        DRIVER={DRIVER_NAME};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};
        Trust_Connection=yes;
        """
        try:
            self.connection = pyodbc.connect(connection_string)
            self.cursor = self.connection.cursor()
            print("Database connected successfully!")
            return True
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to connect to database: {str(e)}")
            return False

# Global application state
app_state = AppState()

class LoginWindow:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("926x578")
        self.window.configure(bg="#2D8CFF")
        self.window.title("Login")
        self.setup_ui()
        
        # Connect to database when window starts
        if not app_state.connect_db():
            self.window.destroy()
            return
            
        self.window.mainloop()
    
    def setup_ui(self):
        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Horve\Documents\Code Projects\pythonProject\PIT code\build\assets\frame2")

        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)

        canvas = Canvas(
            self.window,
            bg="#2D8CFF",
            height=578,
            width=926,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)
        
        # UI elements (same as your original code)
        canvas.create_rectangle(239.0, 17.0, 687.0, 561.0, fill="#FFFFFF", outline="")
        canvas.create_text(272.0, 152.0, anchor="nw", text="Username", fill="#000000", font=("IBMPlexMono Regular", 24 * -1))
        canvas.create_text(272.0, 36.0, anchor="nw", text="Log", fill="#000000", font=("IBMPlexMono Bold", 32 * -1))
        canvas.create_text(328.0, 36.0, anchor="nw", text="In", fill="#0161D6", font=("IBMPlexMono Bold", 32 * -1))
        canvas.create_text(272.0, 258.0, anchor="nw", text="Password", fill="#000000", font=("IBMPlexMono Regular", 24 * -1))

        # Entry fields
        entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
        entry_bg_1 = canvas.create_image(463.0, 208.5, image=entry_image_1)
        self.entry_username = Entry(
            bd=0,
            bg="#E1E1E1",
            fg="#000716",
            highlightthickness=0,
            font=("Arial", 12)
        )
        self.entry_username.place(x=277.0, y=188.0, width=372.0, height=39.0)

        entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
        entry_bg_2 = canvas.create_image(463.0, 314.5, image=entry_image_2)
        self.entry_password = Entry(
            bd=0,
            bg="#E1E1E1",
            fg="#000716",
            highlightthickness=0,
            font=("Arial", 12),
            show="*"  # Hide password characters
        )
        self.entry_password.place(x=277.0, y=294.0, width=372.0, height=39.0)

        # Login button
        button_1 = Button(
            borderwidth=1,
            highlightthickness=0,
            command=self.verify_login,
            relief="flat",
            text="Login",
            font=('Arial', 12),
            bg="red"
        )
        button_1.place(x=272.0, y=368.0, width=382.0, height=41.0)

        canvas.create_text(367.0, 444.0, anchor="nw", text="Forgot your password?", fill="#000000", font=("IBMPlexMono Regular", 16 * -1))
        self.window.resizable(False, False)
    
    def verify_login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if not username or not password:
            messagebox.showerror("Input Error", "Please enter both username and password.")
            return

        try:
            # Parameterized query to prevent SQL injection
            query = "SELECT * FROM students WHERE LRN = ? AND LRN = ?"
            app_state.cursor.execute(query, (username, password))
            result = app_state.cursor.fetchone()

            if result:
                app_state.current_user = username
                messagebox.showinfo("Login Success", f"Welcome, {username}!")
                self.window.destroy()
                DashboardWindow()  # Open dashboard after successful login
            else:
                messagebox.showerror("Login Failed", "Incorrect username or password.")
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {str(e)}")


class DashboardWindow:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("1282x779")
        self.window.configure(bg="#E5E5E5")
        self.window.title("Dashboard")
        self.setup_ui()
        self.window.mainloop()
        self.create_payments_table()
        self.load_payment_data()
    
    def setup_ui(self):
        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Horve\Documents\Code Projects\pythonProject\PIT code\build\assets\frame1")

        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)

        canvas = Canvas(
            self.window,
            bg="#E5E5E5",
            height=779,
            width=1282,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)
        
        # UI elements
        canvas.create_rectangle(333.0, 63.0, 1235.0, 779.0, fill="#FFFFFF", outline="")
        canvas.create_text(359.0, 390.0, anchor="nw", text="Recent Payments", fill="#000000", font=("IBMPlexMono Bold", 24 * -1))
        canvas.create_text(359.0, 84.0, anchor="nw", text=f"LRN: {app_state.current_user}", fill="#818181", font=("IBMPlexMono Regular", 24 * -1))

        # Navigation buttons (1-5) matching PaymentWindow style
        button_data = [
            {"text": "Dashboard", "y": 63.0, "bg": "red", "command": self.open_dashboard},
            {"text": "Payment", "y": 126.0, "bg": "#87CEFA", "command": self.open_payment_window},
            {"text": "Payment Records", "y": 189.0, "bg": "light blue", "command": self.open_payment_records},
            {"text": "Student", "y": 252.0, "bg": "green", "command": self.open_student},
            {"text": "Logout", "y": 315.0, "bg": "light green", "command": self.logout}
        ]

        for btn in button_data:
            button = Button(
                borderwidth=0,
                highlightthickness=0,
                command=btn["command"],
                relief="flat",
                text=btn["text"],
                font=('Arial', 12),
                bg=btn["bg"]
            )
            button.place(
                x=38.0, y=btn["y"],
                width=261.0, height=41.0
            )

        # Keep original buttons 6-8 unchanged
        button_images = [
            ("button_6.png", self.open_payment_window),
            ("button_7.png", self.open_payment_records),
            ("button_8.png", self.open_student)
        ]

        positions = [
            (349.0, 171.0),
            (647.0, 171.0),
            (945.0, 171.0)
        ]

        for i, (img, cmd) in enumerate(button_images):
            button_image = PhotoImage(file=relative_to_assets(img))
            button = Button(
                image=button_image,
                borderwidth=0,
                highlightthickness=0,
                command=cmd,
                relief="flat"
            )
            button.image = button_image
            button.place(
                x=positions[i][0],
                y=positions[i][1],
                width=272.0,
                height=95.0
            )

        canvas.create_rectangle(331.99560546875, 134.98435974121094, 1235.0044555664062, 135.98435974121094, fill="#C0C0C0", outline="")

        # Payment table
        table_frame = tk.Frame(self.window, bg="#FFFFFF")
        table_frame.place(x=350, y=430, width=875, height=300)

        self.payment_tree = ttk.Treeview(
            table_frame,
            columns=("ID", "LRN", "Student Name", "Course", "School Year", "Fees", "Balance", "Date"),
            show='headings'
        )

        columns = {
            "ID": {"width": 50, "anchor": tk.CENTER},
            "LRN": {"width": 120, "anchor": tk.CENTER},
            "Student Name": {"width": 120, "anchor": tk.W},
            "Course": {"width": 150, "anchor": tk.W},
            "School Year": {"width": 100, "anchor": tk.CENTER},
            "Fees": {"width": 120, "anchor": tk.W},
            "Balance": {"width": 100, "anchor": tk.E},
            "Date": {"width": 120, "anchor": tk.CENTER}
        }

        for col, config in columns.items():
            self.payment_tree.heading(col, text=col)
            self.payment_tree.column(col, **config)

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.payment_tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.payment_tree.xview)
        self.payment_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.payment_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        self.load_payment_data()
        self.window.resizable(False, False)

    def create_payments_table(self):
        """Create the payments table with scrollbars"""
        self.table_frame = tk.Frame(self.window, bg="#FFFFFF")
        self.table_frame.place(x=350, y=220, width=875, height=520)
        
        # Create Treeview widget
        self.payment_tree = ttk.Treeview(
            self.table_frame,
            columns=("ID", "LRN", "Student Name", "Course", "School Year", "Fees", "Balance", "Date"),
            show='headings'
        )
        
        # Configure columns
        columns = {
            "ID": {"width": 50, "anchor": tk.CENTER},
            "LRN": {"width": 120, "anchor": tk.CENTER},
            "Student Name": {"width": 120, "anchor": tk.W},
            "Course": {"width": 150, "anchor": tk.W},
            "School Year": {"width": 100, "anchor": tk.CENTER},
            "Fees": {"width": 120, "anchor": tk.W},
            "Balance": {"width": 100, "anchor": tk.E},
            "Date": {"width": 120, "anchor": tk.CENTER}
        }
        
        for col, config in columns.items():
            self.payment_tree.heading(col, text=col)
            self.payment_tree.column(col, **config)
        
        # Add scrollbars
        vsb = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.payment_tree.yview)
        hsb = ttk.Scrollbar(self.table_frame, orient="horizontal", command=self.payment_tree.xview)
        self.payment_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid layout
        self.payment_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        # Configure grid weights
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)

    def load_payment_data(self, search_term=None):
        for item in self.payment_tree.get_children():
            self.payment_tree.delete(item)

        try:
            if search_term:
                query = """
                SELECT PaymentId, LRN, StudentFullName, Course, SchoolYear, 
                    FeeDescription, Balance, Create_at
                FROM payment_records
                WHERE FeeDescription LIKE ?;
                """
                search_param = f'%{search_term}%'
                self.cursor.execute(query, (search_param,))

            else:
                query = """
                SELECT 
                    ID, LRN, StudentFullName, Course, SchoolYear, 
                    FeeDescription, Balance, Create_at
                FROM payment_records 
                WHERE LRN = ?
                ORDER BY Create_at DESC
                """
                app_state.cursor.execute(query, (app_state.current_user,))
                
            rows = app_state.cursor.fetchall()
            
            for row in rows:
                formatted_row = (
                    row[0],  # PaymentId
                    row[1],  # LRN
                    row[2] if row[2] else '',
                    row[3] if row[3] else '',
                    row[4] if row[4] else '',
                    row[5] if row[5] else '',
                    f"₱{row[6]:,.2f}" if row[6] is not None else '₱0.00',
                    row[7]
                )
                self.payment_tree.insert("", tk.END, values=formatted_row)
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load payment data: {str(e)}")

    
    def open_payment_window(self):
        self.window.destroy()
        PaymentWindow()
       
        # Navigation methods
    def open_dashboard(self):
        pass
        
    def open_payment_records(self):
        self.window.destroy()
        PaymentRecordsWindow()
        
    def open_student(self):
        self.window.destroy()
        StudentInformationSystem()  # Pass app_state
        
    def open_payment_options(self):
        self.window.destroy()
        # Create as a child window without destroying current window
        AddPaymentWindow()  # Use self.window as parent

    def logout(self):
        self.window.destroy()
        LoginWindow()


class PaymentWindow:
    def __init__(self):
        # Create main window
        self.window = Tk()
        self.window.geometry("1282x779")
        self.window.configure(bg="#E5E5E5")
        self.window.title("Payment Management")
        self.window.resizable(False, False)
        
        # Setup assets path
        self.OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = self.OUTPUT_PATH / Path(r"C:\Users\Horve\Documents\Code Projects\pythonProject\PIT code\build\assets\frame4")
        
        # Initialize UI
        self.setup_ui()
        self.window.mainloop()
    

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)
    
    def setup_ui(self):
        """Setup all UI components"""
        self.create_canvas()
        self.create_navigation_buttons()
        self.create_search_section()
        self.create_payments_table()
        self.load_payment_data()
    
    def create_canvas(self):
        """Create the main canvas and background elements"""
        self.canvas = Canvas(
            self.window,
            bg="#E5E5E5",
            height=779,
            width=1282,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        
        # Main white rectangle
        self.canvas.create_rectangle(
            333.0, 63.0, 1235.0, 779.0,
            fill="#FFFFFF", outline=""
        )
        
        # Title text
        self.canvas.create_text(
            359.0, 84.0,
            anchor="nw",
            text="Payment",
            fill="#818181",
            font=("IBMPlexMono Regular", 24 * -1)
        )
        
        # Divider line
        self.canvas.create_rectangle(
            331.99560546875, 134.984375,
            1235.0044555664062, 135.984375,
            fill="#C0C0C0", outline=""
        )
    
    def create_navigation_buttons(self):
        """Create all navigation buttons"""
        button_data = [
            {"text": "Dashboard", "y": 63.0, "bg": "red", "command": self.open_dashboard},
            {"text": "Payment", "y": 126.0, "bg": "#87CEFA", "command": self.open_payment},
            {"text": "Payment Records", "y": 189.0, "bg": "light blue", "command": self.open_payment_records},
            {"text": "Student", "y": 252.0, "bg": "green", "command": self.open_student},
            {"text": "Logout", "y": 315.0, "bg": "light green", "command": self.logout},
            {"text": "Add Payment", "x": 1066.0, "y": 152.0, "bg": "green", "command": self.open_payment_options}
        ]
        
        for btn in button_data:
            button = Button(
                borderwidth=0,
                highlightthickness=0,
                command=btn["command"],
                relief="flat",
                text=btn["text"],
                font=('Arial', 12),
                bg=btn["bg"]
            )
            # Use custom x position if specified, otherwise default to 38.0
            x_pos = btn.get("x", 38.0)
            button.place(
                x=x_pos, y=btn["y"],
                width=261.0 if x_pos == 38.0 else 151.0,
                height=41.0
            )
    
    def create_search_section(self):
        """Create the search box and button"""
        # Search entry background
        entry_img = PhotoImage(file=self.relative_to_assets("entry_1.png"))
        self.canvas.create_image(515.5, 166.0, image=entry_img)
        self.entry_img = entry_img  # Keep reference
        
        # Search entry field
        self.search_entry = Entry(
            bd=1,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("Arial", 12)
        )
        self.search_entry.place(
            x=411.0, y=147.0,
            width=209.0, height=36.0
        )
        
        # Search icon background
        self.canvas.create_rectangle(
            361.0, 147.0, 411.0, 185.0,
            fill="#E6E4E4", outline=""
        )
        
        # Search icon
        search_icon = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.canvas.create_image(386.0, 166.0, image=search_icon)
        self.search_icon = search_icon  # Keep reference
        
        # Search button
        self.search_button = Button(
            borderwidth=1,
            highlightthickness=0,
            command=self.search_payments,
            relief="flat",
            text="Search",
            font=('Arial', 12),
            bg="#1fb957"
        )
        self.search_button.place(
            x=620.5, y=146,
            width=127.0, height=35.0
        )
    
    def create_payments_table(self):
        """Create the payments table with scrollbars"""
        self.table_frame = tk.Frame(self.window, bg="#FFFFFF")
        self.table_frame.place(x=350, y=220, width=875, height=520)
        
        # Create Treeview widget
        self.payment_tree = ttk.Treeview(
            self.table_frame,
            columns=("ID", "LRN", "Student Name", "Course", "School Year", "Fees", "Balance", "Date"),
            show='headings'
        )
        
        # Configure columns
        columns = {
            "ID": {"width": 50, "anchor": tk.CENTER},
            "LRN": {"width": 120, "anchor": tk.CENTER},
            "Student Name": {"width": 120, "anchor": tk.W},
            "Course": {"width": 150, "anchor": tk.W},
            "School Year": {"width": 100, "anchor": tk.CENTER},
            "Fees": {"width": 120, "anchor": tk.W},
            "Balance": {"width": 100, "anchor": tk.E},
            "Date": {"width": 120, "anchor": tk.CENTER}
        }
        
        for col, config in columns.items():
            self.payment_tree.heading(col, text=col)
            self.payment_tree.column(col, **config)
        
        # Add scrollbars
        vsb = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.payment_tree.yview)
        hsb = ttk.Scrollbar(self.table_frame, orient="horizontal", command=self.payment_tree.xview)
        self.payment_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid layout
        self.payment_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        # Configure grid weights
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)

    def search_payments(self):
        """Handle search button click - search only by FeeDescription or SchoolYear for current student"""
        search_term = self.search_entry.get().strip()
        
        if not search_term:
            self.load_payment_data()
            return
        
        try:
            # Clear current data
            for item in self.payment_tree.get_children():
                self.payment_tree.delete(item)
            
            # Search query for FeeDescription or SchoolYear for current student only
            query = """
            SELECT ID, LRN, StudentFullName, Course, SchoolYear, 
                FeeDescription, Balance, Create_at
            FROM payment_records
            WHERE LRN = ? AND (FeeDescription LIKE ? OR SchoolYear LIKE ?);
            """
            search_param = f'%{search_term}%'
            app_state.cursor.execute(query, (app_state.current_user, search_param, search_param))
            
            rows = app_state.cursor.fetchall()
            
            for row in rows:
                formatted_row = (
                    row[0],  # PaymentId
                    row[1],  # LRN
                    row[2] if row[2] else '',
                    row[3] if row[3] else '',
                    row[4] if row[4] else '',
                    row[5] if row[5] else '',
                    f"₱{row[6]:,.2f}" if row[6] is not None else '₱0.00',
                    row[7]
                )
                self.payment_tree.insert("", tk.END, values=formatted_row)
                
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to search payment data: {str(e)}")

    # And update the load_payment_data method to match:

    def load_payment_data(self, search_term=None):
        """Load payment data with optional search by FeeDescription or SchoolYear for current student"""
        for item in self.payment_tree.get_children():
            self.payment_tree.delete(item)

        try:
            if search_term:
                query = """
                SELECT ID, LRN, StudentFullName, Course, SchoolYear, 
                    FeeDescription, Balance, Create_at
                FROM payment_records
                WHERE LRN = ? AND (FeeDescription LIKE ? OR SchoolYear LIKE ?);
                """
                search_param = f'%{search_term}%'
                app_state.cursor.execute(query, (app_state.current_user, search_param, search_param))
            else:
                query = """
                SELECT 
                    ID, LRN, StudentFullName, Course, SchoolYear, 
                    FeeDescription, Balance, Create_at
                FROM payment_records 
                WHERE LRN = ?
                """
                app_state.cursor.execute(query, (app_state.current_user,))
                
            rows = app_state.cursor.fetchall()
            
            for row in rows:
                formatted_row = (
                    row[0],  # PaymentId
                    row[1],  # LRN
                    row[2] if row[2] else '',
                    row[3] if row[3] else '',
                    row[4] if row[4] else '',
                    row[5] if row[5] else '',
                    f"₱{row[6]:,.2f}" if row[6] is not None else '₱0.00',
                    row[7]
                )
                self.payment_tree.insert("", tk.END, values=formatted_row)
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load payment data: {str(e)}")
    
    
    def search_payments(self):
        """Handle search button click"""
        search_term = self.search_entry.get().strip()
        self.load_payment_data(search_term if search_term else None)
    
    # Navigation methods
    def open_dashboard(self):
        self.window.destroy()
        DashboardWindow()
    
    def open_payment(self):
        self.window.destroy()
        PaymentWindow()
        
    def open_payment_records(self):
        self.window.destroy()
        PaymentRecordsWindow()
        
    def open_student(self):
        self.window.destroy()
        StudentInformationSystem()  # Pass app_state
        
    def open_payment_options(self):
        self.window.destroy()
        # Create as a child window without destroying current window
        AddPaymentWindow()  # Use self.window as parent
        
    def logout(self):
        self.window.destroy()
        LoginWindow()


class PaymentRecordsWindow:
    def __init__(self):
        # Create main window
        self.window = Tk()
        self.window.geometry("1282x779")
        self.window.configure(bg="#E5E5E5")
        self.window.title("Payment Records")
        self.window.resizable(False, False)
        
        # Setup assets path
        self.OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = self.OUTPUT_PATH / Path(r"C:\Users\Horve\Documents\Code Projects\pythonProject\PIT code\build\assets\frame3")
        
        # Initialize UI
        self.setup_ui()
        self.window.mainloop()
    
    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)
    
    def setup_ui(self):
        """Setup all UI components"""
        self.create_canvas()
        self.create_navigation_buttons()
        self.create_search_section()
        self.create_payments_table()
        self.load_payment_data()
    
    def create_canvas(self):
        """Create the main canvas and background elements"""
        self.canvas = Canvas(
            self.window,
            bg="#E5E5E5",
            height=779,
            width=1282,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        
        # Main white rectangle
        self.canvas.create_rectangle(
            333.0, 63.0, 1235.0, 779.0,
            fill="#FFFFFF", outline=""
        )
        
        # Title text
        self.canvas.create_text(
            359.0, 84.0,
            anchor="nw",
            text="Payment Records",
            fill="#818181",
            font=("IBMPlexMono Regular", 24 * -1)
        )
        
        # Divider line
        self.canvas.create_rectangle(
            331.99560546875, 134.984375,
            1235.0044555664062, 135.984375,
            fill="#C0C0C0", outline=""
        )
    
    def create_navigation_buttons(self):
        """Create all navigation buttons"""
        button_data = [
            {"text": "Dashboard", "y": 63.0, "bg": "red", "command": self.open_dashboard},
            {"text": "Payment", "y": 126.0, "bg": "#87CEFA", "command": self.open_payment},
            {"text": "Payment Records", "y": 189.0, "bg": "light blue", "command": self.open_payment_records},
            {"text": "Student", "y": 252.0, "bg": "green", "command": self.open_student},
            {"text": "Logout", "y": 315.0, "bg": "light green", "command": self.logout}
        ]
        
        for btn in button_data:
            button = Button(
                borderwidth=0,
                highlightthickness=0,
                command=btn["command"],
                relief="flat",
                text=btn["text"],
                font=('Arial', 12),
                bg=btn["bg"]
            )
            button.place(
                x=38.0, y=btn["y"],
                width=261.0, height=41.0
            )
    
    def create_search_section(self):
        """Create the search box and button"""
        # Search entry background
        entry_img = PhotoImage(file=self.relative_to_assets("entry_1.png"))
        self.canvas.create_image(515.5, 166.0, image=entry_img)
        self.entry_img = entry_img  # Keep reference
        
        # Search entry field
        self.search_entry = Entry(
            bd=1,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("Arial", 12)
        )
        self.search_entry.place(
            x=411.0, y=147.0,
            width=209.0, height=36.0
        )
        
        # Search icon background
        self.canvas.create_rectangle(
            361.0, 147.0, 411.0, 185.0,
            fill="#E6E4E4", outline=""
        )
        
        # Search icon
        search_icon = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.canvas.create_image(386.0, 166.0, image=search_icon)
        self.search_icon = search_icon  # Keep reference
        
        # Search button
        self.search_button = Button(
            borderwidth=1,
            highlightthickness=0,
            command=self.search_payments,
            relief="flat",
            text="Search",
            font=('Arial', 12),
            bg="#1fb957"
        )
        self.search_button.place(
            x=620.5, y=146,
            width=127.0, height=35.0
        )
    
    def create_payments_table(self):
        """Create the payments table with scrollbars"""
        self.table_frame = tk.Frame(self.window, bg="#FFFFFF")
        self.table_frame.place(x=350, y=220, width=875, height=520)
        
        # Create Treeview widget
        self.payment_tree = ttk.Treeview(
            self.table_frame,
            columns=("ID", "LRN", "Student Name", "Course", "School Year", "Fees", "Balance", "Date"),
            show='headings'
        )
        
        # Configure columns
        columns = {
            "ID": {"width": 50, "anchor": tk.CENTER},
            "LRN": {"width": 120, "anchor": tk.CENTER},
            "Student Name": {"width": 120, "anchor": tk.W},
            "Course": {"width": 150, "anchor": tk.W},
            "School Year": {"width": 100, "anchor": tk.CENTER},
            "Fees": {"width": 120, "anchor": tk.W},
            "Balance": {"width": 100, "anchor": tk.E},
            "Date": {"width": 120, "anchor": tk.CENTER}
        }
        
        for col, config in columns.items():
            self.payment_tree.heading(col, text=col)
            self.payment_tree.column(col, **config)
        
        # Add scrollbars
        vsb = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.payment_tree.yview)
        hsb = ttk.Scrollbar(self.table_frame, orient="horizontal", command=self.payment_tree.xview)
        self.payment_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid layout
        self.payment_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        # Configure grid weights
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)
    
    def search_payments(self):
        """Handle search button click - search only by FeeDescription or SchoolYear for current student"""
        search_term = self.search_entry.get().strip()
        
        if not search_term:
            self.load_payment_data()
            return
        
        try:
            # Clear current data
            for item in self.payment_tree.get_children():
                self.payment_tree.delete(item)
            
            # Search query for FeeDescription or SchoolYear for current student only
            query = """
            SELECT ID, LRN, StudentFullName, Course, SchoolYear, 
                FeeDescription, Balance, Create_at
            FROM payment_records
            WHERE LRN = ? AND (FeeDescription LIKE ? OR SchoolYear LIKE ?);
            """
            search_param = f'%{search_term}%'
            app_state.cursor.execute(query, (app_state.current_user, search_param, search_param))
            
            rows = app_state.cursor.fetchall()
            
            for row in rows:
                formatted_row = (
                    row[0],  # PaymentId
                    row[1],  # LRN
                    row[2] if row[2] else '',
                    row[3] if row[3] else '',
                    row[4] if row[4] else '',
                    row[5] if row[5] else '',
                    f"₱{row[6]:,.2f}" if row[6] is not None else '₱0.00',
                    row[7]
                )
                self.payment_tree.insert("", tk.END, values=formatted_row)
                
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to search payment data: {str(e)}")

    def load_payment_data(self, search_term=None):
        """Load payment data with optional search by FeeDescription or SchoolYear for current student"""
        for item in self.payment_tree.get_children():
            self.payment_tree.delete(item)

        try:
            if search_term:
                query = """
                SELECT ID, LRN, StudentFullName, Course, SchoolYear, 
                    FeeDescription, Balance, Create_at
                FROM payment_records
                WHERE LRN = ? AND (FeeDescription LIKE ? OR SchoolYear LIKE ?);
                """
                search_param = f'%{search_term}%'
                app_state.cursor.execute(query, (app_state.current_user, search_param, search_param))
            else:
                query = """
                SELECT 
                    ID, LRN, StudentFullName, Course, SchoolYear, 
                    FeeDescription, Balance, Create_at
                FROM payment_records 
                WHERE LRN = ?
                """
                app_state.cursor.execute(query, (app_state.current_user,))
                
            rows = app_state.cursor.fetchall()
            
            for row in rows:
                formatted_row = (
                    row[0],  # PaymentId
                    row[1],  # LRN
                    row[2] if row[2] else '',
                    row[3] if row[3] else '',
                    row[4] if row[4] else '',
                    row[5] if row[5] else '',
                    f"₱{row[6]:,.2f}" if row[6] is not None else '₱0.00',
                    row[7]
                )
                self.payment_tree.insert("", tk.END, values=formatted_row)
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load payment data: {str(e)}")
    
    
    def search_payments(self):
        search_term = self.search_entry.get().strip()
        self.load_payment_data(search_term if search_term else None)
    
    # Navigation methods
    def open_dashboard(self):
        self.window.destroy()
        DashboardWindow()
    
    def open_payment(self):
        self.window.destroy()
        PaymentWindow()
    
    def open_payment_records(self):
        pass
    
    def open_student(self):
        self.window.destroy()
        StudentInformationSystem()
    
    def logout(self):
        self.window.destroy()
        LoginWindow()
   

from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox, StringVar, Listbox, Label, SINGLE, END, Toplevel, Text, Scrollbar
from tkinter import ttk
from pathlib import Path
from reportlab.pdfgen import canvas
import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

class AddPaymentWindow:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("713x684")
        self.window.configure(bg="#FFFFFF")
        self.window.title("Payment")

        # Connect to database
        self.connection = app_state.connection
        self.cursor = app_state.cursor

        self.current_balance = 0.0
        self.current_fee_amount = 0.0

        self.setup_ui()
        self.load_student_data()
        self.load_static_fees()

        self.window.resizable(False, False)
        self.window.mainloop()

    def relative_to_assets(self, path: str) -> Path:
        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Horve\Documents\Code Projects\pythonProject\PIT code\build\assets\frame0")
        return ASSETS_PATH / Path(path)

    def setup_ui(self):
        self.create_canvas()
        self.create_title()
        self.create_student_info_section()
        self.create_payment_form()
        self.create_buttons()

    def create_canvas(self):
        self.canvas = Canvas(
            self.window,
            bg="#FFFFFF",
            height=684,
            width=713,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

    def create_title(self):
        self.canvas.create_text(
            137.0,
            20.0,
            anchor="nw",
            text="Payment",
            fill="#000000",
            font=("IBMPlexMono Regular", 32 * -1)
        )
        self.image_image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.canvas.create_image(112.0, 38.0, image=self.image_image_1)

    def create_student_info_section(self):
        self.canvas.create_text(50.0, 100.0, anchor="nw", text="Student Information:", fill="#000000", font=("IBMPlexMono Bold", 16 * -1))

        self.lrn_label = Label(self.window, text="LRN: ", font=("Arial", 12), bg="#FFFFFF")
        self.lrn_label.place(x=50, y=130)

        self.name_label = Label(self.window, text="Name: ", font=("Arial", 12), bg="#FFFFFF")
        self.name_label.place(x=50, y=160)

        self.course_label = Label(self.window, text="Course: ", font=("Arial", 12), bg="#FFFFFF")
        self.course_label.place(x=50, y=190)

        self.balance_label = Label(self.window, text="Current Balance: ", font=("Arial", 12), bg="#FFFFFF")
        self.balance_label.place(x=50, y=220)

    def create_payment_form(self):
        self.canvas.create_text(50.0, 270.0, anchor="nw", text="School Year:", fill="#000000", font=("Arial", 12))
        self.school_year_entry = Entry(self.window, bd=1, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Arial", 12))
        self.school_year_entry.place(x=200, y=270, width=200, height=25)

        self.canvas.create_text(50.0, 310.0, anchor="nw", text="Fees:", fill="#000000", font=("Arial", 12))
        self.fees_listbox = ttk.Combobox(self.window, font=("Arial", 12), state="readonly")
        self.fees_listbox.place(x=200, y=310, width=200)
        self.fees_listbox.bind("<<ComboboxSelected>>", self.update_fee_balance)

        self.canvas.create_text(50.0, 410.0, anchor="nw", text="Selected Fee:", fill="#000000", font=("Arial", 12))
        self.selected_fee_label = Label(self.window, text="", font=("Arial", 12), bg="#FFFFFF")
        self.selected_fee_label.place(x=200, y=410)

        self.canvas.create_text(50.0, 450.0, anchor="nw", text="Fee Amount:", fill="#000000", font=("Arial", 12))
        self.fee_amount_label = Label(self.window, text="₱0.00", font=("Arial", 12), bg="#FFFFFF")
        self.fee_amount_label.place(x=200, y=450)

        self.canvas.create_text(50.0, 490.0, anchor="nw", text="Amount Paid:", fill="#000000", font=("Arial", 12))
        self.amount_entry = Entry(self.window, bd=1, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Arial", 12))
        self.amount_entry.place(x=200, y=490, width=200, height=25)
        self.amount_entry.bind("<KeyRelease>", self.update_remaining_balance)

        self.canvas.create_text(50.0, 520.0, anchor="nw", text="Remaining Balance:", fill="#000000", font=("Arial", 12))
        self.remaining_balance_var = StringVar(value="₱0.00")
        self.remaining_balance_label = Label(self.window, textvariable=self.remaining_balance_var, font=("Arial", 12), bg="#FFFFFF")
        self.remaining_balance_label.place(x=200, y=520)

        self.canvas.create_text(50.0, 550.0, anchor="nw", text="Date:", fill="#000000", font=("Arial", 12))
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.date_label = Label(self.window, text=current_date, font=("Arial", 12), bg="#FFFFFF")
        self.date_label.place(x=200, y=550)

    def create_buttons(self):
        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_1 = Button(image=self.button_image_1, borderwidth=0, highlightthickness=0, command=self.submit_payment, relief="flat")
        self.button_1.place(x=589.0, y=610.0, width=87.0, height=41.0)

        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_2.png"))
        self.button_2 = Button(image=self.button_image_2, borderwidth=0, highlightthickness=0, command=self.go_back, relief="flat")
        self.button_2.place(x=10.0, y=23.0, width=50.0, height=30.0)

    def load_student_data(self):
        try:
            query = "SELECT LRN, StudentFullName, Course, Balance FROM students WHERE LRN = ?"
            self.cursor.execute(query, (app_state.current_user,))
            student = self.cursor.fetchone()
            if student:
                self.lrn_label.config(text=f"LRN: {student[0]}")
                self.name_label.config(text=f"Name: {student[1]}")
                self.course_label.config(text=f"Course: {student[2]}")
                self.current_balance = float(student[3] or 0)
                self.balance_label.config(text=f"Current Balance: ₱{self.current_balance:.2f}")
            else:
                messagebox.showerror("Error", "Student not found!")
                self.window.destroy()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load student data: {str(e)}")
            self.window.destroy()

    def load_static_fees(self):
        """Load predefined fees into listbox"""
        self.static_fees = {
            "Tuition": self.current_balance,
            "Book and Supplies": 3000.00,
            "Laboratory and Equipments": 5000.00,
            "Uniform": 1000.00,
            "PE Uniform": 700.00
        }
        self.fees_listbox['values'] = list(self.static_fees.keys())

    def update_fee_balance(self, event=None):
        selected_fee = self.fees_listbox.get()
        if selected_fee:
            self.selected_fee_label.config(text=selected_fee)
            self.current_fee_amount = self.static_fees[selected_fee]
            self.fee_amount_label.config(text=f"₱{self.current_fee_amount:.2f}")
            self.remaining_balance_var.set(f"₱{self.current_fee_amount:.2f}")
            self.amount_entry.delete(0, END)

    def update_remaining_balance(self, event=None):
        try:
            paid = float(self.amount_entry.get() or 0)
            remaining = self.current_fee_amount - paid
            self.remaining_balance_var.set(f"₱{remaining:.2f}")
        except ValueError:
            self.remaining_balance_var.set("Invalid amount")

    def submit_payment(self):
        try:
            # Get student info
            lrn = app_state.current_user
            name = self.name_label.cget("text").replace("Name: ", "")
            course = self.course_label.cget("text").replace("Course: ", "")

            # Get user input
            school_year = self.school_year_entry.get().strip()
            selected_fee = self.selected_fee_label.cget("text")
            fee_amount = float(self.fee_amount_label.cget("text").replace("₱", "").replace(",", ""))
            amount_paid = float(self.amount_entry.get())
            remaining_balance = float(self.remaining_balance_var.get().replace("₱", "").replace(",", ""))
            payment_date = self.date_label.cget("text")

            # Validate inputs
            if not school_year:
                raise ValueError("Please enter a valid School Year.")
            if not selected_fee:
                raise ValueError("Please select a fee.")

            # 🔁 Only deduct from student balance if the fee is 'Tuition'
            if selected_fee == "Tuition":
                # Calculate new balance (ensure it doesn't go below 0)
                new_balance = max(0, self.current_balance - amount_paid)

                # Update student balance in students table
                update_query = "UPDATE students SET Balance = ? WHERE LRN = ?"
                self.cursor.execute(update_query, (new_balance, lrn))

            # Insert into payment records
            insert_query = """
            INSERT INTO payment_records 
            (LRN, StudentFullName, Course, SchoolYear, FeeDescription, Fees, AmountPaid, Balance, Create_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            self.cursor.execute(insert_query, (
                lrn, name, course, school_year,
                selected_fee, fee_amount, amount_paid, remaining_balance,
                payment_date
            ))

            # Commit transaction
            self.connection.commit()

            # Show receipt and save it
            self.generate_receipt(lrn, name, course, school_year, selected_fee, fee_amount, amount_paid, remaining_balance, payment_date)

            messagebox.showinfo("Success", "Payment recorded successfully!")
            self.go_back()

        except ValueError as ve:
            messagebox.showerror("Input Error", f"Invalid input: {str(ve)}")
            self.connection.rollback()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to save payment: {str(e)}")
            self.connection.rollback()

    def generate_receipt(self, lrn, name, course, school_year, fee_desc, fee_amount, amount_paid, balance, date):
        """Generate and display receipt with logo, then save to PDF"""
        receipt_window = Toplevel(self.window)
        receipt_window.title("Payment Receipt")
        receipt_window.geometry("600x650")

        # Create Text widget for receipt
        receipt_text = Text(receipt_window, font=("Courier", 12))
        receipt_text.pack(fill="both", expand=True, padx=10, pady=10)

        # Load and insert logo image
        try:
            self.logo_path = self.relative_to_assets("ustplogo.png")  # Make sure this path is correct
            self.logo_image = PhotoImage(file=self.logo_path)  # Keep reference to prevent garbage collection
            receipt_text.image_create("end", image=self.logo_image)
            receipt_text.insert("end", "\n")  # Line break after image
        except Exception as e:
            messagebox.showwarning("Image Error", f"Could not load logo: {str(e)}")

        # Receipt content
        content = f"""

            {'=' * 40}
                    SCHOOL PAYMENT RECEIPT
            {'=' * 40}
            .
            Date: {date}
            Receipt No: {int(datetime.datetime.now().timestamp())}
            STUDENT INFORMATION:
            LRN: {lrn}
            Name: {name}
            Course: {course}
            School Year: {school_year}
            .
            .
            PAYMENT DETAILS:
            Fee Description: {fee_desc}
            Fee Amount: PHP {fee_amount:,.2f}
            Amount Paid: PHP {amount_paid:,.2f}
            Remaining Balance: PHP {balance:,.2f}
            .
            {'=' * 40}
                    Thank you for your payment!
            {'=' * 40}
            """

        # Insert text content below the image
        receipt_text.insert("end", content)
        receipt_text.config(state="disabled")  # Make read-only

        # Buttons for saving and closing
        button_frame = tk.Frame(receipt_window)
        button_frame.pack(pady=10)

        save_button = tk.Button(button_frame, text="Print Receipt", width=12,
                            command=lambda: self.save_receipt_to_pdf(receipt_text))
        save_button.pack(side="left", padx=5)

        close_button = tk.Button(button_frame, text="Close", width=12,
                                command=receipt_window.destroy)
        close_button.pack(side="left", padx=5)

    def save_receipt_to_pdf(self, receipt_widget):
        """Save receipt content including logo to a PDF file"""
        try:
            content = receipt_widget.get("1.0", "end-1c")
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"receipt_{timestamp}.pdf"

            # Create PDF document
            doc = SimpleDocTemplate(filename)
            styles = getSampleStyleSheet()
            style_normal = styles['Normal']
            elements = []

            # Add logo
            try:
                pdf_logo = Image(self.logo_path)
                pdf_logo.drawHeight = 1 * inch
                pdf_logo.drawWidth = 5 * inch
                elements.append(pdf_logo)
            except Exception as img_error:
                messagebox.showwarning("PDF Image Error", f"Could not embed logo in PDF: {str(img_error)}")

            # Add text content line by line
            lines = content.split('\n')
            for line in lines:
                if line.strip():
                    para = Paragraph(line, style_normal)
                    elements.append(para)
                    elements.append(Spacer(1, 6))

            # Build PDF
            doc.build(elements)

            messagebox.showinfo("Saved", f"Receipt saved as:\n{filename}")
        except Exception as e:
            messagebox.showerror("File Error", f"Could not save receipt: {str(e)}")

    def go_back(self):
        self.window.destroy()
        PaymentWindow()


class StudentInformationSystem:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("1282x779")
        self.window.configure(bg="#E5E5E5")
        self.window.title("Student Information System")
        self.window.resizable(False, False)

        self.connection = app_state.connection
        self.cursor = app_state.cursor

        self.setup_ui()
        self.load_student_data()
        self.window.mainloop()

    def setup_ui(self):
        self.create_canvas()
        self.create_navigation_buttons()
        self.create_student_display()

    def create_canvas(self):
        self.canvas = Canvas(
            self.window,
            bg="#E5E5E5",
            height=779,
            width=1282,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        
        self.canvas.create_rectangle(333.0, 63.0, 1235.0, 779.0, fill="#FFFFFF", outline="")
        self.canvas.create_text(359.0, 84.0, anchor="nw", text="Student Information", 
                              fill="#818181", font=("IBMPlexMono Regular", 24 * -1))
        self.canvas.create_rectangle(331.99560546875, 134.984375, 1235.0044555664062, 135.984375,
                                   fill="#C0C0C0", outline="")

    def create_navigation_buttons(self):
        button_data = [
            {"text": "Dashboard", "y": 63.0, "bg": "red", "command": self.open_dashboard},
            {"text": "Payment", "y": 126.0, "bg": "#87CEFA", "command": self.open_payment},
            {"text": "Payment Records", "y": 189.0, "bg": "light blue", "command": self.open_payment_records},
            {"text": "Student", "y": 252.0, "bg": "green", "command": self.open_student},
            {"text": "Logout", "y": 315.0, "bg": "light green", "command": self.logout}
        ]
        
        for btn in button_data:
            Button(
                borderwidth=0,
                highlightthickness=0,
                command=btn["command"],
                relief="flat",
                text=btn["text"],
                font=('Arial', 12),
                bg=btn["bg"]
            ).place(x=38.0, y=btn["y"], width=261.0, height=41.0)

    def create_student_display(self):
        self.student_frame = tk.Frame(self.window, bg="#FFFFFF")
        self.student_frame.place(x=350, y=180, width=875, height=520)

        fields = ["LRN:", "Name:", "Gender:", "Course:", "Department:", "Date Created:"]
        
        for i, field in enumerate(fields):
            Label(
                self.student_frame,
                text=field,
                font=("Calibri", 12, "bold"),
                bg="#FFFFFF",
                anchor="e"
            ).grid(row=i, column=0, padx=10, pady=10, sticky="e")

        self.data_labels = []
        for i in range(6):
            label = Label(self.student_frame, bg="#FFFFFF", anchor="w")
            label.grid(row=i, column=1, padx=10, pady=10, sticky="w")
            self.data_labels.append(label)

    def load_student_data(self):
        try:
            query = """
            SELECT LRN, StudentFullName, Gender, Course, Department, Create_at
            FROM students
            WHERE LRN = ?
            """
            self.cursor.execute(query, (app_state.current_user,))
            student = self.cursor.fetchone()

            if student:
                # Format date properly whether it's string or datetime
                date_value = student[5]
                if date_value:
                    if hasattr(date_value, 'strftime'):  
                        formatted_date = date_value.strftime('%Y-%m-%d')
                    else:  
                        formatted_date = str(date_value).split()[0]  
                else:
                    formatted_date = 'N/A'

                # Update all labels
                data_values = [
                    student[0] or 'N/A',  # LRN
                    student[1] or 'N/A',  # Name
                    student[2] or 'N/A',  # Gender
                    student[3] or 'N/A',  # Course
                    student[4] or 'N/A',  # Department
                    formatted_date       # Date
                ]
                
                for label, value in zip(self.data_labels, data_values):
                    label.config(text=value)
            else:
                messagebox.showerror("Error", "Student not found!")
                self.window.destroy()

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load student data: {str(e)}")
            self.window.destroy()

    # Navigation methods
    def open_dashboard(self):
        self.window.destroy()
        DashboardWindow()
    
    def open_payment(self):
        self.window.destroy()
        PaymentWindow()
    
    def open_payment_records(self):
        self.window.destroy()
        PaymentRecordsWindow()
    
    def open_student(self):
        pass
    
    def logout(self):
        self.window.destroy()
        LoginWindow()


if __name__ == "__main__":
    LoginWindow()