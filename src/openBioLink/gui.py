import os
import tkinter as tk
from tkinter import font  as tkfont, messagebox, filedialog
import sys
from . import openBioLink
from . import utils
from .graph_creation.metadata_db_file import DbMetadata
from .graph_creation.metadata_edge.edgeOntoMetadata import EdgeOntoMetadata
from .graph_creation.metadata_edge.edgeRegularMetadata import EdgeRegularMetadata
from .graph_creation import graphCreationConfig as gcConst
from tkinter.scrolledtext import ScrolledText

app = None


class BimegGui(tk.Tk):
    ARGS_LIST_GLOBAL = []
    ARGS_LIST_GRAPH_CREATION = []
    ARGS_LIST_TRAIN_TEST_SPLT = []
    ARGS_LIST_EVAL = []

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # Define Fonts
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.info_font= tkfont.Font(family='Helvetica', size=7, slant="italic")
        # Define base container
        self.container = tk.Frame(self)
        #self.wm_geometry('600x470')
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
        arg_list.extend(self.ARGS_LIST_TRAIN_TEST_SPLT)
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
            self.show_frame("ConsoleFrame")
            arg_list = self.get_args()
            #openBioLink.main(args_list=arg_list) #fixme CHANGE HERE
            #todo start detached
            #app.destroy()


