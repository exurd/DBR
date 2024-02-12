import tkinter as tk
import tkinter.font as tkFont
from tkinter.filedialog import askopenfilename
import pathlib
from modules import remover

class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey'):
        super().__init__(master)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()

class App:
    def __init__(self, root):
        #setting title
        root.title("DBR's really crappy GUI alternative")
        root.configure(background='dark grey')
        #setting window size
        width=600
        height=250
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GLineEdit_556 = EntryWithPlaceholder(root, "Enter the Roblox URL of badge / game / group to delete from.")
        GLineEdit_556["borderwidth"] = "1px"
        ft = tkFont.Font(family='Serif',size=14)
        GLineEdit_556["font"] = ft
        #GLineEdit_556["fg"] = "#333333"
        GLineEdit_556["justify"] = "left"
        #GLineEdit_556["text"] = "ROBLOX URL HERE!"
        GLineEdit_556["relief"] = "ridge"
        #GLineEdit_556.insert(0, "Enter the Roblox URL of badge / game / group to delete from.")
        GLineEdit_556.pack()
        GLineEdit_556.place(x=20,y=70,width=560,height=40)

        GButton_173=tk.Button(root)
        GButton_173['activebackground'] = 'dark red'
        GButton_173["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Serif',size=14,weight='bold')
        GButton_173["font"] = ft
        GButton_173["fg"] = "#000000"
        GButton_173["justify"] = "center"
        GButton_173["text"] = "DELETE BADGES"
        GButton_173.place(x=210,y=140,width=170,height=40)
        GButton_173["command"] = self.GButton_173_command

        GButton_28=tk.Button(root)
        GButton_28["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_28["font"] = ft
        GButton_28["fg"] = "#000000"
        GButton_28["justify"] = "center"
        GButton_28["text"] = ".txt"
        GButton_28.place(x=20,y=20,width=32,height=32)
        GButton_28["command"] = self.openFile

        def a(e):
            GButton_173['background'] = 'red'

        def b(e):
            GButton_173['background'] = 'SystemButtonFace'

        def aa(e):
            GButton_28['background'] = 'light green'

        def bb(e):
            GButton_28['background'] = 'SystemButtonFace'

        GButton_173.bind("<Enter>", a)
        GButton_173.bind("<Leave>", b)
        GButton_28.bind("<Enter>", aa)
        GButton_28.bind("<Leave>", bb)

    def GButton_173_command(self):
        print("command")

    def openFile(self):
        filename = askopenfilename(filetypes=[("Text files", ".txt")])
        if filename:
            path = pathlib.Path(filename)
            #print(path.suffix)

            if path.suffix == ".txt" or path.suffix == ".TXT":
                #print(filename)
                root.destroy()
                remover.delete_from_text_file(filename)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()