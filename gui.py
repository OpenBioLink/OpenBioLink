import os
import tkinter as tk
from tkinter import font  as tkfont, messagebox, filedialog, ttk
import sys

import masterthesis


class BimegGui(tk.Tk):
    ARGS_LIST_GRAPH_CREATION = []
    ARGS_LIST_TRAIN_TEST_SPLT = []

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.info_font= tkfont.Font(family='Helvetica', size=7, slant="italic")

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.args = []

        self.selected_frames = ['ConfirmFrame']
        self.next_frame_index = 0

        self.frames = {}
        #self.frame_cls = {}
        #for cls in (StartPage, GraphCreationFrame, SplitFrame, CrossValFrame, TrainFrame, EvalFrame, ConfirmFrame):
        #    self.frame_cls[cls.__name__] = cls
        for F in (StartPage, GraphCreationFrame, SplitFrame, CrossValFrame, TrainFrame, EvalFrame, ConfirmFrame):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def get_args(self):
        arg_list = []
        arg_list.extend(self.ARGS_LIST_GRAPH_CREATION)
        arg_list.extend(self.ARGS_LIST_TRAIN_TEST_SPLT)
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
        if self.next_frame_index==1:
            self.next_frame_index = 0
            self.show_frame("StartPage")
            self.selected_frames = ['ConfirmFrame']

        else:
            self.next_frame_index -= 1
            self.show_frame(self.selected_frames[self.next_frame_index-1])

    def show_frame(self, page_name):
        """ Show a frame for the given page name """
        frame = self.frames[page_name]
        frame.controller = self
        frame.update()
        frame.tkraise()

    def start(self):
        """ start script and close gui"""
        if messagebox.askokcancel("Start", "Do you want to start now?"):
            arg_list = []
            arg_list.extend(self.ARGS_LIST_GRAPH_CREATION)
            arg_list.extend(self.ARGS_LIST_TRAIN_TEST_SPLT)
            masterthesis.main(args_list=arg_list)
            app.destroy()

    def ask_for_exit(self, message):
        """ start script and close gui"""
        if messagebox.askokcancel("Warning", message):
            arg_list = []
            arg_list.extend(self.ARGS_LIST_GRAPH_CREATION)
            arg_list.extend(self.ARGS_LIST_TRAIN_TEST_SPLT)
            masterthesis.main(args_list=arg_list)
            app.destroy()


#################### START PAGE ############################

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        title = tk.Label(self, text="Select actions", font=controller.title_font)

        actions_panel=tk.Frame(self)
        self.g = tk.BooleanVar()
        g_box = tk.Checkbutton(actions_panel, text="Generate Graph", variable=self.g)
        self.s = tk.BooleanVar()
        s_box = tk.Checkbutton(actions_panel, text="Generate Train Test Split", variable=self.s)
        self.c = tk.BooleanVar()
        c_box = tk.Checkbutton(actions_panel, text="Apply hyperparameter optimization via cross validation", variable=self.c)
        self.t = tk.BooleanVar()
        t_box = tk.Checkbutton(actions_panel, text="Apply Training", variable=self.t)
        self.e = tk.BooleanVar()
        e_box = tk.Checkbutton(actions_panel, text="Apply Testing and Evaluation", variable=self.e)



        buttons_panel = tk.Frame(self)
        next_button = tk.Button(buttons_panel, text="Next", command=lambda: self.next_page(),height = 1, width = 15 )

        title.pack(side="top", fill="x", pady=10)
        actions_panel.pack(side='top', fill='both', expand=True, anchor='w')
        g_box.pack()
        #s_box.pack()
        #c_box.pack()
        #t_box.pack()
        #e_box.pack()
        ttk.Separator(self, orient='horizontal').pack(side='top', fill='x', pady=(15, 0), padx=10, anchor='s')
        buttons_panel.pack(side='bottom', padx=15, fill='x')
        next_button.pack(side='right', anchor='e', pady=(5, 10))

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
        if len(selected_frames)<1:
            messagebox.showerror("ERROR", "At least one action must be chosen!")
            return
        self.controller.set_selected_frames(selected_frames)
        self.controller.show_next_frame()


#################### GRAPH CREATION PAGE ############################

class GraphCreationFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        title = tk.Label(self, text="Graph Creation", font=controller.title_font)
        working_dir_el = self._create_working_dir_el(self)
        options_panel = tk.Frame(self)
        actions_el = self._create_action_el(options_panel)
        graph_prop_el = self._create_graph_prop_el(options_panel)
        output_format_el = self._create_output_format_el(options_panel)

        buttons_panel = tk.Frame(self)
        next_button = tk.Button(buttons_panel, text="Next", command=lambda: self.next_page(),height = 1, width = 15 )
        prev_button = tk.Button(buttons_panel, text="Back", command=lambda: self.controller.show_previous_frame(), height=1, width=15)

        title.pack(side="top", fill="x", pady=10)
        working_dir_el.pack(side='top', fill='both', padx=15, pady=10, expand=True)
        options_panel.pack(side='top', fill='both', padx=5, pady=10, expand=True)
        actions_el.pack(side='left', fill='both', padx=10, expand=True)
        graph_prop_el.pack(side='left', fill='both', padx=10, expand=True)
        output_format_el.pack(side='left', fill='both', padx=10, expand=True)

        ttk.Separator(self, orient='horizontal').pack(side='top', fill='x', pady=(15,0), padx=10, anchor='s')
        buttons_panel.pack(side='bottom', padx=15, fill='x')
        prev_button.pack(side='left', anchor='w', pady=(5,10))
        next_button.pack(side='right', anchor='e', pady=(5,10))

        #self.no_interact = tk.BooleanVar()

        #no_interact_box = tk.Checkbutton(self, text='graph is undirected', variable=self.no_interact)

        #self.skip = tk.BooleanVar()
        #skip_box = tk.Checkbutton(self, text='graph is undirected', variable=self.skip)

    def _create_working_dir_el(self, parent):
        el = tk.LabelFrame(parent, text="Working Directory")

        self.path = tk.StringVar(value=os.getcwd())
        path_button = tk.Button(el, text="select path ...", command=lambda: self.browse_dir())
        path_label = tk.Label(el, textvariable=self.path)
        path_button.pack(side='left', anchor='w',padx=5, pady=5)
        path_label.pack(side='left', anchor='w',padx=5, pady=5)
        return el

    def _create_action_el(self, parent):
        el = tk.LabelFrame(parent, text="Actions")
        self.download = tk.BooleanVar(value=True)
        dl_box = tk.Checkbutton(el, text='perform download', variable=self.download)
        self.create_infiles = tk.BooleanVar(value=True)
        create_in_box = tk.Checkbutton(el, text='create infiles', variable=self.create_infiles)
        self.create_graph = tk.BooleanVar(value=True)
        create_graph_box = tk.Checkbutton(el, text='create graph', variable=self.create_graph)
        dl_box.pack(side='top',padx=5, anchor='w')
        create_in_box.pack(side='top',padx=5, anchor='w')
        create_graph_box.pack(side='top',padx=5, anchor='w')
        return el

    def _create_graph_prop_el(self, parent):
        el = tk.LabelFrame(parent, text="Graph Properties")
        # quality
        self.qual = tk.StringVar()
        hq_box = tk.Radiobutton(el, text="high quality", variable=self.qual, value='hq')
        mq_box = tk.Radiobutton(el, text="medium quality", variable=self.qual, value='mq')
        lq_box = tk.Radiobutton(el, text="low quality", variable=self.qual, value='lq')
        # undirected
        self.undir = tk.BooleanVar()
        directed_box = tk.Checkbutton(el, text='graph is undirected', variable=self.undir)
        # packing
        hq_box.pack(side='top',  padx=5, anchor='w')
        mq_box.pack(side='top',  padx=5, anchor='w')
        lq_box.pack(side='top',  padx=5, anchor='w')
        ttk.Separator(el, orient='horizontal').pack(side='top', fill='x', pady=2, padx=5, anchor='w')
        directed_box.pack(side='top', pady=2, padx=5, anchor='w')
        return el

    def _create_output_format_el(self, parent):
        el = tk.LabelFrame(parent, text="Output Format")
        # single outputfile
        self.one_output_file = tk.BooleanVar(value=True)
        single_out_file_box = tk.Checkbutton(el, text='single file', variable=self.one_output_file)
        self.single_sep = tk.StringVar(value='t')
        single_sep_frame=tk.Frame(el)
        single_sep_label = tk.Label(single_sep_frame, text='separator:')
        single_sep_info = tk.Label(single_sep_frame, text='(t for tab, n for newline)', font=self.controller.info_font)
        single_sep_value = tk.Entry(single_sep_frame, textvariable=self.single_sep, width=5)
        # multiple output files
        self.multi_output_file = tk.BooleanVar(value=False)
        multi_out_file_box = tk.Checkbutton(el, text='multiple files (one/type)', variable=self.multi_output_file)
        multi_sep_frame=tk.Frame(el)
        self.multi_sep = tk.StringVar(value=None)
        multi_sep_label = tk.Label(multi_sep_frame, text='separator:')
        multi_sep_info = tk.Label(multi_sep_frame, text='(t for tab, n for newline)', font=self.controller.info_font)
        multi_sep_value = tk.Entry(multi_sep_frame, textvariable=self.multi_sep, width=5)
        # qscore
        self.no_qscore = tk.BooleanVar(value=False)
        no_qscore_box = tk.Checkbutton(el, text='without quality score', variable=self.no_qscore)
        # packing
        single_out_file_box.pack(side='top',  padx=5, anchor='w')
        single_sep_frame.pack(side='top',  padx=5, anchor='w')
        single_sep_label.pack(side='left',  padx=5, anchor='w')
        single_sep_value.pack(side='left',   anchor='w')
        single_sep_info.pack(side='left',   anchor='w')
        ttk.Separator(el, orient='horizontal').pack(side='top', fill='x', pady=5, padx=5, anchor='w')
        multi_out_file_box.pack(side='top',  padx=5, anchor='w')
        multi_sep_frame.pack(side='top',  padx=5, anchor='w')
        multi_sep_label.pack(side='left',  padx=5, anchor='w')
        multi_sep_value.pack(side='left',   anchor='w')
        multi_sep_info.pack(side='left', anchor='w')
        ttk.Separator(el, orient='horizontal').pack(side='top', fill='x', pady=5, padx=5, anchor='w')
        no_qscore_box.pack(side='top',  padx=5, anchor='w')
        return el

    def browse_dir(self):
        self.path.set(filedialog.askdirectory())

    def next_page(self):
        self.controller.ARGS_LIST_GRAPH_CREATION=[]
        if self.path.get() == '':
            messagebox.showerror('ERROR', 'Please select a path')
            return
        if (self.one_output_file.get() and self.single_sep.get()=='') or (self.multi_output_file.get() and self.multi_sep.get()==''):
            messagebox.showerror('ERROR', 'Please provide a separator for desired output file')
            return
        self.controller.ARGS_LIST_GRAPH_CREATION.append('-g')
        self.controller.ARGS_LIST_GRAPH_CREATION.extend(['--path', self.path.get()])
        if self.undir.get():
            self.controller.ARGS_LIST_GRAPH_CREATION.append('--undir')
        if not self.qual.get() == '':
            self.controller.ARGS_LIST_GRAPH_CREATION.extend(['--qual',self.qual.get() ])
        if not self.download.get():
            self.controller.ARGS_LIST_GRAPH_CREATION.append('--no_dl')
        if not self.create_infiles.get():
            self.controller.ARGS_LIST_GRAPH_CREATION.append('--no_in')
        if not self.create_graph.get():
            self.controller.ARGS_LIST_GRAPH_CREATION.append('--no_create')
        if self.one_output_file.get():
            if self.multi_output_file.get():
                self.controller.ARGS_LIST_GRAPH_CREATION.extend(['--out_format', 'sm', self.single_sep.get()+self.multi_sep.get()])
            else:
                self.controller.ARGS_LIST_GRAPH_CREATION.extend(['--out_format', 's', self.single_sep.get()])
        elif self.multi_output_file.get():
            self.controller.ARGS_LIST_GRAPH_CREATION.extend(['--out_format', 'm' , self.multi_sep.get()])
        if self.no_qscore.get():
            self.controller.ARGS_LIST_GRAPH_CREATION.append('--no_qscore')

        self.controller.show_next_frame()


