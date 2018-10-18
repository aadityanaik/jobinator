from tkinter import *
from tkinter.ttk import *
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
from DBManager import *


class Poster:
    def __init__(self, firstName, lastName, address, posterid):
        self.firstName = firstName
        self.lastName = lastName
        self.address = address
        self.posterid = posterid


class PosterHome:
    def __init__(self, user, rootWindow):
        self.user = user
        self.root = rootWindow

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_columnconfigure(3, weight=1)
        self.root.grid_rowconfigure(0, minsize=20)
        self.root.grid_rowconfigure(1, minsize=20)
        self.root.grid_rowconfigure(2, minsize=20)
        self.root.grid_rowconfigure(3, minsize=20)

        self.titleLabel = Label(rootWindow, text="Welcome, " + self.user.firstName)
        self.titleLabel.config(font=('Calibri', 30))
        self.titleLabel.grid(rowspan=2, columnspan=4, row=0)

        self.subtitleLabel = Label(rootWindow, text="POSTED JOBS")
        self.subtitleLabel.config(font=('Calibri', 20))
        self.subtitleLabel.grid(rowspan=1, columnspan=2, row=2, padx=2)

        self.postBtn = Button(rootWindow, text="POST A NEW JOB", command=self.postJob)
        # self.postBtn.config(font=('Calibri', 20))
        self.postBtn.grid(row=3, column=1, padx=2, sticky=E)

        Separator(rootWindow, orient=VERTICAL).grid(column=1, row=2, rowspan=10, sticky="nse")

        self.subtitleLabel = Label(rootWindow, text="PROFILE")
        self.subtitleLabel.config(font=('Calibri', 20))
        self.subtitleLabel.grid(column=2, columnspan=2, rowspan=2, row=2, ipadx=2)

        self.subtitleLabel = Label(rootWindow, text="NAME: " + self.user.firstName + " " + self.user.lastName)
        self.subtitleLabel.config(font=('Calibri', 15))
        self.subtitleLabel.grid(column=2, columnspan=2, rowspan=1, row=4, sticky=W, padx=2)

        self.subtitleLabel = Label(rootWindow, text="ADDRESS: " + self.user.address)
        self.subtitleLabel.config(font=('Calibri', 15))
        self.subtitleLabel.grid(column=2, columnspan=2, rowspan=2, row=5, sticky=W, padx=2)

        self.fillJobList()

    def fillJobList(self):
        manager = DBManager()
        listJobs = manager.run("SELECT JOBNAME, DESCRIPTION FROM JOBS WHERE POSTERID = %s", (self.user.posterid,))
        manager.close()
        filledRow = 4
        for job in listJobs:
            jobName = job[0]
            jobDesc = job[1]

            self.root.grid_rowconfigure(filledRow, minsize=20)
            self.root.grid_rowconfigure(filledRow + 1, minsize=20)

            jobNameLabel = Label(self.root, text=jobName, justify=LEFT)
            jobNameLabel.config(font=('Calibri', 15))
            jobNameLabel.grid(row=filledRow, sticky=W, padx=2)

            jobDescLabel = Label(self.root, text=jobDesc, justify=LEFT)
            jobDescLabel.config(font=('Calibri', 10))
            jobDescLabel.grid(row=filledRow + 1, sticky=W, padx=2, columnspan=2)

            filledRow = filledRow + 2

    def postJob(self):
        root = Toplevel()
        root.geometry("500x300")
        root.title("JOBINATOR")
        icon2 = Image("photo", file=r"/home/aaditya/College/V/SE/project/Doofenshmirtz_Portrait.png")
        root.tk.call('wm', 'iconphoto', str(root), icon2)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_rowconfigure(0, minsize=20)
        root.grid_rowconfigure(1, minsize=20)
        root.grid_rowconfigure(2, minsize=20)
        root.grid_rowconfigure(3, minsize=20)
        root.grid_rowconfigure(4, minsize=20)
        root.grid_rowconfigure(5, minsize=20)
        root.grid_rowconfigure(6, minsize=20)
        root.grid_rowconfigure(7, minsize=20)
        root.grid_rowconfigure(8, minsize=20)
        root.grid_rowconfigure(9, minsize=20)

        titleLabel = Label(root, text="Fill in the Details")
        titleLabel.config(font=("Calibri", 15))
        titleLabel.grid(row=0, column=0, rowspan=2, columnspan=2)

        jobTitleLabel = Label(root, text="Title: ")
        jobTitleLabel.grid(row=2, column=0, sticky=E)
        jobTitleText = Entry(root)
        jobTitleText.grid(row=2, column=1, sticky=W)

        jobDescLabel = Label(root, text="Description: ")
        jobDescLabel.grid(row=3, column=0, sticky=E)
        jobDescText = ScrolledText(root, height=4, width=50)
        jobDescText.grid(row=3, column=1, rowspan=2, sticky="nsew")

        postBtn = Button(root, text="POST", command=lambda: self.addJobInDatabase(root, jobTitleText.get(),
                                                                                  jobDescText.get('1.0', 'end-1c')))
        postBtn.grid(row=9, columnspan=2)

        root.mainloop()

    def addJobInDatabase(self, root, title, desc):
        db = DBManager()

        try:
            db.run("INSERT INTO JOBS(JOBNAME, DESCRIPTION, POSTERID) "
                   "VALUES(%s, %s, %s);", (title, desc, self.user.posterid))

            messagebox.showinfo("ALERT", "Job Posted")
            db.close()

            self.fillJobList()

            root.destroy()
        except Exception as e:
            print(e)
            db.close()
            messagebox.showerror("ERROR", e)
