import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

class ConfirmFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        title = tk.Label(self, text="Confirm and Start", font=controller.title_font)

        global_variable_panel = tk.LabelFrame(self, text='Global Config')
        self.param_glob = tk.StringVar(value='')
        self.global_message = ScrolledText(global_variable_panel, height=2 )

        gc_variable_panel = tk.LabelFrame(self, text='Graph Creation Options')
        self.param_gc = tk.StringVar(value='')
        self.gc_message = ScrolledText(gc_variable_panel, height=3)


        tts_variable_panel = tk.LabelFrame(self, text='Train Test Split Options')
        self.param_tts = tk.StringVar(value='')
        tts_message = ScrolledText(tts_variable_panel, height=3)


        buttons_panel = tk.Frame(self)
        next_button = tk.Button(buttons_panel,text="Start", command=lambda: self.controller.start(), height=1, width=15)
        prev_button = tk.Button(buttons_panel,text="Back", command=lambda: self.controller.show_previous_frame(), height=1, width=15)

        title.pack(side="top", fill="x", pady=10)
        global_variable_panel.pack(side='top', fill='both', expand=True, padx=15)
        self.global_message.pack(side='left', fill='both', expand=True, anchor='w')
        gc_variable_panel.pack(side='top', fill='both', expand=True, padx=15)
        self.gc_message.pack(side='left', fill='both', expand=True, anchor='w')
        tts_variable_panel.pack(side='top', fill='both', expand=True, padx=15)
        tts_message.pack(side='left', fill='both', expand=True, anchor='w')

        ttk.Separator(self, orient='horizontal').pack(side='top', fill='x', pady=(15, 0), padx=10, anchor='s')
        buttons_panel.pack(side='bottom', padx=15,  fill='x')
        prev_button.pack(side='left', anchor='w', pady=(5, 10))
        next_button.pack(side='right', anchor='e', pady=(5, 10))

    def update(self):
        self.global_message.delete(1.0,'end')
        self.gc_message.delete(1.0,'end')
        self.gc_message.insert('end',self.args_list_to_string( self.controller.ARGS_LIST_GRAPH_CREATION))
        self.global_message.insert('end',self.args_list_to_string( self.controller.ARGS_LIST_GLOBAL))

        self.param_glob.set(self.args_list_to_string(self.controller.ARGS_LIST_GLOBAL))
        self.param_gc.set(self.args_list_to_string(self.controller.ARGS_LIST_GRAPH_CREATION))
        self.param_tts.set(self.args_list_to_string(self.controller.ARGS_LIST_TRAIN_TEST_SPLT))


    def args_list_to_string(self, arg_list):
        params_gc_string = ''
        for param in arg_list:
            if param.startswith('--'):
                params_gc_string = params_gc_string + '\n\t'
            params_gc_string = params_gc_string + ' ' + param
        return params_gc_string

