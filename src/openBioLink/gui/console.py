# """ source: #https://github.com/beenje/tkinter-logging-text-widget/blob/master/main.py """
import logging
import queue
from tkinter import ttk, N, S, E, W
from tkinter.scrolledtext import ScrolledText

from openbiolink.gui.gui import *

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
        self.scrolled_text.tag_config('INFO', foreground='black')
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

    # def quit(self, *args):
    #    self.root.destroy()
