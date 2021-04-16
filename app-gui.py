from Detector import main_app
from create_classifier import train_classifer
from create_dataset import start_capture
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox,PhotoImage
from PIL import ImageTk, Image
#from gender_prediction import emotion,ageAndgender
names = set()


class MainUI(tk.Tk):#begin reading users list and load their information

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        global names
        with open("nameslist.txt", "r") as f:
            x = f.read()
            z = x.rstrip().split(" ")
            for i in z:
                names.add(i)
        #launch main menu
        self.title_font = tkfont.Font(family='Helvetica', size=16, weight="bold")
        self.title("Facial Recognition Safety Camera")
        self.resizable(False, False)
        self.geometry("500x250")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.active_name = None
        container = tk.Frame(self)
        container.grid(sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")

    def show_frame(self, page_name):
            frame = self.frames[page_name]
            frame.tkraise()

    def on_closing(self):
#message prompted when user closes menu/save user status
        if messagebox.askokcancel("Quit?", "Are you sure you want to quit?"):
            global names
            f =  open("nameslist.txt", "a+")
            for i in names:
                    f.write(i+" ")
            self.destroy()


class StartPage(tk.Frame):

        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.controller = controller
            #load menu images for home menu
            render = PhotoImage(file='baby_lope.png')
            img = tk.Label(self, image=render)
            img.image = render
            img.grid(row=0, column=1, rowspan=4, sticky="nsew")
            label = tk.Label(self, text="        Home Menu        ", font=self.controller.title_font,fg="#263942")
            label.grid(row=0, sticky="ew")
            #create interactive menu buttons
            button1 = tk.Button(self, text="   Add a Family Member  ", fg="#ffffff", bg="#382642",command=lambda: self.controller.show_frame("PageOne"))
            button2 = tk.Button(self, text="   Launch Camera ", fg="#ffffff", bg="#382642",command=lambda: self.controller.show_frame("PageTwo"))
            button3 = tk.Button(self, text="Quit", fg="#ffffff", bg="#382642", command=self.on_closing)
            button1.grid(row=1, column=0, ipady=3, ipadx=7)
            button2.grid(row=2, column=0, ipady=3, ipadx=2)
            button3.grid(row=3, column=0, ipady=3, ipadx=32)
       

        #double check with user if they want to quit app/save user information
        def on_closing(self):
            if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
                global names
                with open("nameslist.txt", "w") as f:
                    for i in names:
                        f.write(i + " ")
                self.controller.destroy()

#add new family member menu
class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="Enter name of family member", fg="#263942", font='Helvetica 12 bold').grid(row=0, column=0, pady=10, padx=5)
        self.user_name = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.user_name.grid(row=0, column=1, pady=10, padx=10)
        self.buttoncanc = tk.Button(self, text="Cancel", bg="#ffffff", fg="#263942", command=lambda: controller.show_frame("StartPage"))
        self.buttonext = tk.Button(self, text="Next", fg="#ffffff", bg="#263942", command=self.start_training)
        self.buttoncanc.grid(row=1, column=0, pady=10, ipadx=5, ipady=4)
        self.buttonext.grid(row=1, column=1, pady=10, ipadx=5, ipady=4)
        #ensure name is not 'none'
    def start_training(self):
        global names
        if self.user_name.get() == "None":
            messagebox.showerror("Error", "Name cannot be an empty field.")
            return #ensure name is not a duplicate
        elif self.user_name.get() in names:
            messagebox.showerror("Error, name is already taken. Please enter different name.")
            return #ensure name is not a duplicate
        elif len(self.user_name.get()) == 0:
            messagebox.showerror("Error", "Name cannot be Null. Please enter different name.")
            return
        name = self.user_name.get()
        names.add(name)
        #proceed to next menu once name is valid
        self.controller.active_name = name
        self.controller.frames["PageTwo"].refresh_names()
        self.controller.show_frame("PageThree")

