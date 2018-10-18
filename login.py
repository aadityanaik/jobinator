from tkinter import *
from tkinter import messagebox
from DBManager import *
from user import User, UserHome
from poster import Poster, PosterHome


class LogIn:
    def __init__(self, master):
        self.root = master
        self.usernameLabel = Label(master, text="Username")
        self.passwordLabel = Label(master, text="Password")

        self.usernameEntry = Entry(master)
        self.passwordEntry = Entry(master, show="*")

        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)
        master.grid_rowconfigure(0, minsize=20)
        master.grid_rowconfigure(1, minsize=20)
        master.grid_rowconfigure(2, minsize=50)
        master.grid_rowconfigure(3, minsize=20)
        master.grid_rowconfigure(4, minsize=20)
        master.grid_rowconfigure(5, minsize=20)

        self.titleLabel = Label(master, text="Enter Your Credentials")
        self.titleLabel.config(font=("Calibri", 20))
        self.titleLabel.grid(row=0, columnspan=2)

        self.subTitleLabel = Label(master, text="If You Are A New User, Register")
        self.subTitleLabel.grid(row=1, columnspan=2)

        self.usernameLabel.grid(row=3, sticky=E)
        self.passwordLabel.grid(row=4, sticky=E)
        self.usernameEntry.grid(row=3, column=1, sticky=W)
        self.passwordEntry.grid(row=4, column=1, sticky=W)

        self.buttonFrame = Frame(master)

        self.loginBtn = Button(self.buttonFrame, text="Log In", command=self.login)
        self.registerBtn = Button(self.buttonFrame, text="Register", command=self.register)

        self.loginBtn.pack(side=LEFT)
        self.registerBtn.pack(side=LEFT)

        self.buttonFrame.grid(row=6, columnspan=2)
    
    def login(self):
        enteredUsername = self.usernameEntry.get()
        enteredPassword = self.passwordEntry.get()

        if enteredUsername == "" or enteredPassword == "":
            messagebox.showerror("ERROR", "Fill all of the information")
        else:
            db = DBManager()

            try:
                outputUserPass = db.run("SELECT * FROM USERPASS WHERE USERNAME = %s;", (enteredUsername, ))
                registeredPassword = outputUserPass[0][1]
                isPoster = (outputUserPass[0][2] == 1)

                if enteredPassword == registeredPassword:
                    if not isPoster:
                        outputUserDetails = db.run("SELECT FNAME, SNAME, ADDRESS FROM APPLICANT WHERE USERNAME = %s", (enteredUsername, ))
                        self.forget_widgets()
                        UserHome(User(outputUserDetails[0][0], outputUserDetails[0][1], outputUserDetails[0][2], enteredUsername),
                                 self.root)
                    else:
                        outputUserDetails = db.run("SELECT FNAME, SNAME, ADDRESS FROM POSTER WHERE USERNAME = %s", (enteredUsername, ))
                        self.forget_widgets()
                        PosterHome(Poster(outputUserDetails[0][0], outputUserDetails[0][1], outputUserDetails[0][2], enteredUsername),
                                   self.root)


                else:
                    print("HERE")
                    messagebox.showerror("ERROR", "Incorrect username or password")

                db.close()

            except Exception as e:
                print(e)
                db.close()
                messagebox.showerror("ERROR", "Incorrect username or password")

    def register(self):
        root = Toplevel()
        root.geometry("1000x600")
        root.title("JOBINATOR")
        icon2 = Image("photo", file=r"/home/aaditya/College/V/SE/project/Doofenshmirtz_Portrait.png")
        root.tk.call('wm', 'iconphoto', str(root), icon2)
        Register(root)
        root.mainloop()

    def forget_widgets(self):
        self.titleLabel.grid_forget()
        self.subTitleLabel.grid_forget()
        self.passwordEntry.grid_forget()
        self.passwordLabel.grid_forget()
        self.usernameLabel.grid_forget()
        self.usernameEntry.grid_forget()
        self.buttonFrame.grid_forget()


