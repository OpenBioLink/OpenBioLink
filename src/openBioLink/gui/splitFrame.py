import os
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

from openbiolink.graph_creation import graphCreationConfig as gcConst
from openbiolink.gui import gui as gui


class SplitFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.info_text = ""
        titles_panel = tk.Frame(self)
        self.info = tk.Button(titles_panel, text=" help ", command=lambda: gui.show_info_box(self.info_text))
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
        self.time_box_el = self._create_time_options_el(self.right_time_box)

        self.buttons_panel = tk.Frame(self)
        self.next_button = tk.Button(self.buttons_panel, text="Next", command=lambda: self.next_page(), height=1,
                                     width=15)
        self.prev_button = tk.Button(self.buttons_panel, text="Back",
                                     command=lambda: self.controller.show_previous_frame(), height=1, width=15)

        # packing
        titles_panel.pack(side="top", fill="x", pady=10)
        self.title.pack(side='left', pady=10, padx=15)
        self.info.pack(side="right", fill="x", pady=5, padx=15)
        self.mode_panel.pack(side='top', fill='both', padx=15, expand=True)
        self.option_panel.pack(side='top', fill='both', padx=15, pady=10, expand=True)
        self.left_box.pack(side='left', fill='both', expand=True)
        self.file_edge_el.pack(side='top', fill='both', padx=15, pady=10, expand=True)
        self.file_tn_el.pack(side='top', fill='both', padx=15, pady=10, expand=True)
        self.file_nodes_el.pack(side='top', fill='both', padx=15, pady=10, expand=True)
        self.right_box.pack(side='left', fill='both', expand=True)
        self.right_rand_box.pack(fill='both', expand=True, padx=(10, 0))
        self.rand_box_el.pack(fill='both', expand=True)

        ttk.Separator(self, orient='horizontal').pack(side='top', fill='x', pady=(15, 0), padx=10, anchor='s')
        self.buttons_panel.pack(side='bottom', padx=15, fill='x')
        self.prev_button.pack(side='left', anchor='w', pady=(5, 10))
        self.next_button.pack(side='right', anchor='e', pady=(5, 10))

    def _create_mode_element(self, parent):
        el = tk.LabelFrame(parent, text="Split Mode")
        self.mode = tk.StringVar(value='rand')
        random_box = tk.Radiobutton(el, text='random split', variable=self.mode, value='rand',
                                    command=self.toggl_tts_elements)
        time_box = tk.Radiobutton(el, text='time slice', variable=self.mode, value='time',
                                  command=self.toggl_tts_elements)
        random_box.pack(side='left', padx=5, anchor='w')
        time_box.pack(side='left', padx=5, anchor='w')
        return el

    def toggl_tts_elements(self):
        if self.mode.get() == 'time':
            self.right_rand_box.pack_forget()
            self.rand_box_el.pack_forget()
            self.right_time_box.pack(fill='both', expand=True, padx=(10, 0))
            self.time_box_el.pack(fill='both', expand=True)
        elif self.mode.get() == 'rand':
            self.right_rand_box.pack(fill='both', expand=True, padx=(10, 0))
            self.rand_box_el.pack(fill='both', expand=True)
            self.right_time_box.pack_forget()
            self.time_box_el.pack_forget()

    def _create_time_options_el(self, parent):
        el = tk.Frame(parent)
        file_edge_el = self._create_tmo_edge_path_el(el)
        file_tn_el = self._create_tmo_tn_path_el(el)
        file_nodes_el = self._create_tmo_nodes_path_el(el)
        file_edge_el.pack(side='top', fill='both', padx=15, pady=10, expand=True)
        file_tn_el.pack(side='top', fill='both', padx=15, pady=10, expand=True)
        file_nodes_el.pack(side='top', fill='both', padx=15, pady=10, expand=True)
        return el

    def _create_rand_options_el(self, parent):
        el = tk.Frame(parent)

        # test frac
        self.test_frac = tk.StringVar(value='0.2')
        test_frac_frame = tk.Frame(el)
        test_frac_label = tk.Label(test_frac_frame, text='test set fraction:')
        test_frac_value = tk.Entry(test_frac_frame, textvariable=self.test_frac, width=5)
        test_frac_info = tk.Label(test_frac_frame, text='as float, e.g. 0.2', font=self.controller.info_font)

        # cross val
        self.crossval = tk.BooleanVar(value=False)
        crossval_box = tk.Checkbutton(el, text='cross validation', variable=self.crossval)
        self.folds = tk.StringVar(value='5')
        folds_frame = tk.Frame(el)
        folds_label = tk.Label(folds_frame, text='folds / validation set fraction:')
        folds_value = tk.Entry(folds_frame, textvariable=self.folds, width=5)
        folds_info = tk.Label(folds_frame, text='folds as int\n validation fraction as float',
                              font=self.controller.info_font)

        # packing
        test_frac_frame.pack(side='top', padx=5, pady=20, anchor='w')
        test_frac_label.pack(side='left', padx=5, anchor='w')
        test_frac_value.pack(side='left', anchor='w')
        test_frac_info.pack(side='left', anchor='w')
        ttk.Separator(el, orient='horizontal').pack(side='top', fill='x', pady=5, padx=5, anchor='w')
        crossval_box.pack(side='top', padx=5, anchor='w')
        folds_frame.pack(side='top', padx=5, anchor='w')
        folds_label.pack(side='left', padx=5, anchor='w')
        folds_value.pack(side='left', anchor='w')
        folds_info.pack(side='left', anchor='w')
        return el

    # todo style: 6 times same function
    def _create_edge_path_el(self, parent):
        el = tk.Frame(parent)
        panel = tk.Frame(el)
        self.edge_path = tk.StringVar()
        edge_button = tk.Button(panel, text="select path ...", command=lambda: self.browse_edge_file())
        edge_label = tk.Entry(el, textvariable=self.edge_path)
        panel.pack(side='top', fill='x')
        tk.Label(panel, text="edge path:").pack(side='left', anchor='w', padx=5, pady=5)
        edge_button.pack(side='right', anchor='w', padx=5, pady=5)
        edge_label.pack(fill='x', padx=5, pady=5)
        return el

    def _create_tn_path_el(self, parent):
        el = tk.Frame(parent)
        panel = tk.Frame(el)
        self.tn_path = tk.StringVar()
        tn_button = tk.Button(panel, text="select path ...", command=lambda: self.browse_tn_file())
        tn_label = tk.Entry(el, textvariable=self.tn_path)
        panel.pack(side='top', fill='x')
        tk.Label(panel, text="true negative edge path:").pack(side='left', anchor='w', padx=5, pady=5)
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
        tk.Label(panel, text="nodes file path").pack(side='left', anchor='w', padx=5, pady=5)
        nodes_button.pack(side='right', anchor='w', padx=5, pady=5)
        nodes_label.pack(fill='x', padx=5, pady=5)
        return el

    def _create_tmo_edge_path_el(self, parent):
        el = tk.Frame(parent)
        panel = tk.Frame(el)
        self.tmo_edge_path = tk.StringVar()
        edge_button = tk.Button(panel, text="select path ...", command=lambda: self.browse_tmo_edge_file())
        edge_label = tk.Entry(el, textvariable=self.tmo_edge_path)
        panel.pack(side='top', fill='x')
        tk.Label(panel, text="edge path:").pack(side='left', anchor='w', padx=5, pady=5)
        edge_button.pack(side='right', anchor='w', padx=5, pady=5)
        edge_label.pack(fill='x', padx=5, pady=5)
        return el

    def _create_tmo_tn_path_el(self, parent):
        el = tk.Frame(parent)
        panel = tk.Frame(el)
        self.tmo_tn_path = tk.StringVar()
        tn_button = tk.Button(panel, text="select path ...", command=lambda: self.browse_tmo_tn_file())
        tn_label = tk.Entry(el, textvariable=self.tmo_tn_path)
        panel.pack(side='top', fill='x')
        tk.Label(panel, text="true negative edge path:").pack(side='left', anchor='w', padx=5, pady=5)
        tn_button.pack(side='right', padx=5, pady=5)
        tn_label.pack(fill='x', padx=5, pady=5)
        return el

    def _create_tmo_nodes_path_el(self, parent):
        el = tk.Frame(parent)
        panel = tk.Frame(el)
        self.tmo_nodes_path = tk.StringVar()
        nodes_button = tk.Button(panel, text="select path ...", command=lambda: self.browse_tmo_nodes_file())
        nodes_label = tk.Entry(el, textvariable=self.tmo_nodes_path)
        panel.pack(side='top', fill='x')
        tk.Label(panel, text="nodes file path").pack(side='left', anchor='w', padx=5, pady=5)
        nodes_button.pack(side='right', anchor='w', padx=5, pady=5)
        nodes_label.pack(fill='x', padx=5, pady=5)
        return el

    def browse_edge_file(self):
        self.edge_path.set(filedialog.askopenfilename())

    def browse_tn_file(self):
        self.tn_path.set(filedialog.askopenfilename())

    def browse_nodes_file(self):
        self.nodes_path.set(filedialog.askopenfilename())

    def browse_tmo_edge_file(self):
        self.tmo_edge_path.set(filedialog.askopenfilename())

    def browse_tmo_tn_file(self):
        self.tmo_tn_path.set(filedialog.askopenfilename())

    def browse_tmo_nodes_file(self):
        self.tmo_nodes_path.set(filedialog.askopenfilename())

    def update(self):
        # fixme check if graph creation action is performed
        graph_files_folder = os.path.join(self.controller.ARGS_LIST_GLOBAL[1], gcConst.GRAPH_FILES_FOLDER_NAME)
        edge_path = os.path.join(graph_files_folder, 'edges.csv')
        if os.path.exists(edge_path) or 'GraphCreationFrame' in self.controller.selected_frames:
            self.edge_path.set(edge_path)
        tn_edge_path = os.path.join(graph_files_folder, 'TN_edges.csv')
        if os.path.exists(tn_edge_path) or 'GraphCreationFrame' in self.controller.selected_frames:
            self.tn_path.set(tn_edge_path)
        nodes_path = os.path.join(graph_files_folder, 'ALL_nodes.csv')
        if os.path.exists(nodes_path) or 'GraphCreationFrame' in self.controller.selected_frames:
            self.nodes_path.set(nodes_path)

    def next_page(self):
        self.controller.ARGS_LIST_TRAIN_TEST_SPLIT = []
        self.controller.ARGS_LIST_TRAIN_TEST_SPLIT.append('-s')
        self.controller.ARGS_LIST_TRAIN_TEST_SPLIT.extend(['--edges', self.edge_path.get()])
        self.controller.ARGS_LIST_TRAIN_TEST_SPLIT.extend(['--tn_edges', self.tn_path.get()])
        self.controller.ARGS_LIST_TRAIN_TEST_SPLIT.extend(['--nodes', self.nodes_path.get()])

        if self.mode.get() == 'time':
            if (self.tmo_edge_path.get() == "") or (self.tmo_tn_path.get() == '') or (self.tmo_nodes_path.get() == ""):
                messagebox.showerror('ERROR', 'Please provide all three t-minus one paths.')
                return
            self.controller.ARGS_LIST_TRAIN_TEST_SPLIT.extend(['--mode', 'time'])
            self.controller.ARGS_LIST_TRAIN_TEST_SPLIT.extend(['--tmo_edges', self.tmo_edge_path.get()])
            self.controller.ARGS_LIST_TRAIN_TEST_SPLIT.extend(['--tmo_tn_edges', self.tmo_tn_path.get()])
            self.controller.ARGS_LIST_TRAIN_TEST_SPLIT.extend(['--tmo_nodes', self.tmo_nodes_path.get()])

        elif self.mode.get() == 'rand':
            if self.test_frac.get() == '':
                messagebox.showerror('ERROR', 'Please provide a test set fraction.')
                return
            self.controller.ARGS_LIST_TRAIN_TEST_SPLIT.extend(['--mode', 'rand'])
            self.controller.ARGS_LIST_TRAIN_TEST_SPLIT.extend(['--test_frac', self.test_frac.get()])

            if self.crossval.get():
                self.controller.ARGS_LIST_TRAIN_TEST_SPLIT.append('--crossval')  # todo crossval
                self.controller.ARGS_LIST_TRAIN_TEST_SPLIT.extend(['--val', self.folds.get()])

        self.controller.show_next_frame()
