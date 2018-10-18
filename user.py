from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from DBManager import *


class User:
    def __init__(self, firstName, lastName, address, username):
        self.firstName = firstName
        self.lastName = lastName
        self.address = address
        self.username = username


class UserHome:
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

        self.subtitleLabel = Label(rootWindow, text="AVAILABLE JOBS")
        self.subtitleLabel.config(font=('Calibri', 20))
        self.subtitleLabel.grid(rowspan=2, columnspan=2, row=2, padx=2)

        Separator(rootWindow, orient=VERTICAL).grid(column=1, row=2, rowspan=10, sticky="nse")

        self.subtitleLabel = Label(rootWindow, text="PROFILE")
        self.subtitleLabel.config(font=('Calibri', 20))
        self.subtitleLabel.grid(column=2, columnspan=2, rowspan=2, row=2, padx=2)

        self.subtitleLabel = Label(rootWindow, text="NAME: " + self.user.firstName + " " + self.user.lastName)
        self.subtitleLabel.config(font=('Calibri', 15))
        self.subtitleLabel.grid(column=2, columnspan=2, rowspan=1, row=4, sticky=W, padx=2)

        self.subtitleLabel = Label(rootWindow, text="ADDRESS: " + self.user.address)
        self.subtitleLabel.config(font=('Calibri', 15))
        self.subtitleLabel.grid(column=2, columnspan=2, rowspan=2, row=5, sticky=W, padx=2)

        manager = DBManager()
        listJobs = manager.run("SELECT * FROM JOBS")
        manager.close()

        filledRow = 4
        listLabels = []
        for index in range(len(listJobs)):
            jobid = listJobs[index][0]
            jobName = listJobs[index][1]
            jobDesc = listJobs[index][2]

            self.root.grid_rowconfigure(filledRow, minsize=20)
            self.root.grid_rowconfigure(filledRow + 1, minsize=20)

            jobNameLabel = Label(rootWindow, text=jobName, justify=LEFT)
            jobNameLabel.config(font=('Calibri', 15))
            jobNameLabel.grid(row=filledRow, sticky=W, padx=2)

            jobApplyBtn = Button(rootWindow, text="APPLY", command=lambda jid=jobid, name=jobName: self.applyJob(jid, name))
            jobApplyBtn.grid(row=filledRow, column=1, sticky=E, padx=2)

            jobDescLabel = Label(rootWindow, text=jobDesc, justify=LEFT)
            jobDescLabel.config(font=('Calibri', 10))
            jobDescLabel.grid(row=filledRow + 1, sticky=W, padx=2, columnspan=2)

            listLabels.append([jobNameLabel, jobDescLabel, jobApplyBtn])

            filledRow = filledRow + 2

    def applyJob(self, jobid, jobname):
        result = messagebox.askquestion("Applying for job: " + jobname, "Your resume will be shared to the poster. Apply?")

        if result == 'yes':
            db = DBManager()
            try:
                userInfo = db.run("SELECT * FROM APPLICANT WHERE USERNAME = %s;", (self.user.username, ))
                db.run("INSERT INTO APPLICATIONS VALUES(%s, %s, %s, %s, %s, %s);",
                       (int(jobid), userInfo[0][2], userInfo[0][0], userInfo[0][1], userInfo[0][3], userInfo[0][4], ))
                db.close()
                messagebox.showinfo("APPLIED", "Your application has been sent.")

            except Exception as e:
                print(e)
                db.close()
                messagebox.showerror("ERROR", e)