class Register:
    def __init__(self, master):
        self.root = master
        self.firstNameLabel = Label(master, text="First Name")
        self.secondNameLabel = Label(master, text="Second Name")
        self.usernameLabel = Label(master, text="Username")
        self.passwordLabel = Label(master, text="Password")
        self.addressLabel = Label(master, text="Address")
        self.accountTypeLabel = Label(master, text="I am a(n)")
        self.additionalLabel = Label(master, text="Path to Resume")

        self.accountType = StringVar(master)
        self.accountType.set("Applicant")

        self.firstNameEntry = Entry(master)
        self.secondNameEntry = Entry(master)
        self.addressEntry = Entry(master)
        self.usernameEntry = Entry(master)
        self.passwordEntry = Entry(master, show="*")
        self.accountTypeList = OptionMenu(master, self.accountType, "Applicant", "Poster",
                                          command=self.changeAdditionalLabel)
        self.additionalEntry = Entry(master)

        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)
        master.grid_rowconfigure(0, minsize=20)
        master.grid_rowconfigure(1, minsize=50)
        master.grid_rowconfigure(2, minsize=20)
        master.grid_rowconfigure(3, minsize=20)
        master.grid_rowconfigure(4, minsize=20)
        master.grid_rowconfigure(5, minsize=20)
        master.grid_rowconfigure(9, minsize=20)

        self.titleLabel = Label(master, text="Enter Your Details")
        self.titleLabel.config(font=("Calibri", 20))
        self.titleLabel.grid(row=0, columnspan=2)

        self.firstNameLabel.grid(row=2, sticky=E)
        self.secondNameLabel.grid(row=3, sticky=E)
        self.addressLabel.grid(row=4, sticky=E)
        self.usernameLabel.grid(row=5, sticky=E)
        self.passwordLabel.grid(row=6, sticky=E)
        self.accountTypeLabel.grid(row=7, sticky=E)
        self.additionalLabel.grid(row=8, sticky=E)

        self.firstNameEntry.grid(row=2, column=1, sticky=W)
        self.secondNameEntry.grid(row=3, column=1, sticky=W)
        self.addressEntry.grid(row=4, column=1, sticky=W)
        self.usernameEntry.grid(row=5, column=1, sticky=W)
        self.passwordEntry.grid(row=6, column=1, sticky=W)
        self.accountTypeList.grid(row=7, column=1, sticky=W)
        self.additionalEntry.grid(row=8, column=1, sticky=W)

        self.regBtn = Button(master, text="Register", command=self.register)

        self.regBtn.grid(row=10, columnspan=2)

    def changeAdditionalLabel(self, value):
        if value == "Applicant":
            self.additionalLabel.config(text="Path to Resume")
        else:
            self.additionalLabel.config(text="Company Name")

    def register(self):
        firstName = self.firstNameEntry.get()
        secondName = self.secondNameEntry.get()
        address = self.addressEntry.get()
        username = self.usernameEntry.get()[:50]
        password = self.passwordEntry.get()

        if firstName == "" or secondName == "" or address == "" or username == "" or password == "":
            messagebox.showerror("ERROR", "Fill all of the information")
        else:
            if self.accountType.get() == "Applicant":
                pathToResume = self.additionalEntry.get()

                if pathToResume == "":
                    messagebox.showerror("ERROR", "Fill all of the information")
                else:
                    with open(pathToResume, mode='rb') as file:
                        content = file.read()

                    db = DBManager()
                    try:

                        db.run("INSERT INTO USERPASS VALUES("
                               "\"" + username + "\", "
                               "\"" + password + "\", "
                               "FALSE);")
                        db.run("INSERT INTO APPLICANT VALUES("
                               "\"" + firstName + "\", "
                               "\"" + secondName + "\", "
                               "\"" + username + "\", "
                               "\"" + address + "\", "
                               "%s );", (content, )
                               )

                        messagebox.showinfo("ATTENTION", "You have been registered", parent=self.root)
                        self.root.destroy()
                    except Exception as e:
                        messagebox.showerror("ERROR", e, parent=self.root)

                    db.close()

            else:
                company = self.additionalEntry.get()

                if company == "":
                    messagebox.showerror("ERROR", "Fill all of the information")
                else:
                    db = DBManager()
                    try:

                        db.run("INSERT INTO USERPASS VALUES("
                               "\"" + username + "\", "
                               "\"" + password + "\", "
                               "TRUE);")
                        db.run("INSERT INTO POSTER VALUES("
                               "\"" + firstName + "\", "
                               "\"" + secondName + "\", "
                               "\"" + username + "\", "
                               "\"" + address + "\", "
                               "\"" + company + "\");"
                               )

                        messagebox.showinfo("ATTENTION", "You have been registered", parent=self.root)
                        self.root.destroy()
                    except Exception as e:
                        messagebox.showerror("ERROR", e, parent=self.root)

                    db.close()
