#import urllib.request


#url = "http://unmtid-shinyapps.net/download/drugcentral.dump.08262018.sql.gz"
#file_folder = "D:\Anna_Breit\master_thesis\playground"
#file_name = "sql_dump.sql.gz"
#file = os.path.join(file_folder, file_name)
#
#urllib.request.urlretrieve(url, file)
#
#df = dcp.table_to_df(file, "omop_relationship")
#print(df)
#
#
#import tkinter as tk
#from tkinter import simpledialog
#
#application_window = tk.Tk()
#application_window.withdraw()
#
#answer = simpledialog.askstring("Input", "What is your first name?",
#                                parent=application_window)
#if answer is not None:
#    print("Your first name is ", answer)
#else:
#    print("You don't have a first name?")
#
#answer = simpledialog.askinteger("Input", "What is your age?",
#                                 parent=application_window,
#                                 minvalue=0, maxvalue=100)
#if answer is not None:
#    print("Your age is ", answer)
#else:
#    print("You don't have an age?")
#
#answer = simpledialog.askfloat("Input", "What is your salary?",
#                               parent=application_window,
#                               minvalue=0.0, maxvalue=100000.0)
#if answer is not None:
#    print("Your salary is ", answer)
#else:
#    print("You don't have a salary?")
#
#import tkinter as tk
#from tkinter import filedialog
#
#
#
#filename = filedialog.askdirectory() #show an "Open" dialog box and return the path to the selected file
#print(filename)
#
#class Application(tk.Frame):
#    def __init__(self, master=None):
#        super().__init__(master)
#        self.master = master
#        self.pack()
#        self.create_widgets()
#
#    def create_widgets(self):
#        self.hi_there = tk.Button(self)
#        self.hi_there["text"] = "Hello World\n(click me)"
#        self.hi_there["command"] = self.say_hi
#        self.hi_there.pack(side="top")
#
#        self.quit = tk.Button(self, text="QUIT", fg="red",
#                              command=self.master.destroy)
#        self.quit.pack(side="bottom")
#
#    def say_hi(self):
#        print("hi there, everyone!")
#
#root = tk.Tk()
#app = Application(master=root)
##app.mainloop()

