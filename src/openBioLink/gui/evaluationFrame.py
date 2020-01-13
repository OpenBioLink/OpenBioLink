import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import openbiolink.evaluation.evalConfig as evalConst
import openbiolink.train_test_set_creation.ttsConfig as ttsConst
from openbiolink.evaluation.metricTypes import RankMetricType, ThresholdMetricType
from openbiolink.evaluation.models.modelTypes import ModelTypes
from openbiolink.gui import gui as gui


class EvalFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.info_text = ""

        # title
        titles_panel = tk.Frame(self)
        self.info = tk.Button(titles_panel, text=" help ", command=lambda: gui.show_info_box(self.info_text))
        self.title = tk.Label(titles_panel, text="(3) Testing and Evaluation", font=controller.title_font)

        self.actions_el = self._create_action_el(self)

        threshold_metrics = [ThresholdMetricType[item] for item in dir(ThresholdMetricType) if
                             not item.startswith("__")]

        options_panel = tk.Frame(self)
        paths_box = tk.LabelFrame(options_panel, text='file paths')
        self.config_path_el = self._create_config_path_el(paths_box)
        self.train_file_el = self._create_train_path_el(paths_box)
        self.test_file_el = self._create_test_path_el(paths_box)
        self.trained_model_file_el = self._create_trained_model_path_el(paths_box)
        self.node_or_corrupted_file_el = self._create_nodes_or_corrupted_path_el(paths_box)

        self.metrics_box = tk.LabelFrame(options_panel, text='choose metrics')
        self.metrics_frame = tk.Frame(self.metrics_box)
        self.rank_metrics_dict = {}
        self.threshold_metrics_dict = {}

        self.hits_at_k_el = self._create_hits_at_k_el(self.metrics_frame)
        self.mrr_el = self._create_mrr_el(self.metrics_frame)
        self.hits_at_k_el.pack(side='top', fill='x', pady=(10, 5))
        self.mrr_el.pack(side='top', fill='x', pady=5)
        ttk.Separator(self.metrics_frame, orient='horizontal').pack(side='top', fill='x', pady=10, padx=10, anchor='s')
        for metric in threshold_metrics:
            self.threshold_metrics_dict[metric] = tk.BooleanVar(value=True)
            cb = tk.Checkbutton(self.metrics_frame, text=metric.value, variable=self.threshold_metrics_dict[metric])
            cb.pack(anchor='w', padx=5, pady=5)

        self.buttons_panel = tk.Frame(self)
        self.next_button = tk.Button(self.buttons_panel, text="Next", command=lambda: self.next_page(), height=1,
                                     width=15)
        self.prev_button = tk.Button(self.buttons_panel, text="Back",
                                     command=lambda: self.controller.show_previous_frame(), height=1, width=15)

        # packing
        titles_panel.pack(side="top", fill="x", pady=10)
        self.title.pack(side='left', pady=10, padx=15)
        self.info.pack(side="right", fill="x", pady=5, padx=15)
        self.actions_el.pack(side='top', fill='both', padx=15, pady=5, expand=True)

        options_panel.pack(side='top', fill='both', padx=15, pady=5, expand=True)
        self.metrics_box.pack(side='left', fill='both', expand=True, padx=(0, 5))
        self.metrics_frame.pack(side='top', fill='both', expand=True)
        paths_box.pack(side='left', fill='both', expand=True, padx=(5, 0))
        self.config_path_el.pack(side='top', fill='x')
        self.pack_file_paths()
        self.node_or_corrupted_file_el.pack(side='top', fill='x')

        ttk.Separator(self, orient='horizontal').pack(side='top', fill='x', pady=(15, 1), padx=10, anchor='s')
        self.buttons_panel.pack(side='bottom', padx=15, fill='x')
        self.prev_button.pack(side='left', anchor='w', pady=(5, 10))
        self.next_button.pack(side='right', anchor='e', pady=(5, 10))

    def pack_file_paths(self):
        self.unpack_file_paths()
        if self.train.get():
            self.train_file_el.pack(side='top', fill='x')
        elif self.evaluate.get():
            self.trained_model_file_el.pack(side='top', fill='x')
        if self.evaluate.get():
            self.test_file_el.pack(side='top', fill='x')
            self.metrics_frame.pack(side='top', fill='both', expand=True)

        else:
            self.metrics_frame.pack_forget()
        if (self.hits.get() or self.mrr.get()) and self.evaluate.get():
            self.node_or_corrupted_file_el.pack(side='top', fill='x')

    def toggl_ranked_metrics(self):
        if not self.hits.get():
            self.rank_metrics_dict[RankMetricType.HITS_AT_K].set(False)
            self.rank_metrics_dict[RankMetricType.HITS_AT_K_UNFILTERED].set(False)
        if not self.mrr.get():
            self.rank_metrics_dict[RankMetricType.MRR].set(False)
            self.rank_metrics_dict[RankMetricType.MRR_UNFILTERED].set(False)

        self.pack_file_paths()

        if (self.hits.get() or self.mrr.get()) and self.evaluate.get():
            self.node_or_corrupted_file_el.pack(side='top', fill='x')

    def unpack_file_paths(self):
        self.train_file_el.pack_forget()
        self.trained_model_file_el.pack_forget()
        self.test_file_el.pack_forget()
        self.node_or_corrupted_file_el.pack_forget()

    def _create_action_el(self, parent):
        el = tk.LabelFrame(parent, text="general info")
        self.train = tk.BooleanVar(value=True)
        train_box = tk.Checkbutton(el, text='perform training', variable=self.train, command=self.pack_file_paths)
        self.evaluate = tk.BooleanVar(value=True)
        eval_box = tk.Checkbutton(el, text='perform evaluation', variable=self.evaluate, command=self.pack_file_paths)
        models = [ModelTypes[item].name for item in dir(ModelTypes) if
                  not item.startswith("__")]
        self.select_choices_models = models
        self.select_model = tk.StringVar()
        select_menu = tk.OptionMenu(el, self.select_model, *self.select_choices_models)
        select_menu.configure(width=20)
        train_box.pack(side='left', padx=5, anchor='w')
        eval_box.pack(side='left', padx=5, anchor='w')
        # ttk.Separator(el, orient='vertical').pack(side='left', fill='y', padx=10, anchor='w')
        select_menu.pack(side='right', padx=(5, 15), anchor='w')

        tk.Label(el, text='model:').pack(side='right')
        return el

    def _create_hits_at_k_el(self, parent):
        el = tk.Frame(parent)
        panel = tk.Frame(el)
        self.hits = tk.BooleanVar(value=True)
        self.ks = tk.StringVar(value=str(evalConst.DEFAULT_HITS_AT_K))
        self.rank_metrics_dict[RankMetricType.HITS_AT_K] = tk.BooleanVar(value=True)
        self.rank_metrics_dict[RankMetricType.HITS_AT_K_UNFILTERED] = tk.BooleanVar(value=True)
        hits_cb = tk.Checkbutton(panel, text='hits@K', variable=self.hits, command=self.toggl_ranked_metrics)
        ks_entry = tk.Entry(panel, textvariable=self.ks)
        hits_filtered_cb = tk.Checkbutton(panel, text='filtered',
                                          variable=self.rank_metrics_dict[RankMetricType.HITS_AT_K])
        hits_unfiltered_cb = tk.Checkbutton(panel, text='unfiltered',
                                            variable=self.rank_metrics_dict[RankMetricType.HITS_AT_K_UNFILTERED])
        panel.pack(side='top', fill='x', padx=5)
        hits_cb.pack(side='left')
        hits_filtered_cb.pack(side='right')
        hits_unfiltered_cb.pack(side='right')
        ks_entry.pack(side='right')
        tk.Label(panel, text='K\'s:').pack(side='right')
        return el

    def _create_mrr_el(self, parent):
        el = tk.Frame(parent)
        panel = tk.Frame(el)
        self.mrr = tk.BooleanVar(value=True)
        self.rank_metrics_dict[RankMetricType.MRR] = tk.BooleanVar(value=True)
        self.rank_metrics_dict[RankMetricType.MRR_UNFILTERED] = tk.BooleanVar(value=True)
        mrr_cb = tk.Checkbutton(panel, text='MRR', variable=self.mrr,
                                command=self.toggl_ranked_metrics)
        mrr_filtered_cb = tk.Checkbutton(panel, text='filtered',
                                         variable=self.rank_metrics_dict[RankMetricType.MRR])
        mrr_unfiltered_cb = tk.Checkbutton(panel, text='unfiltered',
                                           variable=self.rank_metrics_dict[RankMetricType.MRR_UNFILTERED])
        panel.pack(side='top', fill='x', padx=5)
        mrr_cb.pack(side='left')
        mrr_filtered_cb.pack(side='right')
        mrr_unfiltered_cb.pack(side='right')
        return el

    def _create_config_path_el(self, parent):
        el = tk.Frame(parent)
        panel = tk.Frame(el)
        self.config_path = tk.StringVar()
        button = tk.Button(panel, text="select path ...", command=lambda: self.browse_config_file())
        label = tk.Entry(el, textvariable=self.config_path)
        panel.pack(side='top', fill='x')
        tk.Label(panel, text="model config path:").pack(side='left', anchor='w', padx=5, pady=5)
        button.pack(side='right', anchor='w', padx=5, pady=5)
        label.pack(fill='x', padx=5, pady=5)
        return el

    def _create_train_path_el(self, parent):
        el = tk.Frame(parent)
        panel = tk.Frame(el)
        self.train_path = tk.StringVar()
        train_button = tk.Button(panel, text="select path ...", command=lambda: self.browse_train_file())
        train_label = tk.Entry(el, textvariable=self.train_path)
        panel.pack(side='top', fill='x')
        tk.Label(panel, text="training set path:").pack(side='left', anchor='w', padx=5, pady=5)
        train_button.pack(side='right', anchor='w', padx=5, pady=5)
        train_label.pack(fill='x', padx=5, pady=5)
        return el

    def _create_test_path_el(self, parent):
        el = tk.Frame(parent)
        panel = tk.Frame(el)
        self.test_path = tk.StringVar()
        test_button = tk.Button(panel, text="select path ...", command=lambda: self.browse_test_file())
        test_label = tk.Entry(el, textvariable=self.test_path)
        panel.pack(side='top', fill='x')
        tk.Label(panel, text="test set path:").pack(side='left', anchor='w', padx=5, pady=5)
        test_button.pack(side='right', anchor='w', padx=5, pady=5)
        test_label.pack(fill='x', padx=5, pady=5)
        return el

    def _create_trained_model_path_el(self, parent):
        el = tk.Frame(parent)
        panel = tk.Frame(el)
        self.trained_model_path = tk.StringVar()
        button = tk.Button(panel, text="select path ...", command=lambda: self.browse_trained_model())
        label = tk.Entry(el, textvariable=self.trained_model_path)
        panel.pack(side='top', fill='x')
        tk.Label(panel, text="trained model path:").pack(side='left', anchor='w', padx=5, pady=5)
        button.pack(side='right', anchor='w', padx=5, pady=5)
        label.pack(fill='x', padx=5, pady=5)
        return el

    def _create_nodes_or_corrupted_path_el(self, parent):
        el = tk.Frame(parent)
        panel = tk.Frame(el)
        self.nodes_or_corr_path = tk.StringVar()
        button = tk.Button(panel, text="select path ...", command=lambda: self.browse_nodes_or_corr_file())
        self.select_choices_node_corrupted = ['nodes path', 'corrupted triples path']
        self.select_node_corrupted = tk.StringVar(value=self.select_choices_node_corrupted[0])
        select_menu = tk.OptionMenu(panel, self.select_node_corrupted, *self.select_choices_node_corrupted)

        select_menu.configure(width=20)
        label = tk.Entry(el, textvariable=self.nodes_or_corr_path)
        panel.pack(side='top', fill='x')
        select_menu.pack(side='left', anchor='w', padx=5, pady=5)
        button.pack(side='right', anchor='w', padx=5, pady=5)
        label.pack(fill='x', padx=5, pady=5)
        return el

    def browse_test_file(self):
        self.test_path.set(filedialog.askopenfilename())

    def browse_train_file(self):
        self.train_path.set(filedialog.askopenfilename())

    def browse_trained_model(self):
        self.trained_model_path.set(filedialog.askopenfilename())

    def browse_nodes_or_corr_file(self):
        self.nodes_or_corr_path.set(filedialog.askopenfilename())

    def browse_config_file(self):
        self.config_path.set(filedialog.askopenfilename())

    def update(self):
        # fixme check if graph creation action is performed
        tts_files_folder = os.path.join(self.controller.ARGS_LIST_GLOBAL[1], ttsConst.TTS_FOLDER_NAME)
        test_path = os.path.join(tts_files_folder, ttsConst.TEST_FILE_NAME)
        if os.path.exists(test_path) or 'SplitFrame' in self.controller.selected_frames:
            self.test_path.set(test_path)

        train_path = os.path.join(tts_files_folder, ttsConst.TRAIN_FILE_NAME)
        if os.path.exists(train_path) or 'SplitFrame' in self.controller.selected_frames:
            self.train_path.set(train_path)

        nodes_path = os.path.join(tts_files_folder, ttsConst.TRAIN_VAL_NODES_FILE_NAME)
        if os.path.exists(nodes_path) or 'GraphCreationFrame' in self.controller.selected_frames:
            self.nodes_or_corr_path.set(nodes_path)

    def next_page(self):
        if not self.train.get() and not self.evaluate.get():
            messagebox.showerror('ERROR', 'at least one action (training, evaluation) must be chosen')
            return
        if not self.select_model.get():
            messagebox.showerror('ERROR', 'Please select a model')
            return
        if self.train.get():
            if not self.train_path.get():
                messagebox.showerror('ERROR', 'For training, please select a training set path')
                return
        if self.evaluate.get():
            if not self.train.get() and not self.trained_model_path.get():
                messagebox.showerror('ERROR',
                                     'Please either provide a path to your trained model or choose \'perform training')
                return
            if not self.test_path.get():
                messagebox.showerror('ERROR', 'Please provide a trainings path')
                return
            if (self.hits.get() or self.mrr.get()) and not self.nodes_or_corr_path.get():
                messagebox.showerror('ERROR',
                                     'Ranked metrics (his@K, MRR) require either a nodes file or a file of corrupted triples')
                return
            if all([not self.mrr.get(), not self.hits.get()]) \
                    and all([not x.get() for _, x in self.threshold_metrics_dict.items()]):
                messagebox.showerror('ERROR',
                                     '\'Perform evaluation\' is chosen, but no evaluation metrics are selected')
                return
        self.controller.ARGS_LIST_EVAL = []
        self.controller.ARGS_LIST_EVAL.append('-e')
        self.controller.ARGS_LIST_EVAL.extend(['--model_cls', str(ModelTypes[self.select_model.get()].name)])
        if self.config_path.get():
            self.controller.ARGS_LIST_EVAL.extend(['--config', self.config_path.get()])
        if not self.train.get():
            self.controller.ARGS_LIST_EVAL.append('--no_train')
            self.controller.ARGS_LIST_EVAL.extend(['--trained_model', self.trained_model_path.get()])
        else:
            self.controller.ARGS_LIST_EVAL.extend(['--train', self.train_path.get()])
        if not self.evaluate.get():
            self.controller.ARGS_LIST_EVAL.append('--no_eval')
        else:
            self.controller.ARGS_LIST_EVAL.extend(['--test', self.test_path.get()])
            ranked_metrics = [x.name for x, y in self.rank_metrics_dict.items() if y.get()]
            threshold_metrics = [x.name for x, y in self.threshold_metrics_dict.items() if y.get()]
            self.controller.ARGS_LIST_EVAL.append('--metrics')
            self.controller.ARGS_LIST_EVAL.extend(ranked_metrics)
            self.controller.ARGS_LIST_EVAL.extend(threshold_metrics)
            if RankMetricType.HITS_AT_K in self.rank_metrics_dict.keys() or RankMetricType.HITS_AT_K_UNFILTERED in self.rank_metrics_dict.keys():
                self.controller.ARGS_LIST_EVAL.append('--ks')
                import ast
                self.controller.ARGS_LIST_EVAL.extend([str(x) for x in ast.literal_eval(self.ks.get())])
            # if metrics
            if self.select_node_corrupted.get() == 'nodes path':
                self.controller.ARGS_LIST_EVAL.extend(['--eval_nodes', self.nodes_or_corr_path.get()])
            elif self.select_node_corrupted.get() == 'corrupted triples path':
                self.controller.ARGS_LIST_EVAL.extend(['--corrupted', self.nodes_or_corr_path.get()])

        self.controller.show_next_frame()
