from DBManager import DBManager
import warnings
from tkinter import *
from login import LogIn

warnings.filterwarnings('ignore')

root = Tk()
root.geometry("1000x600")
root.title("JOBINATOR")
icon = Image("photo", file=r"/home/aaditya/College/V/SE/project/Doofenshmirtz_Portrait.png")
root.tk.call('wm', 'iconphoto', str(root), icon)

########################################################################################################################
# THE LOG-IN SCREEN
# This is the screen where the user enters their credentials and then gets logged in
########################################################################################################################

loginScreen = LogIn(root)

root.mainloop()
