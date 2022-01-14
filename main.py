from ntpath import join
from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

# Password Generator Project


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
               'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():

    website = website_entry.get().lower()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {website: {
        "email": email,
        "password": password,
    }}

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(
            title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        try:
            with open("data.json", "r") as data_file:
                # reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            # if try fails json file will be created and data written
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # updating old data with new_data
            data.update(new_data)

            with open("data.json", "w") as data_file:
                # saving updated data / create data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- FIND PASSWORD ------------------------------- #

def find_password():
    website = website_entry.get().lower()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(
            title="Error", message="No data file found. \nTry to save some passwors first.")
        return
    else:
        print(data)
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(
                title=website, message=f"Email / user: {email}\nPassword: {password}\n\nPassword copied to clipboard!")
            pyperclip.copy(password)
            website_entry.delete(0, END)
        else:
            messagebox.showinfo(
                title="Oops", message=f"No password saved for '{website_entry.get()}'")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
website_label.config(pady=15)
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
# email_label.config(pady=5)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)
password_label.config(pady=15)

# Entries
website_entry = Entry(width=35)
website_entry.grid(row=1, column=1, sticky="EW")
website_entry.focus()
email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2, sticky="EW")
email_entry.insert(0, "zaharia.ioan@gmail.com")
password_entry = Entry(width=21)
password_entry.grid(row=3, column=1, sticky="EW")

# Buttons
search_button = Button(text="Search", command=find_password)
search_button.grid(row=1, column=2, sticky="EW")
generate_password_button = Button(
    text="Generate Password", command=generate_password)
generate_password_button.grid(row=3, column=2, sticky="EW")
add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2, sticky="EW")

window.mainloop()
