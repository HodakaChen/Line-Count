from tkinter import Frame, Tk, filedialog
from tkinter import CENTER, END, X, N, W
from tkinter import ttk
from os import listdir, path

SUFFIX = {"c": "C/C++", "cpp": "C/C++", "java": "Java", "py": "Python", "js": "Type/JavaScript",
          "ts": "Type/JavaScript", "asm": "Assembly", "html": "Html/CSS", "h": "C/C++", "css": "Html/CSS"}
FILETYPE = {"C/C++": ['c', 'cpp', 'h'], "Java": ['java'], "Python": ['py'],
            "Type/JavaScript": ['js', 'ts'], "Html/CSS": ['html', 'css'], "Assembly": ['asm']}


class Application(Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.counter = {}
        for s in FILETYPE.keys():
            self.counter[s] = 0
        self.master = master
        self.pack()
        self.filePath = None
        self.createWidget()

    def createWidget(self):
        self.label01 = ttk.Label(
            self.master, text='Line Count', font=("Harlow Solid Italic", 30), width=200, anchor=CENTER)
        self.label01.pack(anchor=N, pady=20)

        self.table = ttk.Treeview(self.master, columns=(
            'Language', 'Lines'), show='headings', displaycolumns='#all', height=9)
        self.table.heading('Language', text='Language', anchor=CENTER)
        self.table.heading('Lines', text='Lines', anchor=CENTER)
        self.table.column('Language', width=50, anchor=CENTER)
        self.table.column('Lines', width=50, anchor=CENTER)
        self.table.insert("", END, values=(
            '----------------------------', '----------------------------'))
        for lang in FILETYPE.keys():
            self.table.insert("", END, values=(lang, 0))
        self.table.insert("", END, values=(
            '----------------------------', '----------------------------'))
        self.table.insert("", END, values=('SUM', 0))
        self.table.pack(fill=X, anchor=N, pady=10)

        self.frame01 = ttk.Frame(self.master)

        self.label02 = ttk.Label(
            self.frame01, text="Path>>", font=("Consolas", 11), width=26, anchor=W, background="#E8E8E8", wraplength=210)
        self.label02.grid(row=0, column=0)

        self.btn01 = ttk.Button(self.frame01, text="Directory",
                                command=self.getDirPath)
        self.btn01.grid(row=0, column=1)

        self.frame01.pack()

        self.frame02 = ttk.Frame(self.master)

        self.btn02 = ttk.Button(
            self.frame02, text="Reset", command=self.reset, padding=5)
        self.btn02.grid(row=0, column=1)

        self.btn03 = ttk.Button(
            self.frame02, text="Count", command=self.countLines, padding=5)
        self.btn03.grid(row=0, column=0)

        self.frame02.pack(pady=6)

    def reset(self) -> None:
        for k in self.counter.keys():
            self.counter[k] = 0
        self.updateRes()
        self.label02['text'] = "Path>>"
        self.filePath = None

    def getDirPath(self) -> None:
        self.filePath = filedialog.askdirectory(title="Choose the directory")
        self.label02['text'] = "Path>>" + str(self.filePath)
        return None

    def countLines(self) -> None:
        if(self.filePath != None):
            self.getAllFile(self.filePath)
            self.updateRes()

    def getAllFile(self, rootPath: str) -> None:
        for file in listdir(rootPath):
            filePath = path.join(rootPath, file)

            if path.isdir(filePath):
                self.getAllFile(filePath)
                continue

            file_suffix = file.split(".")[-1]
            if file_suffix in SUFFIX.keys():
                self.search(filePath)

        return None

    def search(self, filePath: str) -> None:
        fileName = path.basename(filePath)
        file_suffix = fileName.split(".")[-1]
        file_type = SUFFIX[file_suffix]

        try:
            fp = open(filePath, 'r', encoding='gbk')
            rows = len(fp.readlines())
            fp.close()
            self.counter[file_type] += rows
        except UnicodeDecodeError:
            fp = open(filePath, 'r', encoding='utf-8')
            rows = len(fp.readlines())
            fp.close()
            self.counter[file_type] += rows

        return None

    def updateRes(self) -> None:
        i = 2
        sum = 0
        for lang in FILETYPE.keys():
            self.table.set("I00"+str(i), column="Lines",
                           value=self.counter[lang])
            sum += self.counter[lang]
            i += 1
        self.table.set("I009", column="Lines", value=sum)


if __name__ == '__main__':
    root = Tk()
    root.geometry('300x450+400+200')
    root.title("Line-Count")
    app = Application(master=root)

    root.mainloop()