#################### START PAGE ############################

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.info_text="select "

        titles_panel = tk.Frame(self)
        info = tk.Button(titles_panel, text=" ? ", command=lambda: show_info_box(self.info_text))
        title = tk.Label(titles_panel, text="Select Actions", font=controller.title_font)

        self.working_dir_el = self._create_working_dir_el(self)

        actions_panel=tk.LabelFrame(self, text='Actions')
        self.g = tk.BooleanVar()
        g_box = tk.Checkbutton(actions_panel, text="(1) Generate Graph", variable=self.g)
        self.s = tk.BooleanVar()
        s_box = tk.Checkbutton(actions_panel, text="(2) Generate Train Test Split", variable=self.s)
        self.e = tk.BooleanVar()
        e_box = tk.Checkbutton(actions_panel, text="(3) Apply Testing and Evaluation", variable=self.e)

        buttons_panel = tk.Frame(self)
        next_button = tk.Button(buttons_panel, text="Next", command=lambda: self.next_page(),height = 1, width = 15 )

        titles_panel.pack(side="top", fill="x", pady=10)
        title.pack(side='left', pady=10, padx=15)
        info.pack(side="right", fill="x", pady=10, padx=15)
        self.working_dir_el.pack(side='top', fill='both', padx=15, pady=10, expand=True)
        actions_panel.pack(side='top', fill='both', expand=True, anchor='w',padx=15, pady=10)
        g_box.pack(side='top', anchor='w', padx=20, pady=(20,0))
        s_box.pack(side='top', anchor='w', padx=20, pady=(20,0))
        e_box.pack(side='top', anchor='w', padx=20, pady=(20,0))
        ttk.Separator(self, orient='horizontal').pack(side='top', fill='x', pady=(15, 0), padx=10, anchor='s')
        buttons_panel.pack(side='bottom', padx=15, fill='x')
        next_button.pack(side='right', anchor='e', pady=(5, 10))

    def _create_working_dir_el(self, parent):
        el = tk.LabelFrame(parent, text="Working Directory")
        self.path = tk.StringVar(value=os.getcwd()) #todo good idea?
        path_button = tk.Button(el, text="select path ...", command=lambda: self.browse_dir())
        path_label = tk.Label(el, textvariable=self.path)
        path_button.pack(side='left', anchor='w',padx=5, pady=5)
        path_label.pack(side='left', anchor='w',padx=5, pady=5)
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
        if self.s.get():
            selected_frames.append("SplitFrame")
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
        self.info_text=''
        self.db_cls_list = [x for x in utils.get_leaf_subclasses(DbMetadata)]
        self.edge_metadata_cls_list = [x for x in utils.get_leaf_subclasses(EdgeRegularMetadata)] + \
                                      [x for x in utils.get_leaf_subclasses(EdgeOntoMetadata)]
        self.db_cls_list.sort(key=lambda x: x.NAME)
        self.edge_metadata_cls_list.sort(key=lambda x: x.NAME)
        self.selected_dbs = None
        self.selected_meta_edges = None

        titles_panel = tk.Frame(self)
        self.info = tk.Button(titles_panel, text=" ? ", command=lambda: show_info_box(self.info_text))
        self.title = tk.Label(titles_panel, text="(1) Graph Creation", font=controller.title_font)

        self.actions_el = self._create_action_el(self)
        select_panel = tk.Frame(self)
        self.select_el = self._create_select_db_meta_edges_el(select_panel)

        options_panel = tk.Frame(self)
        self.graph_prop_el = self._create_graph_prop_el(options_panel)
        self.output_format_el = self._create_output_format_el(options_panel)

        buttons_panel = tk.Frame(self)
        next_button = tk.Button(buttons_panel, text="Next", command=lambda: self.next_page(),height = 1, width = 15 )
        prev_button = tk.Button(buttons_panel, text="Back", command=lambda: self.controller.show_previous_frame(), height=1, width=15)

        titles_panel.pack(side="top", fill="x", pady=10)
        self.title.pack(side='left', pady=10, padx=15)
        self.info.pack(side="right", fill="x", pady=5, padx=15)
        self.actions_el.pack(side='top', fill='both', padx=15, pady=5, expand=True)
        select_panel.pack(side='top', fill='both', padx=10, pady=5, expand=True)
        self.select_el.pack(side='top', fill='both', padx=5, pady=10, expand=True)
        options_panel.pack(side='top', fill='both', padx=5, pady=5, expand=True)
        self.graph_prop_el.pack(side='left', fill='both', padx=10, expand=True)
        self.output_format_el.pack(side='left', fill='both', padx=10, expand=True)

        ttk.Separator(self, orient='horizontal').pack(side='top', fill='x', pady=(15,0), padx=10, anchor='s')
        buttons_panel.pack(side='bottom', padx=15, fill='x')
        prev_button.pack(side='left', anchor='w', pady=(5,10))
        next_button.pack(side='right', anchor='e', pady=(5,10))

    def _create_action_el(self, parent):
        el = tk.LabelFrame(parent, text="Actions")
        self.download = tk.BooleanVar(value=True)
        dl_box = tk.Checkbutton(el, text='perform download', variable=self.download)
        self.create_infiles = tk.BooleanVar(value=True)
        create_in_box = tk.Checkbutton(el, text='create infiles', variable=self.create_infiles)
        self.create_graph = tk.BooleanVar(value=True)
        create_graph_box = tk.Checkbutton(el, text='create graph', variable=self.create_graph, command=self.toggl_cg_elements)
        dl_box.pack(side='left',padx=5, anchor='w')
        create_in_box.pack(side='left',padx=5, anchor='w')
        create_graph_box.pack(side='left',padx=5, anchor='w')
        return el

    def _create_select_db_meta_edges_el(self, parent):
        el = tk.LabelFrame(parent, text="Customize Graph")
        self.select_choices = ['Default Graph',
                   'Use only subset of Source Databases',
                   'Use only subset of Meta edges']
        self.select = tk.StringVar(value=self.select_choices[0])
        select_menu = tk.OptionMenu(el, self.select, *self.select_choices, command=self.toggl_select_buttons)
        select_menu.config(width=32)
        self.select_db_button = tk.Button(el, text='select data bases...', command=self.select_dbs_popup)
        self.select_meta_edge_button = tk.Button(el, text='select meta edges...', command=self.select_mes_popup)
        select_menu.pack(side='left', padx=5, anchor='w')
        return el

    def select_dbs_popup(self):
        select_popup = tk.Toplevel()
        select_popup.wm_title("Select Source Databases")
        select_popup.wm_geometry('400x400')
        label = tk.Label(select_popup,text='Data Base Type - Data Base - Data Base File')
        filterPanel = tk.Frame(select_popup)
        select_all_button = tk.Button(filterPanel, text='select all', command=self.select_all_dbs)
        select_none_button = tk.Button(filterPanel, text='select none', command=self.unselect_all_dbs)
        frame=tk.Frame(select_popup)
        scrollbar = tk.Scrollbar(frame)
        self.db_selection = tk.Listbox(frame, selectmode='multiple', exportselection=0,yscrollcommand = scrollbar.set)
        for i,source_db_cls in enumerate(self.db_cls_list):
            self.db_selection.insert(i, source_db_cls.NAME)
            if source_db_cls in self.selected_dbs:
                self.db_selection.selection_set(i)

        scrollbar.config(command=self.db_selection.yview)
        ok_button = ttk.Button(select_popup, text="Okay", command=lambda: self.safe_select_dbs_and_quit(select_popup))

        label.pack(side='top', anchor='w', pady=10, padx=5)
        filterPanel.pack(side='top')
        select_all_button.pack(side='left')
        select_none_button.pack(side='left')
        frame.pack(side = 'top', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        self.db_selection.pack(fill='both', padx=10, expand=True)
        ok_button.pack(side='bottom')

    def select_all_dbs(self):
        for i, _ in enumerate(self.db_cls_list):
            self.db_selection.selection_set(i)

    def unselect_all_dbs(self):
        self.db_selection.selection_clear(0, len(self.db_cls_list)-1)

    def safe_select_dbs_and_quit(self, pop_up):
        self.selected_dbs = [self.db_cls_list[i] for i in self.db_selection.curselection()]
        pop_up.destroy()

    def select_mes_popup(self):
        select_popup = tk.Toplevel()
        select_popup.wm_title("Select Meta Edges")
        select_popup.wm_geometry('400x400')
        label = tk.Label(select_popup, text='Connection Type - Meta Edge Type')
        filterPanel = tk.Frame(select_popup)
        select_all_button = tk.Button(filterPanel, text='select all', command=self.select_all_mes)
        select_none_button = tk.Button(filterPanel, text='select none', command=self.unselect_all_mes)
        frame = tk.Frame(select_popup)
        scrollbar = tk.Scrollbar(frame)

        self.me_selection = tk.Listbox(frame, selectmode='multiple', exportselection=0, yscrollcommand = scrollbar.set)
        for i,source_me_cls in enumerate(self.edge_metadata_cls_list):
            self.me_selection.insert(i, source_me_cls.NAME)
            if source_me_cls in self.selected_meta_edges:
                self.me_selection.selection_set(i)
        scrollbar.config(command=self.me_selection.yview)
        ok_button = ttk.Button(select_popup, text="Okay", command=lambda: self.safe_select_mes_and_quit(select_popup))

        label.pack(side='top', anchor='w', pady=10, padx=5)
        filterPanel.pack(side='top')
        select_all_button.pack(side='left')
        select_none_button.pack(side='left')
        frame.pack(side='top', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        self.me_selection.pack(fill='both', padx=10, expand=True)
        ok_button.pack(side='bottom')


    def safe_select_mes_and_quit(self, pop_up):
        self.selected_meta_edges = [self.edge_metadata_cls_list[i] for i in self.me_selection.curselection()]
        pop_up.destroy()

    def select_all_mes(self):
        for i, _ in enumerate(self.edge_metadata_cls_list):
            self.me_selection.selection_set(i)

    def unselect_all_mes(self):
        self.me_selection.selection_clear(0, len(self.edge_metadata_cls_list) - 1)

    def toggl_select_buttons(self, select_choice):
        if select_choice == self.select_choices[0]:
            self.selected_dbs = None
            self.selected_meta_edges = None
            self.select_db_button.pack_forget()
            self.select_meta_edge_button.pack_forget()
        elif select_choice == self.select_choices[1]:
            self.selected_dbs = self.db_cls_list.copy()
            self.selected_meta_edges = None
            self.select_db_button.pack(side='right', padx=5, anchor='w')
            self.select_meta_edge_button.pack_forget()
            self.select_dbs_popup()
        elif select_choice == self.select_choices[2]:
            self.selected_dbs = None
            self.selected_meta_edges = self.edge_metadata_cls_list.copy()
            self.select_db_button.pack_forget()
            self.select_meta_edge_button.pack(side='right', padx=5, anchor='w')
            self.select_mes_popup()

    def _create_graph_prop_el(self, parent):
        el = tk.LabelFrame(parent, text="Graph Properties")
        # quality
        self.qual = tk.StringVar(value='None')
        hq_box = tk.Radiobutton(el, text="high quality", variable=self.qual, value='hq')
        mq_box = tk.Radiobutton(el, text="medium quality", variable=self.qual, value='mq')
        lq_box = tk.Radiobutton(el, text="low quality", variable=self.qual, value='lq')
        none_box = tk.Radiobutton(el, text="no quality cutoff", variable=self.qual, value='None')
        # undirected
        self.undir = tk.BooleanVar()
        undirected_box = tk.Radiobutton(el, text='undirected', variable=self.undir, value=True)
        directed_box = tk.Radiobutton(el, text='directed', variable=self.undir, value=False)
        # packing
        none_box.pack(side='top',  padx=5, anchor='w')
        hq_box.pack(side='top',  padx=5, anchor='w')
        mq_box.pack(side='top',  padx=5, anchor='w')
        lq_box.pack(side='top',  padx=5, anchor='w')
        ttk.Separator(el, orient='horizontal').pack(side='top', fill='x', pady=2, padx=5, anchor='w')
        directed_box.pack(side='top', pady=2, padx=5, anchor='w')
        undirected_box.pack(side='top', pady=2, padx=5, anchor='w')
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

    def toggl_cg_elements(self):
        if self.graph_prop_el.winfo_ismapped():
            self.select_el.pack_forget()
            self.graph_prop_el.pack_forget()
            self.output_format_el.pack_forget()
        else:
            self.select_el.pack(side='top', fill='both', padx=5, expand=True)
            self.graph_prop_el.pack(side='left', fill='both', padx=10, expand=True)
            self.output_format_el.pack(side='left', fill='both', padx=10, expand=True)


    def next_page(self):
        self.controller.ARGS_LIST_GRAPH_CREATION=[]
        if (self.one_output_file.get() and self.single_sep.get()=='') or (self.multi_output_file.get() and self.multi_sep.get()==''):
            messagebox.showerror('ERROR', 'Please provide a separator for desired output file')
            return
        self.controller.ARGS_LIST_GRAPH_CREATION.append('-g')
        if self.undir.get():
            self.controller.ARGS_LIST_GRAPH_CREATION.append('--undir')
        if not self.qual.get() == 'None':
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
        if self.selected_dbs:
            self.controller.ARGS_LIST_GRAPH_CREATION.append('--dbs')
            self.controller.ARGS_LIST_GRAPH_CREATION.extend([x.__module__+'.'+x.__name__ for x in self.selected_dbs])
        if self.selected_meta_edges:
            self.controller.ARGS_LIST_GRAPH_CREATION.append('--mes')
            self.controller.ARGS_LIST_GRAPH_CREATION.extend([x.__module__+'.'+x.__name__ for x in self.selected_meta_edges])

        self.controller.show_next_frame()


#################### TRAIN TEST SPLIT ############################

class SplitFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.info_text=""
        titles_panel = tk.Frame(self)
        self.info = tk.Button(titles_panel, text=" ? ", command=lambda: show_info_box(self.info_text))
        self.title = tk.Label(titles_panel, text="(2) Split Creation", font=controller.title_font)

        self.mode_panel = self._create_mode_element(self)

        self.option_panel = tk.Frame(self)
        self.left_box = tk.LabelFrame(self.option_panel, text='graph files')
        self.file_edge_el = self._create_edge_path_el(self.left_box)
        self.file_tn_el = self._create_tn_path_el(self.left_box)
        self.file_nodes_el = self._create_nodes_path_el(self.left_box)
        self.right_box = tk.Frame(self.option_panel)
        self.right_rand_box = tk.LabelFrame(self.right_box, text='parameter for random split')
        self.rand_box_el = self._create_rand_options_el(self.right_rand_box)
        self.right_time_box = tk.LabelFrame(self.right_box, text='parameter for time slice')

        self.buttons_panel = tk.Frame(self)
        self.next_button = tk.Button(self.buttons_panel, text="Next", command=lambda: self.next_page(), height=1, width=15)
        self.prev_button = tk.Button(self.buttons_panel, text="Back", command=lambda: self.controller.show_previous_frame(), height=1, width=15)

        # packing
        titles_panel.pack(side="top", fill="x", pady=10)
        self.title.pack(side='left', pady=10, padx=15)
        self.info.pack(side="right", fill="x", pady=5, padx=15)

        self.mode_panel.pack(side='top',fill='both', expand=True)
        self.option_panel.pack(side='top',fill='both', padx=15, pady=10, expand=True)
        self.left_box.pack(side='left', fill='both', expand=True)
        self.file_edge_el.pack(side='top', fill='both', padx=15, pady=10, expand=True)
        self.file_tn_el.pack(side='top', fill='both', padx=15, pady=10, expand=True)
        self.file_nodes_el.pack(side='top', fill='both', padx=15, pady=10, expand=True)
        self.right_box.pack(side='left',fill='both', expand=True)
        self.right_rand_box.pack(fill='both', expand=True)
        self.rand_box_el.pack(fill='both', expand=True)


        ttk.Separator(self, orient='horizontal').pack(side='top', fill='x', pady=(15, 0), padx=10, anchor='s')
        self.buttons_panel.pack(side='bottom', padx=15, fill='x')
        self.prev_button.pack(side='left', anchor='w', pady=(5,10))
        self.next_button.pack(side='right', anchor='e', pady=(5, 10))


    def _create_mode_element(self, parent):
        el = tk.LabelFrame(parent, text="Split Mode")
        self.mode = tk.StringVar(value='rand')
        random_box = tk.Radiobutton(el, text='random split', variable=self.mode, value='rand', command=self.toggl_tts_elements)
        time_box = tk.Radiobutton(el, text='time slice', variable=self.mode, value='time',
                                          command=self.toggl_tts_elements)
        random_box.pack(side='left', padx=5, anchor='w')
        time_box.pack(side='left', padx=5, anchor='w')
        return el

    def toggl_tts_elements(self):
        if self.mode.get() =='time':
            self.right_rand_box.pack_forget()
            self.right_time_box.pack()
        elif self.mode.get() == 'rand':
            self.right_rand_box.pack()
            self.right_time_box.pack_forget()


    def _create_rand_options_el(self, parent):
        el = tk.Frame(parent)
        # test frac
        self.test_frac = tk.StringVar(value='0.2')  # todo int
        test_frac_frame = tk.Frame(el)
        test_frac_label = tk.Label(test_frac_frame, text='test set fraction:')
        test_frac_value = tk.Entry(test_frac_frame, textvariable=self.test_frac, width=5)
        test_frac_info = tk.Label(test_frac_frame, text='as float, e.g. 0.2', font=self.controller.info_font)

        # cross val
        self.crossval = tk.BooleanVar(value=False)
        crossval_box = tk.Checkbutton(el, text='cross validation', variable=self.crossval)
        self.folds = tk.StringVar(value='5') #todo int
        folds_frame = tk.Frame(el)
        folds_label = tk.Label(folds_frame, text='folds:')
        folds_value = tk.Entry(folds_frame, textvariable=self.folds, width=5)

        # qscore
        self.no_qscore = tk.BooleanVar(value=False)
        no_qscore_box = tk.Checkbutton(el, text='without quality score', variable=self.no_qscore)
        # packing

        test_frac_frame.pack(side='top',  padx=5, pady=20, anchor='w')
        test_frac_label.pack(side='left',  padx=5, anchor='w')
        test_frac_value.pack(side='left',   anchor='w')
        test_frac_info.pack(side='left', anchor='w')
        ttk.Separator(el, orient='horizontal').pack(side='top', fill='x', pady=5, padx=5, anchor='w')
        crossval_box.pack(side='top', padx=5, anchor='w')
        folds_frame.pack(side='top', padx=5, anchor='w')
        folds_label.pack(side='left', padx=5, anchor='w')
        folds_value.pack(side='left', anchor='w')
        ttk.Separator(el, orient='horizontal').pack(side='top', fill='x', pady=5, padx=5, anchor='w')

        ttk.Separator(el, orient='horizontal').pack(side='top', fill='x', pady=5, padx=5, anchor='w')
        no_qscore_box.pack(side='top',  padx=5, anchor='w')
        return el


    def _create_edge_path_el(self, parent):
        el = tk.Frame(parent)
        panel = tk.Frame(el)
        self.edge_path = tk.StringVar()
        edge_button = tk.Button(panel, text="select path ...", command=lambda: self.browse_edge_file())
        edge_label = tk.Entry(el, textvariable=self.edge_path)
        panel.pack(side='top', fill='x')
        tk.Label(panel, text="edge path:").pack(side='left', anchor='w',padx=5, pady=5)
        edge_button.pack(side='right', anchor='w',padx=5, pady=5)
        edge_label.pack( fill='x', padx=5, pady=5)
        return el

    def _create_tn_path_el(self, parent):
        el = tk.Frame(parent)
        panel = tk.Frame(el)
        self.tn_path = tk.StringVar()
        tn_button = tk.Button(panel, text="select path ...", command=lambda: self.browse_tn_file())
        tn_label = tk.Entry(el, textvariable=self.tn_path)
        panel.pack(side='top', fill='x')
        tk.Label(panel, text="true negative edge path:").pack(side='left', anchor='w',padx=5, pady=5)
        tn_button.pack(side='right', padx=5, pady=5)
        tn_label.pack(fill='x', padx=5, pady=5)
        return el

    def _create_nodes_path_el(self, parent):
        el = tk.Frame(parent)
        panel = tk.Frame(el)
        self.nodes_path = tk.StringVar()
        nodes_button = tk.Button(panel, text="select path ...", command=lambda: self.browse_nodes_file())
        nodes_label = tk.Entry(el, textvariable=self.nodes_path)
        panel.pack(side='top', fill='x')
        tk.Label(panel, text="nodes file path").pack(side='left', anchor='w',padx=5, pady=5)
        nodes_button.pack(side='right', anchor='w', padx=5, pady=5)
        nodes_label.pack(fill='x', padx=5, pady=5)
        return el

    def browse_edge_file(self):
        self.edge_path.set(filedialog.askopenfilename())

    def browse_tn_file(self):
        self.tn_path.set(filedialog.askopenfilename())

    def browse_nodes_file(self):
        self.nodes_path.set(filedialog.askopenfilename())

    def update(self):
        graph_files_folder = os.path.join(self.controller.ARGS_LIST_GLOBAL[1], gcConst.GRAPH_FILES_FOLDER_NAME)
        edge_path = os.path.join(graph_files_folder, 'edges.csv')
        if os.path.exists(edge_path) or 'GraphCreationFrame' in self.controller.selected_frames:
            self.edge_path.set(edge_path)
        tn_edge_path = os.path.join(graph_files_folder, 'TN_edges.csv')
        if os.path.exists(tn_edge_path) or 'GraphCreationFrame' in self.controller.selected_frames:
            self.tn_path.set(tn_edge_path)
        nodes_path = os.path.join(graph_files_folder, 'nodes.csv')
        if os.path.exists(nodes_path) or 'GraphCreationFrame' in self.controller.selected_frames:
            self.nodes_path.set(nodes_path)


    def next_page(self):
        self.controller.show_next_frame()



#################### EVALUATE VAL ############################

class EvalFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.info_text = ""
        titles_panel = tk.Frame(self)
        self.info = tk.Button(titles_panel, text=" ? ", command=lambda: show_info_box(self.info_text))
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


#################### CONFIRM VAL ############################

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
        self.for_all=False
        self.win = tk.Toplevel()
        message = 'The file %s already exists'%(file_path)
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
            self.for_all=False
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

#################### DISPLAY LOGGING IN GUI ############################

# """ source: #https://github.com/beenje/tkinter-logging-text-widget/blob/master/main.py """
import logging
import queue
from tkinter import ttk, N, S, E, W

logger = logging.getLogger()

class QueueHandler(logging.Handler):
    """Class to send logging records to a queue

    It can be used from different threads
    The ConsoleUi class polls this queue to display records in a ScrolledText widget
    """
    # Example from Moshe Kaplan: https://gist.github.com/moshekaplan/c425f861de7bbf28ef06
    # (https://stackoverflow.com/questions/13318742/python-logging-to-tkinter-text-widget) is not thread safe!
    # See https://stackoverflow.com/questions/43909849/tkinter-python-crashes-on-new-thread-trying-to-log-on-main-thread

    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(record)


class ConsoleUi:
    """Poll messages from a logging queue and display them in a scrolled text widget"""

    def __init__(self, frame):
        self.frame = frame
        # Create a ScrolledText wdiget
        self.scrolled_text = ScrolledText(frame, state='disabled', height=12)
        self.scrolled_text.grid(row=0, column=0, sticky=(N, S, W, E))
        self.scrolled_text.configure(font='TkFixedFont')
        self.scrolled_text.tag_config('INFO', foreground='black' )
        self.scrolled_text.tag_config('DEBUG', foreground='gray')
        self.scrolled_text.tag_config('WARNING', foreground='orange')
        self.scrolled_text.tag_config('ERROR', foreground='red')
        self.scrolled_text.tag_config('CRITICAL', foreground='red', underline=1)
        # Create a logging handler using a queue
        self.log_queue = queue.Queue()
        self.queue_handler = QueueHandler(self.log_queue)
        formatter = logging.Formatter('%(asctime)s: %(message)s')
        self.queue_handler.setFormatter(formatter)
        logger.addHandler(self.queue_handler)
        # Start polling messages from the queue
        self.frame.after(100, self.poll_log_queue)

    def display(self, record):
        msg = self.queue_handler.format(record)
        self.scrolled_text.configure(state='normal')
        self.scrolled_text.insert(tk.END, msg + '\n', record.levelname)
        self.scrolled_text.configure(state='disabled')
        # Autoscroll to the bottom
        self.scrolled_text.yview(tk.END)

    def poll_log_queue(self):
        # Check every 100ms if there is a new message in the queue to display
        while True:
            try:
                record = self.log_queue.get(block=False)
            except queue.Empty:
                break
            else:
                self.display(record)
        self.frame.after(100, self.poll_log_queue)


class ConsoleFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Create the panes and frames
        console_frame = ttk.Labelframe(self, text="Console")
        buttons_panel = tk.Frame(self)
        next_button = tk.Button(buttons_panel, text="Cancel", command=lambda: on_closing(), height=1, width=15)

        # Initialize all frames
        self.console = ConsoleUi(console_frame)
        console_frame.pack(side='top', fill='both', expand=True)

        ttk.Separator(self, orient='horizontal').pack(side='top', fill='x', pady=(15, 0), padx=10, anchor='s')
        buttons_panel.pack(side='bottom', padx=15, fill='x')
        next_button.pack(side='left', anchor='w', pady=(5, 10))

    #def quit(self, *args):
    #    self.root.destroy()

#################### MAIN GUI ############################

def on_closing():
    if messagebox.askokcancel("Quit", "Do you really want to quit?"):
        app.destroy()
        sys.exit()


def show_info_box(msg):
    if not bool(msg):
        msg='No info available'
    messagebox.showinfo('Info',msg)


def start_gui():

    global app
    app = BimegGui()

    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()
