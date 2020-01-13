import os
import tkinter as tk
from tkinter import messagebox, filedialog, ttk

from openbiolink.gui import gui as gui


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.info_text = "select "

        titles_panel = tk.Frame(self)
        info = tk.Button(titles_panel, text=" help ", command=lambda: gui.show_info_box(self.info_text))
        title = tk.Label(titles_panel, text="Select Actions", font=controller.title_font)

        self.working_dir_el = self._create_working_dir_el(self)

        actions_panel = tk.LabelFrame(self, text='Actions')
        self.g = tk.BooleanVar()
        g_box = tk.Checkbutton(actions_panel, text="(1) Generate Graph", variable=self.g)
        self.s = tk.BooleanVar()
        s_box = tk.Checkbutton(actions_panel, text="(2) Generate Train Test Split", variable=self.s)
        self.e = tk.BooleanVar()
        e_box = tk.Checkbutton(actions_panel, text="(3) Apply Testing and Evaluation", variable=self.e)

        buttons_panel = tk.Frame(self)
        next_button = tk.Button(buttons_panel, text="Next", command=lambda: self.next_page(), height=1, width=15)

        titles_panel.pack(side="top", fill="x", pady=10)
        title.pack(side='left', pady=10, padx=15)
        info.pack(side="right", fill="x", pady=10, padx=15)
        self.working_dir_el.pack(side='top', fill='both', padx=15, pady=10, expand=True)
        actions_panel.pack(side='top', fill='both', expand=True, anchor='w', padx=15, pady=10)
        g_box.pack(side='top', anchor='w', padx=20, pady=(20, 0))
        s_box.pack(side='top', anchor='w', padx=20, pady=(20, 0))
        e_box.pack(side='top', anchor='w', padx=20, pady=(20, 0))
        ttk.Separator(self, orient='horizontal').pack(side='top', fill='x', pady=(15, 0), padx=10, anchor='s')
        buttons_panel.pack(side='bottom', padx=15, fill='x')
        next_button.pack(side='right', anchor='e', pady=(5, 10))

    def _create_working_dir_el(self, parent):
        el = tk.LabelFrame(parent, text="Working Directory")
        self.path = tk.StringVar(value=os.getcwd())  # todo good idea?
        path_button = tk.Button(el, text="select path ...", command=lambda: self.browse_dir())
        path_label = tk.Label(el, textvariable=self.path)
        path_button.pack(side='left', anchor='w', padx=5, pady=5)
        path_label.pack(side='left', anchor='w', padx=5, pady=5)
        return el

    def browse_dir(self):
        self.path.set(filedialog.askdirectory())

    def next_page(self):
        self.controller.ARGS_LIST_GLOBAL = []
        if self.path.get() == '':
            messagebox.showerror('ERROR', 'Please select a path')
            return
        self.controller.ARGS_LIST_GLOBAL.extend(['-p', self.path.get()])

        selected_frames = []
        if self.g.get():
            selected_frames.append("GraphCreationFrame")
        else:
            self.ARGS_LIST_GRAPH_CREATION = []
        if self.s.get():
            selected_frames.append("SplitFrame")
        else:
            self.controller.ARGS_LIST_TRAIN_TEST_SPLIT = []
        if self.e.get():
            selected_frames.append("EvalFrame")
        else:
            self.controller.ARGS_LIST_EVAL = []
        if len(selected_frames) < 1:
            messagebox.showerror("ERROR", "At least one action must be chosen!")
            return
        self.controller.set_selected_frames(selected_frames)
        self.controller.show_next_frame()
