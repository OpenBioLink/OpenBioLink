import tkinter as tk
from tkinter import ttk

import gui.gui as gui
import evaluation.metricTypes as Metrics


class EvalFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.info_text = ""
        titles_panel = tk.Frame(self)
        metrics = [Metrics.MetricType[item] for item in dir(Metrics.MetricType) if not item.startswith("__")]
        self.info = tk.Button(titles_panel, text=" ? ", command=lambda: gui.show_info_box(self.info_text))
        self.title = tk.Label(titles_panel, text="(3) Testing and Evaluation", font=controller.title_font)
        metrics_frame = tk.Frame(self)
        self.metrics_dicr = {}
        for metric in metrics:
            self.metrics_dicr[metric.value] = tk.BooleanVar(value=True)
            cb = tk.Checkbutton(metrics_frame, text=metric.value, variable=self.metrics_dicr[metric.value])
            cb.pack(anchor='w')


        self.buttons_panel = tk.Frame(self)
        self.next_button = tk.Button(self.buttons_panel, text="Next", command=lambda: self.next_page(), height=1,
                                     width=15)
        self.prev_button = tk.Button(self.buttons_panel, text="Back",
                                     command=lambda: self.controller.show_previous_frame(), height=1, width=15)

        # packing
        titles_panel.pack(side="top", fill="x", pady=10)
        self.title.pack(side='left', pady=10, padx=15)
        self.info.pack(side="right", fill="x", pady=5, padx=15)
        metrics_frame.pack(side='top')


        ttk.Separator(self, orient='horizontal').pack(side='top', fill='x', pady=(15, 1), padx=10, anchor='s')
        self.buttons_panel.pack(side='bottom', padx=15, fill='x')
        self.prev_button.pack(side='left', anchor='w', pady=(5, 10))
        self.next_button.pack(side='right', anchor='e', pady=(5, 10))



    def next_page(self):
        self.controller.show_next_frame()



