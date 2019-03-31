import tkinter as tk
from tkinter import font  as tkfont, messagebox, filedialog


class BimegGui(tk.Tk):
    ARGS_LIST_GRAPH_CREATION = []
    ARGS_LIST_TRAIN_TEST_SPLT = []

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.args = []

        self.selected_frames = ['ConfirmFrame']
        self.current_frame_index = 0

        self.frames = {}
        for F in (StartPage, GraphCreationFrame, SplitFrame, CrossValFrame, TrainFrame, EvalFrame, ConfirmFrame):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")


    def set_selected_frames(self, selected_frames):
         self.selected_frames = selected_frames + self.selected_frames


    def show_next_frame(self):
        if self.current_frame_index == len(self.selected_frames):
            self.start()
        else:
            self.show_frame(self.selected_frames[self.current_frame_index])
            self.current_frame_index += 1


    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def start(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            app.destroy()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="This is the start page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.g = tk.BooleanVar()
        g_box = tk.Checkbutton(self, text="Generate Graph", variable=self.g)
        self.s = tk.BooleanVar()
        s_box = tk.Checkbutton(self, text="Generate Train Test Split", variable=self.s)
        self.c = tk.BooleanVar()
        c_box = tk.Checkbutton(self, text="Apply hyperparameter optimization via cross validation", variable=self.c)
        self.t = tk.BooleanVar()
        t_box = tk.Checkbutton(self, text="Apply Training", variable=self.t)
        self.e = tk.BooleanVar()
        e_box = tk.Checkbutton(self, text="Apply Testing and Evaluation", variable=self.e)

        next_button = tk.Button(self, text="NEXT", command=lambda: self.next_page())

        g_box.pack()
        s_box.pack()
        c_box.pack()
        t_box.pack()
        e_box.pack()

        next_button.pack()

    def next_page(self):
        selected_frames = []

        if self.g.get():
            selected_frames.append("GraphCreationFrame")
        if self.s.get():
            selected_frames.append("SplitFrame")
        if self.c.get():
            selected_frames.append("CrossValFrame")
        if self.t.get():
            selected_frames.append("TrainFrame")
        if self.e.get():
            selected_frames.append("EvalFrame")
        if len(self.controller.selected_frames)<1:
            messagebox.showerror("ERROR", "At least one action must be chosen!")
            return
        self.controller.set_selected_frames(selected_frames)
        self.controller.show_next_frame()


class GraphCreationFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Graph Creation", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.path = ''
        tk.Button(self, text="select path ...", command=lambda: self.browse_dir()).pack()
        self.undir = tk.BooleanVar()
        tk.Checkbutton(self, text='graph is undirected', variable=self.undir).pack()
        self.qual = tk.StringVar()

        tk.Radiobutton(self, text="High Quality",padx=20, variable=self.qual,value='hq').pack()
        tk.Radiobutton(self, text="Medium Quality",padx=20, variable=self.qual,value='mq').pack()
        tk.Radiobutton(self, text="Low Quality",padx=20, variable=self.qual,value='lq').pack()

        tk.Button(self, text="Next", command=lambda: self.next_page()).pack()

        #self.no_interact = tk.BooleanVar()
        #no_interact_box = tk.Checkbutton(self, text='graph is undirected', variable=self.no_interact)

        #self.skip = tk.BooleanVar()
        #skip_box = tk.Checkbutton(self, text='graph is undirected', variable=self.skip)


    def browse_dir(self):
        self.path = filedialog.askdirectory()


    def next_page(self):
        self.controller.ARGS_LIST_GRAPH_CREATION.append('-g')
        if self.path == '':
            messagebox.showerror('ERROR', 'Please select a path')
            return
        self.controller.ARGS_LIST_GRAPH_CREATION.extend(['--path', self.path])
        if self.undir.get():
            self.controller.ARGS_LIST_GRAPH_CREATION.append('--undir')
        if not self.qual.get() == '':
            self.controller.ARGS_LIST_GRAPH_CREATION.extend(['--qual',self.qual.get() ])
        self.controller.show_next_frame()


class SplitFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Split Creation", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        next_button = tk.Button(self, text="Next", command=lambda: self.next_page())

        next_button.pack()

    def next_page(self):
        self.controller.show_next_frame()


class CrossValFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text=" Hyperparameter Optimization (Cross Validation)", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        next_button = tk.Button(self, text="Next", command=lambda: self.next_page())
        next_button.pack()

    def next_page(self):
        self.controller.show_next_frame()


class TrainFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Training", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        next_button = tk.Button(self, text="Next", command=lambda: self.next_page())
        next_button.pack()

    def next_page(self):
        self.controller.show_next_frame()


class EvalFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Testing and Evaluation", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        next_button = tk.Button(self, text="Start", command=lambda: self.next_page())
        next_button.pack()

    def next_page(self):
        self.controller.show_next_frame()



class ConfirmFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Confirm and Start", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        next_button = tk.Button(self, text="Start", command=lambda: self.controller.start())
        next_button.pack()



if __name__ == "__main__":
    app = BimegGui()


    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            app.destroy()


    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()