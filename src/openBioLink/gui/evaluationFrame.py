import tkinter as tk
from tkinter import ttk

import gui.gui as gui


class EvalFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.info_text = ""
        titles_panel = tk.Frame(self)
        self.info = tk.Button(titles_panel, text=" ? ", command=lambda: gui.show_info_box(self.info_text))
        self.title = tk.Label(titles_panel, text="(3) Testing and Evaluation", font=controller.title_font)

        self.buttons_panel = tk.Frame(self)
        self.next_button = tk.Button(self.buttons_panel, text="Next", command=lambda: self.next_page(), height=1,
                                     width=15)
        self.prev_button = tk.Button(self.buttons_panel, text="Back",
                                     command=lambda: self.controller.show_previous_frame(), height=1, width=15)

        # packing
        titles_panel.pack(side="top", fill="x", pady=10)
        self.title.pack(side='left', pady=10, padx=15)
        self.info.pack(side="right", fill="x", pady=5, padx=15)

        ttk.Separator(self, orient='horizontal').pack(side='top', fill='x', pady=(15, 1), padx=10, anchor='s')
        self.buttons_panel.pack(side='bottom', padx=15, fill='x')
        self.prev_button.pack(side='left', anchor='w', pady=(5, 10))
        self.next_button.pack(side='right', anchor='e', pady=(5, 10))



    def next_page(self):
        self.controller.show_next_frame()