import cProfile
s = ['AACAF', 'AACAY', 'AACTFAAGC', 'AAGIY', 'AAIGF', 'AAMAF', 'AAPH', 'AAPT', 'AAST', 'AATDF', 'AATGF', 'AATRL', 'AAUKF',
 'AAWC', 'AABY', 'ABCAF', 'ABCCF', 'ABCE', 'ABCFF', 'ABCZF', 'ABCZY', 'ABEPF', 'ABHD', 'ABHI', 'ABLT', 'ABLYF', 'ABNAF',
 'ABNK', 'ABNRY', 'AACAF', 'AACAY', 'AACTFAAGC', 'AAGIY', 'AAIGF', 'AAMAF', 'AAPH', 'AAPT', 'AAST', 'AATDF', 'AATGF',
 'AATRL', 'AAUKF', 'AAWC', 'AABY', 'ABCAF', 'ABCCF', 'ABCE', 'ABCFF', 'ABCZF', 'ABCZY', 'ABEPF', 'ABHD', 'ABHI', 'ABLT',
 'ABLYF', 'ABNAF', 'ABNK', 'ABNRY', 'AACAF', 'AACAY', 'AACTFAAGC', 'AAGIY', 'AAIGF', 'AAMAF', 'AAPH', 'AAPT', 'AAST',
 'AATDF', 'AATGF', 'AATRL', 'AAUKF', 'AAWC', 'AABY', 'ABCAF', 'ABCCF', 'ABCE', 'ABCFF', 'ABCZF', 'ABCZY', 'ABEPF',
 'ABHD', 'ABHI', 'ABLT', 'ABLYF', 'ABNAF', 'ABNK', 'ABNRY', 'AACAF', 'AACAY', 'AACTFAAGC', 'AAGIY', 'AAIGF', 'AAMAF',
 'AAPH', 'AAPT', 'AAST', 'AATDF', 'AATGF', 'AATRL', 'AAUKF', 'AAWC', 'AABY', 'ABCAF', 'ABCCF', 'ABCE', 'ABCFF', 'ABCZF',
 'ABCZY', 'ABEPF', 'ABHD', 'ABHI', 'ABLT', 'ABLYF', 'ABNAF', 'ABNK', 'ABNRY', 'AACAF', 'AACAY', 'AACTFAAGC', 'AAGIY',
 'AAIGF', 'AAMAF', 'AAPH', 'AAPT', 'AAST', 'AATDF', 'AATGF', 'AATRL', 'AAUKF', 'AAWC', 'AABY', 'ABCAF', 'ABCCF', 'ABCE', 'ABCFF', 'ABCZF', 'ABCZY', 'ABEPF', 'ABHD', 'ABHI', 'ABLT', 'ABLYF', 'ABNAF', 'ABNK', 'ABNRY', 'AACAF', 'AACAY', 'AACTFAAGC', 'AAGIY', 'AAIGF', 'AAMAF', 'AAPH', 'AAPT', 'AAST', 'AATDF', 'AATGF', 'AATRL', 'AAUKF', 'AAWC', 'AABY', 'ABCAF', 'ABCCF', 'ABCE', 'ABCFF', 'ABCZF', 'ABCZY', 'ABEPF', 'ABHD', 'ABHI', 'ABLT', 'ABLYF', 'ABNAF', 'ABNK', 'ABNRY', 'AACAF', 'AACAY', 'AACTFAAGC', 'AAGIY', 'AAIGF', 'AAMAF', 'AAPH', 'AAPT', 'AAST', 'AATDF', 'AATGF', 'AATRL', 'AAUKF', 'AAWC', 'AABY', 'ABCAF', 'ABCCF', 'ABCE', 'ABCFF', 'ABCZF', 'ABCZY', 'ABEPF', 'ABHD', 'ABHI', 'ABLT', 'ABLYF', 'ABNAF', 'ABNK', 'ABNRY', 'AACAF', 'AACAY', 'AACTFAAGC', 'AAGIY', 'AAIGF', 'AAMAF', 'AAPH', 'AAPT', 'AAST', 'AATDF', 'AATGF', 'AATRL', 'AAUKF', 'AAWC', 'AABY', 'ABCAF', 'ABCCF', 'ABCE', 'ABCFF', 'ABCZF', 'ABCZY', 'ABEPF', 'ABHD', 'ABHI', 'ABLT', 'ABLYF', 'ABNAF', 'ABNK', 'ABNRY', 'AACAF', 'AACAY', 'AACTFAAGC', 'AAGIY', 'AAIGF', 'AAMAF', 'AAPH', 'AAPT', 'AAST', 'AATDF', 'AATGF', 'AATRL', 'AAUKF', 'AAWC', 'AABY', 'ABCAF', 'ABCCF', 'ABCE', 'ABCFF', 'ABCZF', 'ABCZY', 'ABEPF', 'ABHD', 'ABHI', 'ABLT', 'ABLYF', 'ABNAF', 'ABNK', 'ABNRY', 'AACAF', 'AACAY', 'AACTFAAGC', 'AAGIY', 'AAIGF', 'AAMAF', 'AAPH', 'AAPT', 'AAST', 'AATDF', 'AATGF', 'AATRL', 'AAUKF', 'AAWC', 'AABY', 'ABCAF', 'ABCCF', 'ABCE', 'ABCFF', 'ABCZF', 'ABCZY', 'ABEPF', 'ABHD', 'ABHI', 'ABLT', 'ABLYF', 'ABNAF', 'ABNK', 'ABNRY', 'AACAF', 'AACAY', 'AACTFAAGC', 'AAGIY', 'AAIGF', 'AAMAF', 'AAPH', 'AAPT', 'AAST', 'AATDF', 'AATGF', 'AATRL', 'AAUKF', 'AAWC', 'AABY', 'ABCAF', 'ABCCF', 'ABCE', 'ABCFF', 'ABCZF', 'ABCZY', 'ABEPF', 'ABHD', 'ABHI', 'ABLT', 'ABLYF', 'ABNAF', 'ABNK', 'ABNRY', 'AACAF', 'AACAY', 'AACTFAAGC', 'AAGIY', 'AAIGF', 'AAMAF', 'AAPH', 'AAPT', 'AAST', 'AATDF', 'AATGF', 'AATRL', 'AAUKF', 'AAWC', 'AABY', 'ABCAF', 'ABCCF', 'ABCE', 'ABCFF', 'ABCZF', 'ABCZY', 'ABEPF', 'ABHD', 'ABHI', 'ABLT', 'ABLYF', 'ABNAF', 'ABNK', 'ABNRY', 'AACAF', 'AACAY', 'AACTFAAGC', 'AAGIY', 'AAIGF', 'AAMAF', 'AAPH', 'AAPT', 'AAST', 'AATDF', 'AATGF', 'AATRL', 'AAUKF', 'AAWC', 'AABY', 'ABCAF', 'ABCCF', 'ABCE', 'ABCFF', 'ABCZF', 'ABCZY', 'ABEPF', 'ABHD', 'ABHI', 'ABLT', 'ABLYF', 'ABNAF', 'ABNK', 'ABNRY', 'AACAF', 'AACAY', 'AACTFAAGC', 'AAGIY', 'AAIGF', 'AAMAF', 'AAPH', 'AAPT', 'AAST', 'AATDF', 'AATGF', 'AATRL', 'AAUKF', 'AAWC', 'AABY', 'ABCAF', 'ABCCF', 'ABCE', 'ABCFF', 'ABCZF', 'ABCZY', 'ABEPF', 'ABHD', 'ABHI', 'ABLT', 'ABLYF', 'ABNAF', 'ABNK', 'ABNRY', 'AACAF', 'AACAY', 'AACTFAAGC', 'AAGIY', 'AAIGF', 'AAMAF', 'AAPH', 'AAPT', 'AAST', 'AATDF', 'AATGF', 'AATRL', 'AAUKF', 'AAWC', 'AABY', 'ABCAF', 'ABCCF', 'ABCE', 'ABCFF', 'ABCZF', 'ABCZY', 'ABEPF', 'ABHD', 'ABHI', 'ABLT', 'ABLYF', 'ABNAF', 'ABNK', 'ABNRY', 'AACAF', 'AACAY', 'AACTFAAGC', 'AAGIY', 'AAIGF', 'AAMAF', 'AAPH', 'AAPT', 'AAST', 'AATDF', 'AATGF', 'AATRL', 'AAUKF', 'AAWC', 'AABY', 'ABCAF', 'ABCCF', 'ABCE', 'ABCFF', 'ABCZF', 'ABCZY', 'ABEPF', 'ABHD', 'ABHI', 'ABLT', 'ABLYF', 'ABNAF', 'ABNK', 'ABNRY', 'AACAF', 'AACAY', 'AACTFAAGC', 'AAGIY', 'AAIGF', 'AAMAF', 'AAPH', 'AAPT', 'AAST', 'AATDF', 'AATGF', 'AATRL', 'AAUKF', 'AAWC', 'AABY', 'ABCAF', 'ABCCF', 'ABCE', 'ABCFF', 'ABCZF', 'ABCZY', 'ABEPF', 'ABHD', 'ABHI', 'ABLT', 'ABLYF', 'ABNAF', 'ABNK', 'ABNRY', 'AACAF', 'AACAY', 'AACTFAAGC', 'AAGIY', 'AAIGF', 'AAMAF', 'AAPH', 'AAPT', 'AAST', 'AATDF', 'AATGF', 'AATRL', 'AAUKF', 'AAWC', 'AABY', 'ABCAF', 'ABCCF', 'ABCE', 'ABCFF', 'ABCZF', 'ABCZY', 'ABEPF', 'ABHD', 'ABHI', 'ABLT', 'ABLYF', 'ABNAF', 'ABNK', 'ABNRY', 'AACAF', 'AACAY', 'AACTFAAGC', 'AAGIY', 'AAIGF', 'AAMAF', 'AAPH', 'AAPT', 'AAST', 'AATDF', 'AATGF', 'AATRL', 'AAUKF', 'AAWC', 'AABY', 'ABCAF', 'ABCCF', 'ABCE', 'ABCFF', 'ABCZF', 'ABCZY', 'ABEPF', 'ABHD', 'ABHI', 'ABLT', 'ABLYF', 'ABNAF', 'ABNK', 'ABNRY', 'AACAF', 'AACAY', 'AACTFAAGC', 'AAGIY', 'AAIGF', 'AAMAF', 'AAPH', 'AAPT', 'AAST', 'AATDF', 'AATGF', 'AATRL', 'AAUKF', 'AAWC', 'AABY', 'ABCAF', 'ABCCF', 'ABCE', 'ABCFF', 'ABCZF', 'ABCZY', 'ABEPF', 'ABHD', 'ABHI', 'ABLT', 'ABLYF', 'ABNAF', 'ABNK', 'ABNRY', 'AACAF', 'AACAY', 'AACTFAAGC', 'AAGIY', 'AAIGF', 'AAMAF', 'AAPH', 'AAPT', 'AAST', 'AATDF', 'AATGF', 'AATRL', 'AAUKF', 'AAWC', 'AABY', 'ABCAF', 'ABCCF', 'ABCE', 'ABCFF', 'ABCZF', 'ABCZY', 'ABEPF', 'ABHD', 'ABHI', 'ABLT', 'ABLYF', 'ABNAF', 'ABNK', 'ABNRY', 'AACAF', 'AACAY', 'AACTFAAGC', 'AAGIY', 'AAIGF', 'AAMAF', 'AAPH', 'AAPT', 'AAST', 'AATDF', 'AATGF', 'AATRL', 'AAUKF', 'AAWC', 'AABY', 'ABCAF', 'ABCCF', 'ABCE', 'ABCFF', 'ABCZF', 'ABCZY', 'ABEPF', 'ABHD', 'ABHI', 'ABLT', 'ABLYF', 'ABNAF', 'ABNK', 'ABNRY', 'AACAF', 'AACAY', 'AACTFAAGC', 'AAGIY', 'AAIGF', 'AAMAF', 'AAPH', 'AAPT', 'AAST', 'AATDF', 'AATGF', 'AATRL', 'AAUKF', 'AAWC', 'AABY', 'ABCAF', 'ABCCF', 'ABCE', 'ABCFF', 'ABCZF', 'ABCZY', 'ABEPF', 'ABHD', 'ABHI', 'ABLT', 'ABLYF', 'ABNAF', 'ABNK', 'ABNRY', 'AACAF', 'AACAY', 'AACTFAAGC', 'AAGIY', 'AAIGF', 'AAMAF', 'AAPH', 'AAPT', 'AAST', 'AATDF', 'AATGF', 'AATRL', 'AAUKF', 'AAWC', 'AABY', 'ABCAF', 'ABCCF', 'ABCE', 'ABCFF', 'ABCZF', 'ABCZY', 'ABEPF', 'ABHD', 'ABHI', 'ABLT', 'ABLYF', 'ABNAF', 'ABNK', 'ABNRY', 'AACAF', 'AACAY', 'AACTFAAGC', 'AAGIY', 'AAIGF', 'AAMAF', 'AAPH', 'AAPT', 'AAST', 'AATDF', 'AATGF', 'AATRL', 'AAUKF', 'AAWC', 'AABY', 'ABCAF', 'ABCCF', 'ABCE', 'ABCFF', 'ABCZF', 'ABCZY', 'ABEPF', 'ABHD', 'ABHI', 'ABLT', 'ABLYF', 'ABNAF', 'ABNK', 'ABNRY', 'AACAF', 'AACAY', 'AACTFAAGC', 'AAGIY', 'AAIGF', 'AAMAF', 'AAPH', 'AAPT', 'AAST', 'AATDF', 'AATGF', 'AATRL', 'AAUKF', 'AAWC', 'AABY', 'ABCAF', 'ABCCF', 'ABCE', 'ABCFF', 'ABCZF', 'ABCZY', 'ABEPF', 'ABHD', 'ABHI', 'ABLT', 'ABLYF', 'ABNAF', 'ABNK', 'ABNRY', 'AACAF', 'AACAY', 'AACTFAAGC', 'AAGIY', 'AAIGF', 'AAMAF', 'AAPH', 'AAPT', 'AAST', 'AATDF', 'AATGF', 'AATRL', 'AAUKF', 'AAWC', 'AABY', 'ABCAF', 'ABCCF', 'ABCE', 'ABCFF', 'ABCZF', 'ABCZY', 'ABEPF', 'ABHD', 'ABHI', 'ABLT', 'ABLYF', 'ABNAF', 'ABNK', 'ABNRY', 'AACAF', 'AACAY', 'AACTFAAGC', 'AAGIY', 'AAIGF', 'AAMAF', 'AAPH', 'AAPT', 'AAST', 'AATDF', 'AATGF', 'AATRL', 'AAUKF', 'AAWC', 'AABY', 'ABCAF', 'ABCCF', 'ABCE', 'ABCFF', 'ABCZF', 'ABCZY', 'ABEPF', 'ABHD', 'ABHI', 'ABLT', 'ABLYF', 'ABNAF', 'ABNK', 'ABNRY', 'AACAF', 'AACAY', 'AACTFAAGC', 'AAGIY', 'AAIGF', 'AAMAF', 'AAPH', 'AAPT', 'AAST', 'AATDF', 'AATGF', 'AATRL', 'AAUKF', 'AAWC', 'AABY', 'ABCAF', 'ABCCF', 'ABCE', 'ABCFF', 'ABCZF', 'ABCZY', 'ABEPF', 'ABHD', 'ABHI', 'ABLT', 'ABLYF', 'ABNAF', 'ABNK', 'ABNRY', 'AACAF', 'AACAY', 'AACTFAAGC', 'AAGIY', 'AAIGF', 'AAMAF', 'AAPH', 'AAPT', 'AAST', 'AATDF', 'AATGF', 'AATRL', 'AAUKF', 'AAWC', 'AABY', 'ABCAF', 'ABCCF', 'ABCE', 'ABCFF', 'ABCZF', 'ABCZY', 'ABEPF', 'ABHD', 'ABHI', 'ABLT', 'ABLYF', 'ABNAF', 'ABNK', 'ABNRY', 'AACAF', 'AACAY', 'AACTFAAGC', 'AAGIY', 'AAIGF', 'AAMAF', 'AAPH', 'AAPT', 'AAST', 'AATDF', 'AATGF', 'AATRL', 'AAUKF', 'AAWC', 'AABY', 'ABCAF', 'ABCCF', 'ABCE', 'ABCFF', 'ABCZF', 'ABCZY', 'ABEPF', 'ABHD', 'ABHI', 'ABLT', 'ABLYF', 'ABNAF', 'ABNK', 'ABNRY', 'AACAF', 'AACAY', 'AACTFAAGC', 'AAGIY', 'AAIGF', 'AAMAF', 'AAPH', 'AAPT', 'AAST', 'AATDF', 'AATGF', 'AATRL', 'AAUKF', 'AAWC', 'AABY', 'ABCAF', 'ABCCF', 'ABCE', 'ABCFF', 'ABCZF', 'ABCZY', 'ABEPF', 'ABHD', 'ABHI', 'ABLT', 'ABLYF', 'ABNAF', 'ABNK', 'ABNRY', 'AACAF', 'AACAY', 'AACTFAAGC', 'AAGIY', 'AAIGF', 'AAMAF', 'AAPH', 'AAPT', 'AAST', 'AATDF', 'AATGF', 'AATRL', 'AAUKF', 'AAWC', 'AABY', 'ABCAF', 'ABCCF', 'ABCE', 'ABCFF', 'ABCZF', 'ABCZY', 'ABEPF', 'ABHD', 'ABHI', 'ABLT', 'ABLYF', 'ABNAF', 'ABNK', 'ABNRY', 'AACAF', 'AACAY', 'AACTFAAGC', 'AAGIY', 'AAIGF', 'AAMAF', 'AAPH', 'AAPT', 'AAST', 'AATDF', 'AATGF', 'AATRL', 'AAUKF', 'AAWC', 'AABY', 'ABCAF', 'ABCCF', 'ABCE', 'ABCFF', 'ABCZF', 'ABCZY', 'ABEPF', 'ABHD', 'ABHI', 'ABLT', 'ABLYF', 'ABNAF', 'ABNK', 'ABNRY', 'one', 'two', 'one', 'two', 'one', 'two', 'one', 'two', 'one', 'two', 'one', 'two', 'three', 'four']

strings = ['AACAF','AACAY','AACTF'
'AAGC','AAGIY','AAIGF',
'AAMAF','AAPH','AAPT',
'AAST','AATDF','AATGF',
'AATRL','AAUKF','AAWC',
'AABY','ABCAF','ABCCF',
'ABCE','ABCFF','ABCZF',
'ABCZY','ABEPF','ABHD',
'ABHI','ABLT','ABLYF',
'ABNAF','ABNK','ABNRY']


def function():
    list = []
    for i in range (len(s)-1):
        y= s[i]+ s[i+1]
        list.append(y)
    print(len(list))

cProfile.run('function()')