#launch camera menu
class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global names
        self.controller = controller
        tk.Label(self, text="Select user", fg="#382642", font='Helvetica 12 bold').grid(row=0, column=0, padx=10, pady=10)
        self.buttoncanc = tk.Button(self, text="Cancel", command=lambda: controller.show_frame("StartPage"), bg="#ffffff", fg="#263942")
        self.menuvar = tk.StringVar(self)
        self.dropdown = tk.OptionMenu(self, self.menuvar, *names)
        self.dropdown.config(bg="lightgrey")
        self.dropdown["menu"].config(bg="lightgrey")
        self.buttonext = tk.Button(self, text="Next", command=self.nextfoo, fg="#ffffff", bg="#263942")
        self.dropdown.grid(row=0, column=1, ipadx=8, padx=10, pady=10)
        self.buttoncanc.grid(row=1, ipadx=5, ipady=4, column=0, pady=10)
        self.buttonext.grid(row=1, ipadx=5, ipady=4, column=1, pady=10)
#return to menu if name is invalid
    def nextfoo(self):
        if self.menuvar.get() == "None":
            messagebox.showerror("ERROR", "Name cannot be 'None'")
            return
        self.controller.active_name = self.menuvar.get()
        self.controller.show_frame("PageFour")
#add name to user list once upload is complete
    def refresh_names(self):
        global names
        self.menuvar.set('')
        self.dropdown['menu'].delete(0, 'end')
        for name in names:
            self.dropdown['menu'].add_command(label=name, command=tk._setit(self.menuvar, name))

class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.numimglabel = tk.Label(self, text="Number of images captured = 0", font='Helvetica 12 bold', fg="#382642")
        self.numimglabel.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)
        self.capturebutton = tk.Button(self, text="Capture Images", fg="#ffffff", bg="#382642", command=self.capimg)
        self.trainbutton = tk.Button(self, text="Train The Recognizer", fg="#ffffff", bg="#382642",command=self.trainmodel)
        self.capturebutton.grid(row=1, column=0, ipadx=5, ipady=4, padx=10, pady=20)
        self.trainbutton.grid(row=1, column=1, ipadx=5, ipady=4, padx=10, pady=20)

    def capimg(self):
        self.numimglabel.config(text=str("Captured Images = 0 "))
        messagebox.showinfo("INSTRUCTIONS", "Ensure only one person is in view. Stay still & make various faces.")
        x = start_capture(self.controller.active_name)
        self.controller.num_of_images = x
        self.numimglabel.config(text=str("Number of images = "+str(x)))
#model needs at least 300 images, if less prompt the user to take more images
#if model is succesfully trained, return to menu
    def trainmodel(self):
        if self.controller.num_of_images < 300:
            messagebox.showerror("ERROR", "Need more images captured.")
            return
        train_classifer(self.controller.active_name)
        messagebox.showinfo("SUCCESS", "The model has been trained and is ready!")
        self.controller.show_frame("PageFour")

#menu to launch camera scan or return to home menu
class PageFour(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Face Recognition", font='Helvetica 16 bold')
        label.grid(row=0,column=0, sticky="ew")
        button1 = tk.Button(self, text="Start Camera", command=self.openwebcam, fg="#ffffff", bg="#382642")
        #button2 = tk.Button(self, text="Emotion Detection", command=self.emot, fg="#ffffff", bg="#263942")
        #button3 = tk.Button(self, text="Gender and Age Prediction", command=self.gender_age_pred, fg="#ffffff", bg="#263942")
        button4 = tk.Button(self, text="Go to Home Page", command=lambda: self.controller.show_frame("StartPage"), bg="#ffffff", fg="#382642")
        button1.grid(row=1,column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        #button2.grid(row=1,column=1, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        #button3.grid(row=2,column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        button4.grid(row=1,column=1, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)

    def openwebcam(self):
        main_app(self.controller.active_name)
    #def gender_age_pred(self):
     #  ageAndgender()
    #def emot(self):
     #   emotion()


#launch menu and app icon
app = MainUI()
app.iconphoto(False, tk.PhotoImage(file='icon.ico'))
app.mainloop()

