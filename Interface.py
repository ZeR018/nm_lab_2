import tkinter as tk
from ctypes import *
import ctypes
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk, END
from tkinter import *
from PIL import Image, ImageTk
import numpy as np
from test import test


class Interface:
    def __init__(self, master):
        self.master = master  # инициализируем основное окно
        self.photo = tk.PhotoImage(file='logo.png')  # загрузка иконки приложения
        master.iconphoto(False, self.photo)  # установка иконки
        master.title('Лабораторная работа №2. Решение краевых задач для ОДУ. Вариант 3')  # заголовок
        master.configure(bg='#ececec')  # фон
        master.minsize(1200, 600)  # минимальный размер окна

        self.ep = tk.DoubleVar(master, 0.3)  # Эпсилон
        self.mu1 = tk.DoubleVar(master, 1)  # мю 1
        self.mu2 = tk.DoubleVar(master, 0)  # мю 2
        self.k_1 = tk.DoubleVar(master, 2.09)  # для тестовой: k1
        self.k_2 = tk.DoubleVar(master, 0.09 )  # для тестовой: k2
        self.q_1 = tk.DoubleVar(master, 0.3)  # для тестовой: q1
        self.q_2 = tk.DoubleVar(master, 0.09)  # для тестовой: q2
        self.f_1 = tk.DoubleVar(master, 1) # для тестовой: f1
        self.f_2 = tk.DoubleVar(master, np.sin(np.pi * 0.3)) # для тестовой: f2
        self.n = tk.IntVar(master, 100) # число разбиений
        self.accuracy = tk.DoubleVar(master, 0.00001) # точность для тестовой
        self.difference = tk.DoubleVar(master, 0.00001) # разность
        self.error = tk.DoubleVar(master, 0)  # точность
        self.difference_get = tk.DoubleVar(master, 0)  # разность в точке

        self.flag = tk.BooleanVar(master) #какая задача, True - Основная, False - Тестовая
        self.label = 'График зависимости температура стержня'

        self.create_widgets()

    def make_menu(self):
        mainmenu = Menu(self.master)
        self.master.config(menu=mainmenu)

        info = Menu(mainmenu, tearoff=0)
        info.add_command(label="Описание задачи", command = self.task_window)
        mainmenu.add_cascade(label="Информация", menu=info)

    def task_window(self):
        task = tk.Toplevel()
        task.title('Описание задачи')
        img = ImageTk.PhotoImage(Image.open("./task.jpg"))
        panel = tk.Label(task, image=img)
        panel.pack(side='bottom', fill='both', expand='yes')
        task.mainloop()

    def make_frame(self):
        splitting = Label(text = 'Число разбиений: ').grid(row=0, column=0)
        splitting = tk.Entry(highlightbackground='#cbcbcb', textvariable=self.n).grid(row=0, column=1, padx = (10, 0), pady = (10, 0))
        self.frame_top = LabelFrame(text="Справка")
        self.frame_top.grid(row=1, column=0, columnspan=2, padx = (10, 0), pady = (10, 0))

        n = Label(self.frame_top, text='Для решения тестовой задачи').grid(row=2, column=1, sticky='w')
        n = Label(self.frame_top, text='использована сетка с числом').grid(row=3, column=1, sticky='w')
        n = Label(self.frame_top, text='разбиений по x: ' + str(self.n.get())).grid(row=4, column=1, sticky='w')
        accuracy = Label(self.frame_top, text='Тестовая задача решена').grid(row=5, column=1, sticky='w')
        accuracy = Label(self.frame_top, text='с точностью: ' + str(self.accuracy.get())).grid(row=5, column=1, sticky='w')
        error = Label(self.frame_top, text='Максимально отклонение точного и').grid(row=6, column=1, sticky='w')
        error = Label(self.frame_top, text='приближенного решения наблидается').grid(row=7, column=1, sticky='w')
        error = Label(self.frame_top, text='в точке: ' + str(self.error.get())).grid(row=8, column=1, sticky='w')

        n = Label(self.frame_top, text='Для решения основной задачи').grid(row=9, column=1, sticky='w')
        n = Label(self.frame_top, text='использована сетка с числом').grid(row=10, column=1, sticky='w')
        n = Label(self.frame_top, text='разбиений по x: ' + str(self.n.get())).grid(row=11, column=1, sticky='w')
        difference = Label(self.frame_top, text='При пересчёте задачи с половинным').grid(row=12, column=1, sticky='w')
        difference = Label(self.frame_top, text='шагом максимальная разность').grid(row=13,column=1,sticky='w')
        difference = Label(self.frame_top, text='приближений составила: ' + str(self.difference.get())).grid(row=14, column=1, sticky='w')
        difference_get = Label(self.frame_top, text='и соответствует узлу x = ' + str(self.difference_get.get())).grid(row=15, column=1, sticky='w')

    def save(self):
        self.frame_top.destroy()
        self.make_frame()

    def create_notebook(self):
        notebook = ttk.Notebook()
        notebook.grid(row=0, column=2, sticky = 'n', rowspan = 4, pady = (10, 0), padx = (10, 10))
        self.set_nb_frames(notebook)
        notebook.add(self.main_frame, text='Основная')
        notebook.add(self.test_frame, text='Тестовая')

    def set_nb_frames(self, notebook):
        self.main_frame = ttk.Frame(notebook, width=900, height=400)
        self.test_frame = ttk.Frame(notebook, width=400, height=300)

    def create_widgets(self):
        self.make_menu()
        self.make_frame()
        self.create_notebook()
        execute1 = tk.Button(text='Решить тестовую задачу', bg='#ececec', highlightbackground='#ececec', command=self.execute_test).grid(
            row=17, column=0, columnspan=2, pady = (10, 10), padx = (10, 0), sticky = 'nwe')
        execute2 = tk.Button(text='Решить основную задачу', bg='#ececec', highlightbackground='#ececec', command=self.execute_main).grid(
            row=18, column=0, columnspan=2, pady=(10, 10), padx=(10, 0), sticky='nwe')

        self.reference_t = tk.Text(self.test_frame, height=5, width=70, highlightbackground='#cbcbcb')
        self.reference_t.grid(row=5, column=0, rowspan=3, padx=(10, 10), sticky='w')

        #self.create_table(self.main_frame)
        self.craete_table_test_start()

        #self.plotOnPlane(self.label, self.main_frame, [])
        self.plotOnPlane_start(self.label, self.test_frame)

    def dll_work(self):
        init_params = (c_double * 11)()
        init_params[0] = self.n.get()
        init_params[1] = self.flag

        dll = cdll.LoadLibrary("dll_for_py2//x64//Release//dll_for_py2.dll")
        dll.work_RK31R.argtypes = [POINTER(POINTER(c_double))]
        dll.work_RK31R.restype = None
        dll.del_mem.argtypes = [POINTER(POINTER(c_double))]
        dll.work_RK31R.restype = None

        p_test = {'x': 0, 'u': 1, 'v': 2, '|u-v|': 3}
        p_main = {'x': 0, 'V': 1, 'v2': 2, '|V-v2|': 3}
        d = POINTER(c_double)()
        _i = (c_int)()

        dll.work_RK31R(byref(d), byref(init_params), byref(_i))
        return p_test, p_main, d, _i
    def craete_table_test_start(self):
        self.table = ttk.Treeview(self.test_frame, show='headings', height=20)
        names=['№ узла', 'x', 'u(x)', 'v(x)', '|u(x) - v(x)|']
        self.table["columns"]=names
        self.table.grid(row=0, column=0)
        for i in names:
            self.table.column(i, anchor="w", width=110)
            self.table.heading(i, text=i, anchor='w')
    def create_table_test(self, ndata):
        cols = list(ndata.columns)
        self.table = ttk.Treeview(self.test_frame, show='headings', height=20)
        self.table["columns"] = cols
        self.table.grid(row=0, column=0, columnspan=2,sticky=tk.W)
        for i in cols:
            self.table.column(i, anchor="w", width=110)
            self.table.heading(i, text=i, anchor='w')
        for index, row in ndata.iterrows():
            self.table.insert("", 0, text=index, values=list(row))

    def scroll(self, place):
        scroll_bar1 = Scrollbar(place, orient=VERTICAL, command=self.table.yview)
        scroll_bar1.grid(row=0, column=1, sticky=tk.NS)
        self.table.configure(yscroll=scroll_bar1.set)
    def plotOnPlane_start(self, label, place):
        f = plt.figure(figsize=(8, 6), dpi=80, facecolor='#ececec')
        fig = plt.subplot(1, 1, 1)
        fig.set_title(label[0])
        fig.set_xlabel(label[1])
        fig.set_ylabel(label[2])
        fig.plot()
        self.create_form_graph(f, place)
    def plotOnPlane(self, label, place, ndata):

        f = plt.figure(figsize=(8, 6), dpi=80, facecolor='#ececec')
        fig = plt.subplot(1, 1, 1)
        fig.set_title(label)
        plt.grid()
        fig.plot(ndata['x'].values, ndata['v(x)'].values, label = "Численная траектория", color='r')
        fig.plot(ndata['x'].values, ndata['u(x)'].values, label = 'Истинная траектория', linestyle='--', color='b')
        fig.legend()
        self.create_form_graph(f, place)

    def create_form_graph(self, figure, place):
        canvas = FigureCanvasTkAgg(figure, place)
        canvas.get_tk_widget().grid(row=0, column=2)
        canvas.draw()

    def fill_graph(self, ndata):
        self.plotOnPlane(self.label, self.test_frame, ndata)

    def reference(self, ndata):
        self.reference_t.delete(1.0, END)
        xmax_error=0
        max_error=0
        for index, row in ndata.iterrows():
            if row['|u(x) - v(x)|']>max_error:
                max_error=row['|u(x) - v(x)|']
                xmax_error=row['x']

        self.reference_t.insert(1.0, 'Справка\n\n')
        self.reference_t.insert(2.0, 'Максимальная ошибка: ' + str(max_error) + ' и достигается в точке x = ' + str(xmax_error))
    def execute_test(self):
        self.flag = False
        #p_test, p_main, d, i = self.dll_work()
        #self.fill_table(p_test, d, i, self.test_frame)
        #self.fill_graph(p_test, d, i, self.ndata)
        #self.reference()
        self.result = test(self.n.get())
        self.note, self.ndata = self.result.Solution()
        self.fill_graph(self.ndata)
        self.create_table_test(self.ndata)
        self.reference(self.ndata)
        self.scroll(self.test_frame)



    def execute_main(self):
        self.flag = True
        p_test, p_main, d, i = self.dll_work()
        self.fill_table(p_main, d, i, self.main_frame)
        self.fill_graph(p_main, d, i)



root = tk.Tk()
gui = Interface(root)
root.mainloop()