#################### TRAIN TEST SPLIT ############################

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


#################### CROSS VAL ############################

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

#################### TRAIN VAL ############################

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


#################### EVALUATE VAL ############################

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


#################### CONFIRM VAL ############################

class ConfirmFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        title = tk.Label(self, text="Confirm and Start", font=controller.title_font)

        gc_variable_panel = tk.LabelFrame(self, text='Graph Creation Options')
        self.param_gc = tk.StringVar(value='')
        gc_message = tk.Message(gc_variable_panel, textvariable=self.param_gc, width=500)

        tts_variable_panel = tk.LabelFrame(self, text='Train Test Split Options')
        self.param_tts = tk.StringVar(value='')
        tts_message = tk.Message(tts_variable_panel, textvariable=self.param_tts, width=500)


        buttons_panel = tk.Frame(self)
        next_button = tk.Button(buttons_panel,text="Start", command=lambda: self.controller.start(), height=1, width=15)
        prev_button = tk.Button(buttons_panel,text="Back", command=lambda: self.controller.show_previous_frame(), height=1, width=15)

        title.pack(side="top", fill="x", pady=10)
        gc_variable_panel.pack(side='top', fill='both', expand=True, padx=15, pady=5)
        gc_message.pack(side='left', fill='y', expand=True, anchor='w')
        tts_variable_panel.pack(side='top', fill='both', expand=True, padx=15, pady=5)
        tts_message.pack(side='left', fill='y', expand=True, anchor='w')

        ttk.Separator(self, orient='horizontal').pack(side='top', fill='x', pady=(15, 0), padx=10, anchor='s')
        buttons_panel.pack(side='bottom', padx=15,  fill='x')
        prev_button.pack(side='left', anchor='w', pady=(5, 10))
        next_button.pack(side='right', anchor='e', pady=(5, 10))

    def update(self):
        self.param_gc.set(self.args_list_to_string(self.controller.ARGS_LIST_GRAPH_CREATION))
        self.param_tts.set(self.args_list_to_string(self.controller.ARGS_LIST_TRAIN_TEST_SPLT))


    def args_list_to_string(self, arg_list):
        params_gc_string = ''
        for param in arg_list:
            if param.startswith('--'):
                params_gc_string = params_gc_string + '\n\t'
            params_gc_string = params_gc_string + ' ' + param
        return params_gc_string


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

def on_closing():
    if messagebox.askokcancel("Quit", "Do you really want to quit?"):
        app.destroy()
        sys.exit()

app = BimegGui()

app.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()