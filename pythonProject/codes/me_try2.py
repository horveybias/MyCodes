from tkinter import*

def buttonClick(number):
    current = myentry.get()
    myentry.delete(0, END)
    myentry.insert(0, str(current) + str(number))

def buttonClear():
    myentry.delete(0, END)

def sum():
    first_num = myentry.get()
    global f_num
    global math
    f_num = int(first_num)
    math = "Addition"
    myentry.delete(0, END)

def sub():
    first_num = myentry.get()
    global f_num
    global math
    f_num = int(first_num)
    math = "Subtraction"
    myentry.delete(0, END)

def mul():
    first_num = myentry.get()
    global f_num
    global math
    f_num = int(first_num)
    math = "Multiplication"
    myentry.delete(0, END)

def div():
    first_num = myentry.get()
    global f_num
    global math
    f_num = int(first_num)
    math = "Division"
    myentry.delete(0, END)

def buttonEqual():
    second_num = myentry.get()
    myentry.delete(0, END)

    if math == "Addition":
        myentry.insert(0, f_num + int(second_num))
    elif math == "Subtraction":
        myentry.insert(0, f_num - int(second_num))
    elif math == "Multiplication":
        myentry.insert(0, f_num * int(second_num))
    elif math == "Division":
        myentry.insert(0, f_num / int(second_num))


root = Tk()
root.title("Simple Calculator by horve ybias")

myentry = Entry(root, width=35, borderwidth=5)
myentry.grid(row=0, column=0, columnspan=4)



button_1 = Button(root, text=9, padx=40, pady=20, command=lambda: buttonClick(9))
button_2 = Button(root, text=8, padx=40, pady=20, command=lambda: buttonClick(8))
button_3 = Button(root, text=7, padx=40, pady=20, command=lambda: buttonClick(7))
button_4 = Button(root, text=4, padx=40, pady=20, command=lambda: buttonClick(4))
button_5 = Button(root, text=5, padx=40, pady=20, command=lambda: buttonClick(5))
button_6 = Button(root, text=6, padx=40, pady=20, command=lambda: buttonClick(6))
button_7 = Button(root, text=1, padx=40, pady=20, command=lambda: buttonClick(1))
button_8 = Button(root, text=2, padx=40, pady=20, command=lambda: buttonClick(2))
button_9 = Button(root, text=3, padx=40, pady=20, command=lambda: buttonClick(3))
button_10 = Button(root, text="clear", padx=30, pady=20, command=buttonClear)
button_11 = Button(root, text=0, padx=40, pady=20, command=lambda: buttonClick(0))
button_12 = Button(root, text="=", padx=40, pady=20, command=buttonEqual)

button_13 = Button(root, text="+", padx=40, pady=20, command=sum)
button_14 = Button(root, text="-", padx=40, pady=20, command=sub)
button_15 = Button(root, text="x", padx=40, pady=20, command=mul)
button_16 = Button(root, text="/", padx=40, pady=20, command=div)




button_1.grid(row=1, column=2)
button_2.grid(row=1, column=1)
button_3.grid(row=1, column=0)
button_4.grid(row=2, column=0)
button_5.grid(row=2, column=1)
button_6.grid(row=2, column=2)
button_7.grid(row=3, column=2)
button_8.grid(row=3, column=1)
button_9.grid(row=3, column=0)
button_10.grid(row=4, column=0)
button_11.grid(row=4, column=1)
button_12.grid(row=4, column=2)

button_13.grid(row=1, column=3)
button_14.grid(row=2, column=3)
button_15.grid(row=3, column=3)
button_16.grid(row=4, column=3)

root.mainloop()