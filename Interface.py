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
from test_task import test
from main_task import main



class Interface:
    def __init__(self, master):
        self.master = master  # инициализируем основное окно
        self.photo = tk.PhotoImage(file='logo.png')  # загрузка иконки приложения
        master.iconphoto(False, self.photo)  # установка иконки
        master.title('Лабораторная работа №2. Решение краевых задач для ОДУ. Вариант 3')  # заголовок
        master.configure(bg='#ececec')  # фон
        master.minsize(1200, 650)  # минимальный размер окна

        self.n = tk.IntVar(master, 400) # число разбиений

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
        self.frame_top = LabelFrame(text="Цель работы:")
        self.frame_top.grid(row=1, column=0, columnspan=2, padx = (10, 0), pady = (10, 0), sticky='nsew')

        n = Label(self.frame_top, text='Освоение методов численного').grid(row=2, column=1, sticky='w')
        n = Label(self.frame_top, text='решения краевых задач на').grid(row=3, column=1, sticky='w')
        n = Label(self.frame_top, text='примере первой краевой').grid(row=4, column=1, sticky='w')
        n = Label(self.frame_top, text='задачи для обыкновенного').grid(row=5, column=1, sticky='w')
        n = Label(self.frame_top, text='дифференциального уравнения').grid(row=6, column=1, sticky='w')
        n = Label(self.frame_top, text='(ОДУ) второго порядка с ').grid(row=7, column=1, sticky='w')
        n = Label(self.frame_top, text='разрывными коэффициентами. ').grid(row=8, column=1, sticky='w')
        n = Label(self.frame_top, text='Разработка, отладка и').grid(row=9, column=1, sticky='w')
        n = Label(self.frame_top, text='применение программных').grid(row=10, column=1, sticky='w')
        n = Label(self.frame_top, text='средств. Анализ').grid(row=11, column=1, sticky='w')
        n = Label(self.frame_top, text='сходимости и погрешности').grid(row=12, column=1, sticky='w')


    def save(self):
        self.frame_top.destroy()
        self.make_frame()

    def create_notebook(self):
        notebook = ttk.Notebook()
        notebook.grid(row=0, column=2, sticky = 'n', rowspan = 10, pady = (10, 0), padx = (10, 10))
        self.set_nb_frames(notebook)
        notebook.add(self.test_frame, text='Тестовая')
        notebook.add(self.main_frame, text='Основная')
        notebook.add(self.graph_frame, text='График погрешности')

    def set_nb_frames(self, notebook):
        self.main_frame = ttk.Frame(notebook, width=900, height=400)
        self.test_frame = ttk.Frame(notebook, width=900, height=400)
        self.graph_frame = ttk.Frame(notebook, width=900, height=400)

    def create_widgets(self):
        self.make_menu()
        self.make_frame()
        self.create_notebook()
        execute1 = tk.Button(text='Решить тестовую задачу', bg='#ececec', highlightbackground='#ececec', command=self.execute_test).grid(
            row=2, column=0, columnspan=2, pady = (10, 10), padx = (10, 0), sticky = 'nsew')
        execute2 = tk.Button(text='Решить основную задачу', bg='#ececec', highlightbackground='#ececec', command=self.execute_main).grid(
            row=3, column=0, columnspan=2, pady=(10, 10), padx=(10, 0), sticky='nsew')

        self.reference_t = tk.Text(self.test_frame, height=5, width=81, highlightbackground='#cbcbcb')
        self.reference_t.grid(row=5, column=0, rowspan=3, padx=(10, 10), pady = (10, 10), sticky='w')

        self.reference_m = tk.Text(self.main_frame, height=5, width=81, highlightbackground='#cbcbcb')
        self.reference_m.grid(row=5, column=0, rowspan=3, padx=(10, 10), pady = (10, 10), sticky='w')

        self.craete_table_start(self.test_frame)
        self.craete_table_start(self.main_frame)

        self.plotOnPlane_start(self.label, self.main_frame)
        self.plotOnPlane_start(self.label, self.test_frame)

    def craete_table_start(self, place):
        self.table = ttk.Treeview(place, show='headings', height=20)
        if place==self.test_frame:
            names=['№ узла', 'x', 'u(x)', 'v(x)', '|u(x) - v(x)|']
        else:
            names = ['№ узла', 'x', 'v(x)', 'v2(x2i)', '|v(x) - v2(x2i)|']
        self.table["columns"]=names
        self.table.grid(row=0, column=0, columnspan=2,padx=(10,), pady=(10,), sticky='wns')
        for i in names:
            self.table.column(i, anchor="w", width=130)
            self.table.heading(i, text=i, anchor='w')

    def create_table(self, ndata, place):
        cols = list(ndata.columns)
        self.table = ttk.Treeview(place, show='headings', height=20)
        self.table["columns"] = cols
        self.table.grid(row=0, column=0, columnspan=2, padx=(10, 10),pady=(10,), sticky='wns')
        for i in cols:
            self.table.column(i, anchor="w", width=130)
            self.table.heading(i, text=i, anchor='w')
        for index, row in ndata.iterrows():
            self.table.insert("", 100, text=index, values=list(row))

    def scroll(self, place):
        scroll_bar1 = Scrollbar(place, orient=VERTICAL, command=self.table.yview)
        scroll_bar1.grid(row=0, column=1, sticky=tk.NS)
        self.table.configure(yscroll=scroll_bar1.set)

    def plotOnPlane_start(self, label, place):
        f = plt.figure(figsize=(8, 6), dpi=80, facecolor='#ececec')
        fig = plt.subplot(1, 1, 1)
        fig.set_title(label)
        fig.plot()
        self.create_form_graph(f, place, 1)

    def plotOnPlane(self, label, place, ndata):
        f = plt.figure(figsize=(8, 6), dpi=80, facecolor='#ececec')
        fig = plt.subplot(1, 1, 1)
        fig.set_title(label)
        fig.set_xlabel('x')
        plt.grid()
        if place==self.test_frame:
            fig.set_ylabel('v(x)')
            fig.plot(ndata['x'].values, ndata['v(x)'].values, label = "Численная траектория", color='r')
            fig.plot(ndata['x'].values, ndata['u(x)'].values, label = 'Истинная траектория', linestyle='--', color='b')
            fig.legend()
            self.create_form_graph(f, place, 0)
        elif place==self.main_frame:
            fig.set_ylabel('v(x)')
            fig.plot(ndata['x'].values, ndata['v(x)'].values, label="Численная траектория", color='r')
            fig.legend()
            self.create_form_graph(f, place, 2)
        elif place==self.graph_frame:
            if self.flag == False:
                fig.set_ylabel('|u(x) - v(x)|')
                fig.set_title('График разности аналитического и численного решений')
                plt.grid()
                fig.plot(ndata['x'].values, ndata['|u(x) - v(x)|'].values, color='b')
                self.create_form_graph(f, place, 0)
            else:
                fig.set_ylabel('|v(x) - v2(x2i)|')
                fig.set_title('График разности аналитического и численного решений')
                plt.grid()
                fig.plot(ndata['x'].values, ndata['|v(x) - v2(x2i)|'].values, color='b')
                self.create_form_graph(f, place, 1)

    def create_form_graph(self, figure, place, g):
        canvas = FigureCanvasTkAgg(figure, place)
        if place==self.graph_frame:
            canvas.get_tk_widget().grid(row=0, column=g)
        else:
            canvas.get_tk_widget().grid(row=0, column=2)
        canvas.draw()

    def reference(self, ndata):
        xmax_error=0
        max_error=0
        if self.flag==True:
            self.reference_m.delete(1.0, END)
            for index, row in ndata.iterrows():
                if row['|v(x) - v2(x2i)|']>max_error:
                    max_error=row['|v(x) - v2(x2i)|']
                    xmax_error=row['x']
            self.reference_m.insert(1.0, 'Справка\n\n')
            self.reference_m.insert(2.0, 'Для решения задачи использована равномерная сетка счислом разбиений n = ' + str(self.n.get()))
            self.reference_m.insert(3.0, 'Максимальная погрешность: ' + str(max_error) + ' и наблюдается в точке x = ' + str(
                xmax_error))
        else:
            for index, row in ndata.iterrows():
                self.reference_t.delete(1.0, END)
                if row['|u(x) - v(x)|'] > max_error:
                    max_error = row['|u(x) - v(x)|']
                    xmax_error = row['x']

            self.reference_t.insert(1.0, 'Справка\n\n')
            self.reference_t.insert(2.0,
                                    'Для решения задачи использована равномерная сетка счислом разбиений n = ' + str(
                                        self.n.get()))
            self.reference_t.insert(3.0,
                                    'Максимальная погрешность: ' + str(max_error) + ' и наблюдается в точке x = ' + str(
                                        xmax_error))

    def execute_test(self):
        self.flag = False
        self.result = test(self.n.get())
        self.ndata = self.result.Solution()
        self.plotOnPlane(self.label, self.test_frame, self.ndata)
        self.create_table(self.ndata, self.test_frame)
        self.reference(self.ndata)
        self.scroll(self.test_frame)
        self.plotOnPlane(self.label, self.graph_frame, self.ndata)

    def execute_main(self):
        self.flag = True
        self.result = main(self.n.get())
        self.ndata1 = self.result.Solution()
        self.plotOnPlane(self.label, self.main_frame, self.ndata1)
        self.create_table(self.ndata1, self.main_frame)
        self.reference(self.ndata1)
        self.scroll(self.main_frame)
        self.plotOnPlane(self.label, self.graph_frame, self.ndata1)

root = tk.Tk()
gui = Interface(root)
root.mainloop()