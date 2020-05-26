import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import openbiolink.evaluation.evalConfig as evalConst
import openbiolink.train_test_set_creation.ttsConfig as ttsConst
from openbiolink.evaluation.metricTypes import RankMetricType, ThresholdMetricType
from openbiolink.evaluation.embedded.models.modelTypes import ModelTypes as EmbeddedModelTypes
from openbiolink.evaluation.symbolic.models.modelTypes import ModelTypes as SymbolicModelTypes
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

        threshold_metrics = [
            ThresholdMetricType[item] for item in dir(ThresholdMetricType) if not item.startswith("__")
        ]

        options_panel = tk.Frame(self)
        paths_box = tk.LabelFrame(options_panel, text="file paths")
        self.config_path_el = self._create_config_path_el(paths_box)
        self.train_file_el = self._create_train_path_el(paths_box)
        self.neg_train_file_el = self._create_neg_train_path_el(paths_box)
        self.test_file_el = self._create_test_path_el(paths_box)
        self.neg_test_file_el = self._create_neg_test_path_el(paths_box)
        self.trained_model_file_el = self._create_trained_model_path_el(paths_box)
        self.node_or_corrupted_file_el = self._create_nodes_or_corrupted_path_el(paths_box)

        self.select_model = None
        self.snapshot_at = tk.StringVar(value="100")
        self.valid_file_el = self._create_valid_path_el(paths_box)
        self.anyburl_learn_el = self._create_anyburl_learn_el(paths_box)
        self.anyburl_eval_el = self._create_anyburl_eval_el(paths_box)

        self.metrics_box = tk.LabelFrame(options_panel, text="choose metrics")
        self.metrics_frame = tk.Frame(self.metrics_box)
        self.rank_metrics_dict = {}
        self.threshold_metrics_dict = {}

        self.hits_at_k_el = self._create_hits_at_k_el(self.metrics_frame)
        self.mrr_el = self._create_mrr_el(self.metrics_frame)
        self.hits_at_k_el.pack(side="top", fill="x", pady=(10, 5))
        self.mrr_el.pack(side="top", fill="x", pady=5)
        ttk.Separator(self.metrics_frame, orient="horizontal").pack(side="top", fill="x", pady=10, padx=10, anchor="s")
        for metric in threshold_metrics:
            self.threshold_metrics_dict[metric] = tk.BooleanVar(value=True)
            cb = tk.Checkbutton(self.metrics_frame, text=metric.value, variable=self.threshold_metrics_dict[metric])
            cb.pack(anchor="w", padx=5, pady=5)

        self.buttons_panel = tk.Frame(self)
        self.next_button = tk.Button(
            self.buttons_panel, text="Next", command=lambda: self.next_page(), height=1, width=15
        )
        self.prev_button = tk.Button(
            self.buttons_panel, text="Back", command=lambda: self.controller.show_previous_frame(), height=1, width=15
        )

        # packing
        titles_panel.pack(side="top", fill="x", pady=10)
        self.title.pack(side="left", pady=10, padx=15)
        self.info.pack(side="right", fill="x", pady=5, padx=15)
        self.actions_el.pack(side="top", fill="both", padx=15, pady=5, expand=True)

        options_panel.pack(side="top", fill="both", padx=15, pady=5, expand=True)
        self.metrics_box.pack(side="left", fill="both", expand=True, padx=(0, 5))
        self.metrics_frame.pack(side="top", fill="both", expand=True)
        paths_box.pack(side="left", fill="both", expand=True, padx=(5, 0))
        self.config_path_el.pack(side="top", fill="x")
        self.pack_file_paths()
        self.node_or_corrupted_file_el.pack(side="top", fill="x")

        ttk.Separator(self, orient="horizontal").pack(side="top", fill="x", pady=(15, 1), padx=10, anchor="s")
        self.buttons_panel.pack(side="bottom", padx=15, fill="x")
        self.prev_button.pack(side="left", anchor="w", pady=(5, 10))
        self.next_button.pack(side="right", anchor="e", pady=(5, 10))

    def pack_file_paths(self):
        self.unpack_file_paths()
        if self.method.get() == "embedded":
            self.config_path_el.pack(side="top", fill="x")
            if self.train.get():
                self.train_file_el.pack(side="top", fill="x")
                self.neg_train_file_el.pack(side="top", fill="x")
            elif self.evaluate.get():
                self.trained_model_file_el.pack(side="top", fill="x")
            if self.evaluate.get():
                self.test_file_el.pack(side="top", fill="x")
                self.neg_test_file_el.pack(side="top", fill="x")
                self.metrics_frame.pack(side="top", fill="both", expand=True)
            else:
                self.metrics_frame.pack_forget()
            if (self.hits.get() or self.mrr.get()) and self.evaluate.get():
                self.node_or_corrupted_file_el.pack(side="top", fill="x")
        else:
            self.train_file_el.pack(side="top", fill="x")
            self.test_file_el.pack(side="top", fill="x")
            self.valid_file_el.pack(side="top", fill="x")
            if self.train.get():
                self.anyburl_learn_el.pack(side="top", fill="x")
            if self.evaluate.get():
                self.anyburl_eval_el.pack(side="top", fill="x")
                self.metrics_frame.pack(side="top", fill="both", expand=True)

    def toggl_ranked_metrics(self):
        if not self.hits.get():
            self.rank_metrics_dict[RankMetricType.HITS_AT_K].set(False)
            self.rank_metrics_dict[RankMetricType.HITS_AT_K_UNFILTERED].set(False)
        if not self.mrr.get():
            self.rank_metrics_dict[RankMetricType.MRR].set(False)
            self.rank_metrics_dict[RankMetricType.MRR_UNFILTERED].set(False)

        self.pack_file_paths()

        if (self.hits.get() or self.mrr.get()) and self.evaluate.get():
            self.node_or_corrupted_file_el.pack(side="top", fill="x")

    def unpack_file_paths(self):
        self.train_file_el.pack_forget()
        self.neg_train_file_el.pack_forget()
        self.trained_model_file_el.pack_forget()
        self.test_file_el.pack_forget()
        self.neg_test_file_el.pack_forget()
        self.valid_file_el.pack_forget()
        self.node_or_corrupted_file_el.pack_forget()
        self.anyburl_learn_el.pack_forget()
        self.anyburl_eval_el.pack_forget()
        self.config_path_el.pack_forget()

    def _create_action_el(self, parent):
        el = tk.LabelFrame(parent, text="general info")
        self.train = tk.BooleanVar(value=True)
        train_box = tk.Checkbutton(el, text="perform training", variable=self.train, command=self.pack_file_paths)
        self.evaluate = tk.BooleanVar(value=True)
        eval_box = tk.Checkbutton(el, text="perform evaluation", variable=self.evaluate, command=self.pack_file_paths)

        model_label = tk.Label(el, text="model:")

        method_choices = {"embedded", "symbolic"}
        self.method = tk.StringVar()
        self.method.set("embedded")
        method_menu = tk.OptionMenu(el, self.method, *method_choices)
        self.model_menu = None

        def pack_action(*args):
            if self.model_menu is not None:
                unpack_action()
                self.pack_file_paths()
            if self.method.get() == "embedded":
                models = [EmbeddedModelTypes[item].name for item in dir(EmbeddedModelTypes) if
                          not item.startswith("__")]
            else:
                models = [SymbolicModelTypes[item].name for item in dir(SymbolicModelTypes) if
                          not item.startswith("__")]
            self.select_choices_models = models
            self.select_model = tk.StringVar()
            self.model_menu = tk.OptionMenu(el, self.select_model, *self.select_choices_models)
            self.model_menu.configure(width=20)
            train_box.pack(side="left", padx=5, anchor="w")
            eval_box.pack(side="left", padx=5, anchor="w")
            self.model_menu.pack(side="right", padx=(5, 15), anchor="w")
            model_label.pack(side="right")
            method_menu.pack(side="right", padx=5, anchor="w")

        def unpack_action():
            train_box.pack_forget()
            eval_box.pack_forget()
            method_menu.pack_forget()
            self.model_menu.pack_forget()
            model_label.pack_forget()

        self.method.trace("w", pack_action)
        pack_action()

        # ttk.Separator(el, orient='vertical').pack(side='left', fill='y', padx=10, anchor='w')

        return el

    def _create_hits_at_k_el(self, parent):
        el = tk.Frame(parent)
        panel = tk.Frame(el)
        self.hits = tk.BooleanVar(value=True)
        self.ks = tk.StringVar(value=str(evalConst.DEFAULT_HITS_AT_K))
        self.rank_metrics_dict[RankMetricType.HITS_AT_K] = tk.BooleanVar(value=True)
        self.rank_metrics_dict[RankMetricType.HITS_AT_K_UNFILTERED] = tk.BooleanVar(value=True)
        hits_cb = tk.Checkbutton(panel, text="hits@K", variable=self.hits, command=self.toggl_ranked_metrics)
        ks_entry = tk.Entry(panel, textvariable=self.ks)
        hits_filtered_cb = tk.Checkbutton(
            panel, text="filtered", variable=self.rank_metrics_dict[RankMetricType.HITS_AT_K]
        )
        hits_unfiltered_cb = tk.Checkbutton(
            panel, text="unfiltered", variable=self.rank_metrics_dict[RankMetricType.HITS_AT_K_UNFILTERED]
        )
        panel.pack(side="top", fill="x", padx=5)
        hits_cb.pack(side="left")
        hits_filtered_cb.pack(side="right")
        hits_unfiltered_cb.pack(side="right")
        ks_entry.pack(side="right")
        tk.Label(panel, text="K's:").pack(side="right")
        return el

    def _create_mrr_el(self, parent):
        el = tk.Frame(parent)
        panel = tk.Frame(el)
        self.mrr = tk.BooleanVar(value=True)
        self.rank_metrics_dict[RankMetricType.MRR] = tk.BooleanVar(value=True)
        self.rank_metrics_dict[RankMetricType.MRR_UNFILTERED] = tk.BooleanVar(value=True)
        mrr_cb = tk.Checkbutton(panel, text="MRR", variable=self.mrr, command=self.toggl_ranked_metrics)
        mrr_filtered_cb = tk.Checkbutton(panel, text="filtered", variable=self.rank_metrics_dict[RankMetricType.MRR])
        mrr_unfiltered_cb = tk.Checkbutton(
            panel, text="unfiltered", variable=self.rank_metrics_dict[RankMetricType.MRR_UNFILTERED]
        )
        panel.pack(side="top", fill="x", padx=5)
        mrr_cb.pack(side="left")
        mrr_filtered_cb.pack(side="right")
        mrr_unfiltered_cb.pack(side="right")
        return el

    def _create_config_path_el(self, parent):
        el = tk.Frame(parent)
        panel = tk.Frame(el)
        self.config_path = tk.StringVar()
        button = tk.Button(panel, text="select path ...", command=lambda: self.browse_config_file())
        label = tk.Entry(el, textvariable=self.config_path)
        panel.pack(side="top", fill="x")
        tk.Label(panel, text="model config path:").pack(side="left", anchor="w", padx=5, pady=5)
        button.pack(side="right", anchor="w", padx=5, pady=5)
        label.pack(fill="x", padx=5, pady=5)
        return el

    def _create_train_path_el(self, parent):
        el = tk.Frame(parent)
        panel = tk.Frame(el)
        self.train_path = tk.StringVar()
        train_button = tk.Button(panel, text="select path ...", command=lambda: self.browse_train_file())
        train_label = tk.Entry(el, textvariable=self.train_path)
        panel.pack(side="top", fill="x")
        tk.Label(panel, text="training set path:").pack(side="left", anchor="w", padx=5, pady=5)
        train_button.pack(side="right", anchor="w", padx=5, pady=5)
        train_label.pack(fill="x", padx=5, pady=5)
        return el

    def _create_neg_train_path_el(self, parent):
        el = tk.Frame(parent)
        panel = tk.Frame(el)
        self.neg_train_path = tk.StringVar()
        train_button = tk.Button(panel, text="select path ...", command=lambda: self.browse_neg_train_file())
        train_label = tk.Entry(el, textvariable=self.neg_train_path)
        panel.pack(side="top", fill="x")
        tk.Label(panel, text="negative training set path:").pack(side="left", anchor="w", padx=5, pady=5)
        train_button.pack(side="right", anchor="w", padx=5, pady=5)
        train_label.pack(fill="x", padx=5, pady=5)
        return el

    def _create_test_path_el(self, parent):
        el = tk.Frame(parent)
        panel = tk.Frame(el)
        self.test_path = tk.StringVar()
        test_button = tk.Button(panel, text="select path ...", command=lambda: self.browse_test_file())
        test_label = tk.Entry(el, textvariable=self.test_path)
        panel.pack(side="top", fill="x")
        tk.Label(panel, text="test set path:").pack(side="left", anchor="w", padx=5, pady=5)
        test_button.pack(side="right", anchor="w", padx=5, pady=5)
        test_label.pack(fill="x", padx=5, pady=5)
        return el

    def _create_neg_test_path_el(self, parent):
        el = tk.Frame(parent)
        panel = tk.Frame(el)
        self.neg_test_path = tk.StringVar()
        test_button = tk.Button(panel, text="select path ...", command=lambda: self.browse_neg_test_file())
        test_label = tk.Entry(el, textvariable=self.neg_test_path)
        panel.pack(side="top", fill="x")
        tk.Label(panel, text="negative test set path:").pack(side="left", anchor="w", padx=5, pady=5)
        test_button.pack(side="right", anchor="w", padx=5, pady=5)
        test_label.pack(fill="x", padx=5, pady=5)
        return el

    def _create_valid_path_el(self, parent):
        el = tk.Frame(parent)
        panel = tk.Frame(el)
        self.val_path = tk.StringVar()
        test_button = tk.Button(panel, text="select path ...", command=lambda: self.browse_val_file())
        test_label = tk.Entry(el, textvariable=self.val_path)
        panel.pack(side="top", fill="x")
        tk.Label(panel, text="Validation set path:").pack(side="left", anchor="w", padx=5, pady=5)
        test_button.pack(side="right", anchor="w", padx=5, pady=5)
        test_label.pack(fill="x", padx=5, pady=5)
        return el

    def _create_trained_model_path_el(self, parent):
        el = tk.Frame(parent)
        panel = tk.Frame(el)
        self.trained_model_path = tk.StringVar()
        button = tk.Button(panel, text="select path ...", command=lambda: self.browse_trained_model())
        label = tk.Entry(el, textvariable=self.trained_model_path)
        panel.pack(side="top", fill="x")
        tk.Label(panel, text="trained model path:").pack(side="left", anchor="w", padx=5, pady=5)
        button.pack(side="right", anchor="w", padx=5, pady=5)
        label.pack(fill="x", padx=5, pady=5)
        return el

    def _create_nodes_or_corrupted_path_el(self, parent):
        el = tk.Frame(parent)
        panel = tk.Frame(el)
        self.nodes_or_corr_path = tk.StringVar()
        button = tk.Button(panel, text="select path ...", command=lambda: self.browse_nodes_or_corr_file())
        self.select_choices_node_corrupted = ["nodes path", "corrupted triples path"]
        self.select_node_corrupted = tk.StringVar(value=self.select_choices_node_corrupted[0])
        select_menu = tk.OptionMenu(panel, self.select_node_corrupted, *self.select_choices_node_corrupted)

        select_menu.configure(width=20)
        label = tk.Entry(el, textvariable=self.nodes_or_corr_path)
        panel.pack(side="top", fill="x")
        select_menu.pack(side="left", anchor="w", padx=5, pady=5)
        button.pack(side="right", anchor="w", padx=5, pady=5)
        label.pack(fill="x", padx=5, pady=5)
        return el

    def _create_anyburl_learn_el(self, parent):
        el = tk.LabelFrame(parent, text="learn config")
        panel = tk.Frame(el)
        panel.pack(side="top", fill="x")

        snapshot_at_frame = tk.Frame(panel)
        snapshot_at_label = tk.Label(snapshot_at_frame, text="Snapshot at:")
        snapshot_at_entry = tk.Entry(snapshot_at_frame, textvariable=self.snapshot_at, width=5)
        snapshot_at_info = tk.Label(
            snapshot_at_frame, text="as int in seconds, e.g. 100", font=self.controller.info_font
        )
        snapshot_at_frame.pack(side="top", padx=5, pady=(0, 10), anchor="w")
        snapshot_at_label.pack(side="left", padx=5, anchor="w")
        snapshot_at_entry.pack(side="left", anchor="w")
        snapshot_at_info.pack(side="left", anchor="w")

        policy_frame = tk.Frame(panel)
        policy_label = tk.Label(policy_frame, text="Policy:")
        policy_choices = ["1", "2"]
        self.selected_policy = tk.StringVar()
        self.selected_policy.set("2")
        policy_menu = tk.OptionMenu(policy_frame, self.selected_policy, *policy_choices)
        policy_frame.pack(side="top", padx=5, pady=(0, 10), anchor="w")
        policy_label.pack(side="left", padx=5, anchor="w")
        policy_menu.pack(side="left", anchor="w")

        reward_frame = tk.Frame(panel)
        reward_label = tk.Label(reward_frame, text="Reward:")
        reward_choices = ["1", "3", "5"]
        self.selected_reward = tk.StringVar()
        self.selected_reward.set("5")
        reward_menu = tk.OptionMenu(reward_frame, self.selected_reward, *reward_choices)
        reward_frame.pack(side="top", padx=5, pady=(0, 10), anchor="w")
        reward_label.pack(side="left", padx=5, anchor="w")
        reward_menu.pack(side="left", anchor="w")

        self.epsilon = tk.StringVar(value="0.1")
        epsilon_frame = tk.Frame(panel)
        epsilon_label = tk.Label(epsilon_frame, text="Epsilon:")
        epsilon_entry = tk.Entry(epsilon_frame, textvariable=self.epsilon, width=5)
        epsilon_info = tk.Label(
            epsilon_frame, text="as float, e.g. 0.1", font=self.controller.info_font
        )
        epsilon_frame.pack(side="top", padx=5, pady=(0, 10), anchor="w")
        epsilon_label.pack(side="left", padx=5, anchor="w")
        epsilon_entry.pack(side="left", anchor="w")
        epsilon_info.pack(side="left", anchor="w")

        self.worker_threads_learn = tk.StringVar(value="7")
        worker_threads_frame = tk.Frame(panel)
        worker_threads_label = tk.Label(worker_threads_frame, text="Worker threads:")
        worker_threads_entry = tk.Entry(worker_threads_frame, textvariable=self.worker_threads_learn, width=5)
        worker_threads_info = tk.Label(
            worker_threads_frame, text="as int in seconds, e.g. 7", font=self.controller.info_font
        )
        worker_threads_frame.pack(side="top", padx=5, pady=(0, 10), anchor="w")
        worker_threads_label.pack(side="left", padx=5, anchor="w")
        worker_threads_entry.pack(side="left", anchor="w")
        worker_threads_info.pack(side="left", anchor="w")

        return el

    def _create_anyburl_eval_el(self, parent):
        el = tk.LabelFrame(parent, text="eval config")
        panel = tk.Frame(el)
        panel.pack(side="top", fill="x")

        snapshot_at_frame = tk.Frame(panel)
        snapshot_at_label = tk.Label(snapshot_at_frame, text="Snapshot at:")
        snapshot_at_entry = tk.Entry(snapshot_at_frame, textvariable=self.snapshot_at, width=5)
        snapshot_at_info = tk.Label(
            snapshot_at_frame, text="as int in seconds, e.g. 100", font=self.controller.info_font
        )
        snapshot_at_frame.pack(side="top", padx=5, pady=(0, 10), anchor="w")
        snapshot_at_label.pack(side="left", padx=5, anchor="w")
        snapshot_at_entry.pack(side="left", anchor="w")
        snapshot_at_info.pack(side="left", anchor="w")

        discrimination_bound_frame = tk.Frame(panel)
        self.discrimination_bound = tk.StringVar(value="1000")
        discrimination_bound_label = tk.Label(discrimination_bound_frame, text="Discrimination bound:")
        discrimination_bound_entry = tk.Entry(discrimination_bound_frame, textvariable=self.discrimination_bound, width=5)
        discrimination_bound_info = tk.Label(
            discrimination_bound_frame, text="as int, e.g. 1000", font=self.controller.info_font
        )
        discrimination_bound_frame.pack(side="top", padx=5, pady=(0, 10), anchor="w")
        discrimination_bound_label.pack(side="left", padx=5, anchor="w")
        discrimination_bound_entry.pack(side="left", anchor="w")
        discrimination_bound_info.pack(side="left", anchor="w")

        unseen_negative_examples_frame = tk.Frame(panel)
        self.unseen_negative_examples = tk.StringVar(value="5")
        unseen_negative_examples_label = tk.Label(unseen_negative_examples_frame, text="Unseen negative examples:")
        unseen_negative_examples_entry = tk.Entry(unseen_negative_examples_frame, textvariable=self.unseen_negative_examples,
                                              width=5)
        unseen_negative_examples_info = tk.Label(
            unseen_negative_examples_frame, text="as int, e.g. 5", font=self.controller.info_font
        )
        unseen_negative_examples_frame.pack(side="top", padx=5, pady=(0, 10), anchor="w")
        unseen_negative_examples_label.pack(side="left", padx=5, anchor="w")
        unseen_negative_examples_entry.pack(side="left", anchor="w")
        unseen_negative_examples_info.pack(side="left", anchor="w")

        top_k_output_frame = tk.Frame(panel)
        self.top_k_output = tk.StringVar(value="10")
        top_k_output_label = tk.Label(top_k_output_frame, text="Top k output:")
        top_k_output_entry = tk.Entry(top_k_output_frame,
                                                  textvariable=self.top_k_output,
                                                  width=5)
        top_k_output_info = tk.Label(
            top_k_output_frame, text="as int, has to be equal or higher than highest specified k in metrics", font=self.controller.info_font
        )
        top_k_output_frame.pack(side="top", padx=5, pady=(0, 10), anchor="w")
        top_k_output_label.pack(side="left", padx=5, anchor="w")
        top_k_output_entry.pack(side="left", anchor="w")
        top_k_output_info.pack(side="left", anchor="w")

        worker_threads_eval_frame = tk.Frame(panel)
        self.worker_threads_eval = tk.StringVar(value="7")
        worker_threads_eval_label = tk.Label(worker_threads_eval_frame, text="Worker threads:")
        worker_threads_eval_entry = tk.Entry(worker_threads_eval_frame,
                                      textvariable=self.worker_threads_eval,
                                      width=5)
        worker_threads_eval_info = tk.Label(
            worker_threads_eval_frame, text="as int, e.g. 7",
            font=self.controller.info_font
        )
        worker_threads_eval_frame.pack(side="top", padx=5, pady=(0, 10), anchor="w")
        worker_threads_eval_label.pack(side="left", padx=5, anchor="w")
        worker_threads_eval_entry.pack(side="left", anchor="w")
        worker_threads_eval_info.pack(side="left", anchor="w")

        threshold_confidence_frame = tk.Frame(panel)
        self.threshold_confidence = tk.StringVar(value="0.001")
        threshold_confidence_label = tk.Label(threshold_confidence_frame, text="Threshold confidence:")
        threshold_confidence_entry = tk.Entry(threshold_confidence_frame,
                                             textvariable=self.threshold_confidence,
                                             width=5)
        threshold_confidence_info = tk.Label(
            threshold_confidence_frame, text="as float, e.g. 0.001",
            font=self.controller.info_font
        )
        threshold_confidence_frame.pack(side="top", padx=5, pady=(0, 10), anchor="w")
        threshold_confidence_label.pack(side="left", padx=5, anchor="w")
        threshold_confidence_entry.pack(side="left", anchor="w")
        threshold_confidence_info.pack(side="left", anchor="w")

        self.fast = tk.IntVar(value=1)
        no_fast_checkbox = tk.Checkbutton(panel, text="Fast", variable=self.fast)
        no_fast_checkbox.pack(side="top", padx=5, pady=(0, 10), anchor="w")

        self.discrimination_unique = tk.IntVar(value=0)
        discrimination_unique_checkbox = tk.Checkbutton(panel, text="Discrimination unique", variable=self.discrimination_unique)
        discrimination_unique_checkbox.pack(side="top", padx=5, pady=(0, 10), anchor="w")

        self.intermediate_discrimination = tk.IntVar(value=1)
        no_intermediate_discrimination_checkbox = tk.Checkbutton(panel, text="Intermediate discrimination", variable=self.intermediate_discrimination)
        no_intermediate_discrimination_checkbox.pack(side="top", padx=5, pady=(0, 10), anchor="w")

        return el

    def browse_test_file(self):
        self.test_path.set(filedialog.askopenfilename())

    def browse_neg_test_file(self):
        self.neg_test_path.set(filedialog.askopenfilename())

    def browse_train_file(self):
        self.train_path.set(filedialog.askopenfilename())

    def browse_neg_train_file(self):
        self.neg_train_path.set(filedialog.askopenfilename())

    def browse_val_file(self):
        self.val_path.set(filedialog.askopenfilename())

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
        if os.path.exists(test_path) or "SplitFrame" in self.controller.selected_frames:
            self.test_path.set(test_path)

        train_path = os.path.join(tts_files_folder, ttsConst.TRAIN_FILE_NAME)
        if os.path.exists(train_path) or "SplitFrame" in self.controller.selected_frames:
            self.train_path.set(train_path)

        neg_test_path = os.path.join(tts_files_folder, ttsConst.NEGATIVE_PREFIX + ttsConst.TEST_FILE_NAME)
        if os.path.exists(neg_test_path) or "SplitFrame" in self.controller.selected_frames:
            self.neg_test_path.set(neg_test_path)

        neg_train_path = os.path.join(tts_files_folder, ttsConst.NEGATIVE_PREFIX + ttsConst.TRAIN_FILE_NAME)
        if os.path.exists(neg_train_path) or "SplitFrame" in self.controller.selected_frames:
            self.neg_train_path.set(neg_train_path)

        val_path = os.path.join(tts_files_folder, ttsConst.VAL_FILE_NAME)
        if os.path.exists(val_path) or "SplitFrame" in self.controller.selected_frames:
            self.val_path.set(val_path)

        # train val nodes path for obl 2020
        nodes_path = os.path.join(tts_files_folder, ttsConst.TRAIN_VAL_NODES_FILE_NAME)
        train_nodes_path = os.path.join(tts_files_folder, ttsConst.TRAIN_NODES_FILE_NAME)
        if os.path.exists(nodes_path):
            self.nodes_or_corr_path.set(nodes_path)
        elif os.path.exists(train_nodes_path) or "GraphCreationFrame" in self.controller.selected_frames:
            self.nodes_or_corr_path.set(train_nodes_path)

    def next_page(self):
        if self.method.get() == "embedded":
            if not self.train.get() and not self.evaluate.get():
                messagebox.showerror("ERROR", "at least one action (training, evaluation) must be chosen")
                return
            if not self.select_model.get():
                messagebox.showerror("ERROR", "Please select a model")
                return
            if self.train.get():
                if not self.train_path.get():
                    messagebox.showerror("ERROR", "For training, please select a training set path")
                    return
            if self.evaluate.get():
                if not self.train.get() and not self.trained_model_path.get():
                    messagebox.showerror(
                        "ERROR", "Please either provide a path to your trained model or choose 'perform training"
                    )
                    return
                if not self.test_path.get():
                    messagebox.showerror("ERROR", "Please provide a test path")
                    return
                if (self.hits.get() or self.mrr.get()) and not self.nodes_or_corr_path.get():
                    messagebox.showerror(
                        "ERROR", "Ranked metrics (his@K, MRR) require either a nodes file or a file of corrupted triples"
                    )
                    return
                if all([not self.mrr.get(), not self.hits.get()]) and all(
                        [not x.get() for _, x in self.threshold_metrics_dict.items()]
                ):
                    messagebox.showerror("ERROR", "'Perform evaluation' is chosen, but no evaluation metrics are selected")
                    return

            self.controller.ARGS_LIST_TRAIN = []
            self.controller.ARGS_LIST_EVAL = []

            if self.train.get():
                self.controller.ARGS_LIST_TRAIN.extend(["train", "embedded"])
                self.controller.ARGS_LIST_TRAIN.extend(["-m", str(EmbeddedModelTypes[self.select_model.get()].name)])
                if self.config_path.get():
                    self.controller.ARGS_LIST_TRAIN.extend(["--config", self.config_path.get()])
                self.controller.ARGS_LIST_TRAIN.extend(["--training-path", self.train_path.get()])
                if self.neg_train_path.get():
                    self.controller.ARGS_LIST_TRAIN.extend(["--negative-training-path", self.neg_train_path.get()])
                if self.select_node_corrupted.get() == "nodes path":
                    self.controller.ARGS_LIST_TRAIN.extend(["--nodes", self.nodes_or_corr_path.get()])

            if self.evaluate.get():
                self.controller.ARGS_LIST_EVAL.extend(["evaluate", "embedded"])
                self.controller.ARGS_LIST_EVAL.extend(["-m", str(EmbeddedModelTypes[self.select_model.get()].name)])
                if self.config_path.get():
                    self.controller.ARGS_LIST_EVAL.extend(["--config", self.config_path.get()])
                if self.trained_model_path.get():
                    self.controller.ARGS_LIST_EVAL.extend(["--trained-model", self.trained_model_path.get()])
                self.controller.ARGS_LIST_EVAL.extend(["--testing-path", self.test_path.get()])
                if self.neg_test_path.get():
                    self.controller.ARGS_LIST_EVAL.extend(["--negative-testing-path", self.neg_test_path.get()])
                ranked_metrics = [x.name for x, y in self.rank_metrics_dict.items() if y.get()]
                for ranked_metric in ranked_metrics:
                    self.controller.ARGS_LIST_EVAL.extend(["--metrics", ranked_metric])

                threshold_metrics = [x.name for x, y in self.threshold_metrics_dict.items() if y.get()]
                for threshold_metric in threshold_metrics:
                    self.controller.ARGS_LIST_EVAL.extend(["--metrics", threshold_metric])

                if (
                        RankMetricType.HITS_AT_K in self.rank_metrics_dict.keys()
                        or RankMetricType.HITS_AT_K_UNFILTERED in self.rank_metrics_dict.keys()
                ):
                    import ast

                    for x in ast.literal_eval(self.ks.get()):
                        self.controller.ARGS_LIST_EVAL.extend(["--ks", str(x)])
                if self.select_node_corrupted.get() == "nodes path":
                    self.controller.ARGS_LIST_EVAL.extend(["--nodes", self.nodes_or_corr_path.get()])

        elif self.method.get() == "symbolic":
            if not self.train.get() and not self.evaluate.get():
                messagebox.showerror("ERROR", "at least one action (training, evaluation) must be chosen")
                return
            if not self.select_model.get():
                messagebox.showerror("ERROR", "Please select a model")
                return
            if not self.train_path.get():
                messagebox.showerror("ERROR", "For training, please select a training set path")
                return
            if not self.test_path.get():
                messagebox.showerror("ERROR", "Please provide a test path")
                return
            if self.evaluate.get():
                if all([not self.mrr.get(), not self.hits.get()]) and all(
                        [not x.get() for _, x in self.threshold_metrics_dict.items()]
                ):
                    messagebox.showerror("ERROR", "'Perform evaluation' is chosen, but no evaluation metrics are selected")
                    return
            self.controller.ARGS_LIST_EVAL = []
            self.controller.ARGS_LIST_TRAIN = []

            if self.train.get():
                self.controller.ARGS_LIST_TRAIN.extend(["train", "symbolic"])
                self.controller.ARGS_LIST_TRAIN.extend(["-m", str(SymbolicModelTypes[self.select_model.get()].name)])
                self.controller.ARGS_LIST_TRAIN.extend(["--training-path", self.train_path.get()])
                self.controller.ARGS_LIST_TRAIN.extend(["--testing-path", self.test_path.get()])
                self.controller.ARGS_LIST_TRAIN.extend(["--valid-path", self.val_path.get()])
                self.controller.ARGS_LIST_TRAIN.extend(["--policy", self.selected_policy.get()])
                self.controller.ARGS_LIST_TRAIN.extend(["--reward", self.selected_reward.get()])
                self.controller.ARGS_LIST_TRAIN.extend(["--snapshot-at", self.snapshot_at.get()])
                self.controller.ARGS_LIST_TRAIN.extend(["--worker-threads", self.worker_threads_learn.get()])

            if self.evaluate.get():
                self.controller.ARGS_LIST_EVAL.extend(["evaluate", "symbolic"])
                self.controller.ARGS_LIST_EVAL.extend(["-m", str(SymbolicModelTypes[self.select_model.get()].name)])
                self.controller.ARGS_LIST_EVAL.extend(["--training-path", self.train_path.get()])
                self.controller.ARGS_LIST_EVAL.extend(["--testing-path", self.test_path.get()])
                self.controller.ARGS_LIST_EVAL.extend(["--valid-path", self.val_path.get()])
                self.controller.ARGS_LIST_EVAL.extend(["--discrimination-bound", self.discrimination_bound.get()])
                self.controller.ARGS_LIST_EVAL.extend(["--top-k-output", self.top_k_output.get()])
                self.controller.ARGS_LIST_EVAL.extend(["--snapshot-at", self.snapshot_at.get()])
                self.controller.ARGS_LIST_EVAL.extend(["--worker-threads", self.worker_threads_eval.get()])
                self.controller.ARGS_LIST_EVAL.extend(["--threshold-confidence", self.threshold_confidence.get()])
                if self.fast.get() == 0:
                    self.controller.ARGS_LIST_EVAL.extend(["--no-fast"])
                if self.discrimination_unique.get() == 1:
                    self.controller.ARGS_LIST_EVAL.extend(["--discrimination-unique"])
                if self.intermediate_discrimination.get() == 0:
                    self.controller.ARGS_LIST_EVAL.extend(["--no-intermediate-discrimination"])


        self.controller.show_next_frame()
