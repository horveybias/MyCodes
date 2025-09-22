
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


if __name__ == "__main__":
    AddPaymentWindow()