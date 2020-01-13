import os
import sys
import tkinter as tk
from tkinter import font  as tkfont, messagebox
from tkinter.ttk import Style

from openbiolink import openBioLink
from openbiolink.gui.confirmFrame import ConfirmFrame
from openbiolink.gui.console import ConsoleFrame
from openbiolink.gui.evaluationFrame import EvalFrame
from openbiolink.gui.graphCreationFrame import GraphCreationFrame
from openbiolink.gui.splitFrame import SplitFrame
from openbiolink.gui.startPage import StartPage

app = None


class BimegGui(tk.Tk):
    ARGS_LIST_GLOBAL = []
    ARGS_LIST_GRAPH_CREATION = []
    ARGS_LIST_TRAIN_TEST_SPLIT = []
    ARGS_LIST_EVAL = []

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Define Fonts
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.info_font = tkfont.Font(family='Helvetica', size=7, slant="italic")
        # Define base container
        self.container = tk.Frame(self)
        # self.wm_geometry('600x470')
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Initialize all frames
        self.frames = {}
        for F in (StartPage, GraphCreationFrame, SplitFrame, EvalFrame, ConfirmFrame, ConsoleFrame):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.args = []

        self.selected_frames = ['ConfirmFrame']
        self.next_frame_index = 0

        self.show_frame("StartPage")

    def get_args(self):
        arg_list = []
        arg_list.extend(self.ARGS_LIST_GLOBAL)
        arg_list.extend(self.ARGS_LIST_GRAPH_CREATION)
        arg_list.extend(self.ARGS_LIST_TRAIN_TEST_SPLIT)
        arg_list.extend(self.ARGS_LIST_EVAL)
        return arg_list

    def set_selected_frames(self, selected_frames):
        self.selected_frames = selected_frames + self.selected_frames

    def show_next_frame(self):
        if self.next_frame_index == len(self.selected_frames):
            self.start()
        else:
            self.show_frame(self.selected_frames[self.next_frame_index])
            self.next_frame_index += 1

    def show_previous_frame(self):
        if self.next_frame_index == 1:
            self.next_frame_index = 0
            self.show_frame("StartPage")
            self.selected_frames = ['ConfirmFrame']

        else:
            self.next_frame_index -= 1
            self.show_frame(self.selected_frames[self.next_frame_index - 1])

    def show_frame(self, page_name):
        """ Show a frame for the given page name """
        frame = self.frames[page_name]
        frame.controller = self
        frame.update()
        frame.tkraise()

    def start(self):
        """ start script and close gui"""
        if messagebox.askokcancel("Start", "Do you want to start now?"):
            self.show_frame("ConsoleFrame")
            arg_list = self.get_args()
            openBioLink.main(args_list=arg_list)
            # fixme start detached
            # app.destroy()


#################### ASK FOR EXIT ############################

class AskForExitPopup:
    def __init__(self, message):
        win = self.win = tk.Toplevel()

        l = tk.Label(self.win, text=message)
        l.grid(row=0, column=0)

        b1 = tk.Button(win, text="Cancel", command=self.cancel)
        b2 = tk.Button(win, text="Continue", command=self.go_on)
        b1.grid(row=1, column=0)
        b2.grid(row=1, column=1)
        win.wait_window()

    def cancel(self):
        self.win.destroy()
        return True

    def go_on(self):
        self.win.destroy()
        return False


def askForExit(message):
    exit = AskForExitPopup(message)
    if exit:
        on_closing()


#################### SKIP EXISTING FILES ############################

class SkipExistingFilesPopup:
    def __init__(self, file_path):
        self.skip = None
        self.for_all = False
        self.win = tk.Toplevel()
        message = 'The file %s already exists' % (file_path)
        l = tk.Label(self.win, text=message)

        button_panel = tk.Frame(self.win)

        go_on_button = tk.Button(button_panel, text="continue anyways", command=self.go_on)
        go_on_all_button = tk.Button(button_panel, text="continue anyways for all files", command=self.go_on_for_all)
        skip_button = tk.Button(button_panel, text="skip this file", command=self.skip_this)
        skip_all_button = tk.Button(button_panel, text="skip all existing files", command=self.skip_all)
        exit_button = tk.Button(button_panel, text="exit", command=self.exit)
        l.pack(side='top')
        button_panel.pack(side='top')
        go_on_button.pack(side='left')
        go_on_all_button.pack(side='left')
        skip_button.pack(side='left')
        skip_all_button.pack(side='left')
        exit_button.pack(side='left')
        self.win.wait_window()

    def exit(self):
        self.win.destroy()
        self.skip = None
        self.for_all = None

    def go_on(self):
        self.win.destroy()
        self.skip = None
        self.for_all = False

    def go_on_for_all(self):
        self.win.destroy()
        self.skip = False
        self.for_all = True

    def skip_this(self):
        self.win.destroy()
        self.skip = True
        self.for_all = False

    def skip_all(self):
        self.win.destroy()
        self.skip = True
        self.for_all = True


def skipExistingFiles(file_path):
    skip = None
    for_all = False
    if os.path.isfile(file_path):
        popup_response = SkipExistingFilesPopup(file_path)
        skip = popup_response.skip
        for_all = popup_response.for_all
        if skip is None and for_all is None:
            on_closing()
    return skip, for_all


#################### MAIN GUI ############################

def on_closing():
    if messagebox.askokcancel("Quit", "Do you really want to quit?"):
        app.destroy()
        sys.exit()


def show_info_box(msg):
    if not bool(msg):
        msg = 'No info available'
    messagebox.showinfo('Info', msg)


def start_gui():
    global app
    app = BimegGui()
    app.style = Style()

    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()
