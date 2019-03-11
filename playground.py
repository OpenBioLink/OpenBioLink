import tkinter as tk
from tkinter import font  as tkfont, messagebox
import playgroud2 as arg

#arg.G= 0
#arg.S= 0
#arg.C= 0
#arg.T= 0
#arg.E = 0
#
LOO = 'FOO'

ARGS_LIST_GRAPH_CREATION = []
ARGS_LIST_TRAIN_TEST_SPLT= []


class BimegGui(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, GraphCreationFrame, SplitFrame, CrossValFrame, TrainFrame, EvalFrame):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def start(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            app.destroy() #todo implement


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="This is the start page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.g = tk.IntVar()
        g_box = tk.Checkbutton(self, text="Generate Graph", variable=self.g)
        self.s = tk.IntVar()
        s_box = tk.Checkbutton(self, text="Generate Train Test Split", variable=self.s)
        self.c = tk.IntVar()
        c_box = tk.Checkbutton(self, text="Apply hyperparameter optimization via cross validation", variable=self.c)
        self.t = tk.IntVar()
        t_box = tk.Checkbutton(self, text="Apply Training", variable=self.t)
        self.e = tk.IntVar()
        e_box = tk.Checkbutton(self, text="Apply Testing and Evaluation", variable=self.e)

        next_button = tk.Button(self, text="Go to NEXT", command=lambda: self.next_page())

        g_box.pack()
        s_box.pack()
        c_box.pack()
        t_box.pack()
        e_box.pack()

        next_button.pack()

    def next_page(self):
        LOO = 25
        arg.G= self.g.get()
        arg.S= self.s.get()
        arg.C= self.c.get()
        arg.T= self.t.get()
        arg.E = self.e.get()
        if arg.G== 1:
            nextFrame = "GraphCreationFrame"
        elif arg.S== 1:
            nextFrame = "SplitFrame"
        elif arg.C== 1:
            nextFrame = "CrossValFrame"
        elif arg.T== 1:
            nextFrame = "TrainFrame"
        elif arg.E == 1:
            nextFrame = "EvalFrame"
        else:
            messagebox.showerror("ERROR", "At least one action must be chosen!")
            return
        print(LOO)
        self.controller.show_frame(nextFrame)


class GraphCreationFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Graph Creation", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        if arg.LAST =='G':
            next_button = tk.Button(self, text="Start", command=lambda: controller.start())
        else:
            next_button = tk.Button(self, text="Next", command=lambda: self.next_page())

        next_button.pack()

    def next_page(self):
        if arg.S== 1:
            nextFrame = "SplitFrame"
        elif arg.C== 1:
            nextFrame = "CrossValFrame"
        elif arg.T== 1:
            nextFrame = "TrainFrame"
        else:
            nextFrame = "EvalFrame"
        print(LOO)
        self.controller.show_frame(nextFrame)


class SplitFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Split Creation", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        if arg.LAST == 'S':
            next_button = tk.Button(self, text="Start", command=lambda: controller.start())
        else:
            next_button = tk.Button(self, text="Next", command=lambda: self.next_page())

        next_button.pack()

    def next_page(self):
        if arg.C== 1:
            nextFrame = "CrossValFrame"
        elif arg.T== 1:
            nextFrame = "TrainFrame"
        else:
            nextFrame = "EvalFrame"
        print(LOO)
        self.controller.show_frame(nextFrame)


class CrossValFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text=" Hyperparameter Optimization (Cross Validation)", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        if arg.LAST == 'C':
            next_button = tk.Button(self, text="Start", command=lambda: controller.start())
        else:
            next_button = tk.Button(self, text="Next", command=lambda: self.next_page())
        next_button.pack()

    def next_page(self):
        if arg.T== 1:
            nextFrame = "TrainFrame"
        else:
            nextFrame = "EvalFrame"
        print(LOO)
        self.controller.show_frame(nextFrame)


class TrainFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Training", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        if arg.LAST == 'T':
            next_button = tk.Button(self, text="Start", command=lambda: controller.start())
        else:
            next_button = tk.Button(self, text="Next", command=lambda: self.next_page())
        next_button.pack()

    def next_page(self):
        nextFrame = "EvalFrame"
        self.controller.show_frame(nextFrame)


class EvalFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Testing and Evaluation", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        next_button = tk.Button(self, text="Start", command=lambda: controller.start())

        next_button.pack()




if __name__ == "__main__":
    app = BimegGui()


    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            app.destroy()


    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()