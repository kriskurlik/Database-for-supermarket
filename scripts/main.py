# -*- coding: utf-8 -*-
"""
Talibov S. M., Goncharova K. V., brigade 4, BIV221
"""
import sys
import os
import tkinter as tk
import pandas as pd
import numpy as np
import matplotlib as mpl
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)

os.chdir("C:/work")
sys.path.append("./library/")

import text_reports as tr
import dataframe_manipulation as dm
import graphical_reports as gm


def light_theme():
    """
    Данная функция определяет цветовое оформление приложения для режима
    "Светлая тема"
    """
    global light, dark, white, text_color
    light = rgb_hack((170,207,208))
    dark = rgb_hack((121,168,169))
    white = rgb_hack((244,247,247))
    text_color = rgb_hack((0,0,0))

def dark_theme():
    """
    Данная функция определяет цветовое оформление приложения для режима
    "Темная тема"
    """
    global light, dark, white, text_color
    light = rgb_hack((57,62,70))
    dark = rgb_hack((34,40,49))
    white = rgb_hack((238,238,238))
    text_color = rgb_hack((238,238,238))

def Button_1(master, text):
    """
    Аргументы:
        master - виджет, родительский элемент кнопки
        text - строка, которая будет текстом кнопки

    Результат:
        button - объект класса tkinter.Button()

    Данная функция является шаблоном для создания кнопок
    """
    button=tk.Button(master, text=text)
    button.config(bg = white, fg="black", height = 1, width = 25)
    return button

def Button_2(master, text):
    """
    Аргументы:
        master - виджет, родительский элемент кнопки
        text - строка, которая будет текстом кнопки

    Результат:
        button - объект класса tkinter.Button()

    Данная функция является шаблоном для создания кнопок
    """
    button=tk.Button(master, text=text)
    button.config(bg = white, fg="black", height = 2, width = 25)
    return button

def Button_3(master, text, color):
    """
    Аргументы:
        master - виджет, родительский элемент кнопки
        text - строка, которая будет текстом кнопки
        color - цвет в шестнадцатеричном формате

    Результат:
        button - объект класса tkinter.Button()

    Данная функция является шаблоном для создания кнопок
    """
    button=tk.Button(master, text=text)
    button.config(bg = white, fg=color, height = 2, width = 25)
    return button

def Button_4(master, text):
    button=tk.Button(master, text=text)
    button.config(bg = white, fg="black", height = 1, width = 30)
    return button

def rgb_hack(rgb):
    """
    Использование RGB формата для цветов
    https://docs.python.org/3/library/stdtypes.html#old-string-formatting
    """
    return "#%02x%02x%02x" % rgb


# Функции для справочников

def f1(help_spr):
    """
    Функция, создающая окно справки о справочниках
    """
    root1=tk.Tk()
    root1.geometry('1300x200+100+80')
    root1.title("Справка")
    reference_text = tk.Label(root1,
                              text=help_spr,
                              font=('Colibry', 12, 'bold'),
                              fg=rgb_hack((42,54,59)))
    reference_text.grid(column=0, row=1)
    root1.mainloop()


def spr1(hsb, vsb):
    """
    Аргументы:
        hsb - объкет класса tkinter.Scrollbar()
        vsb - объкет класса tkinter.Scrollbar()

    Функция для отображения окна взаимодействия со справочником
    goods_store_amount
    """
    global menu1_2
    global frames_s
    global frame
    # global frames_all
    for widget in frames_s.winfo_children():
        if not widget==frame:
            widget.destroy()

    goods_provider_price = pd.read_pickle('./data/goods_provider_price.pkl')
    goods_store_amount = pd.read_pickle('./data/goods_store_amount.pkl')
    store_address = pd.read_pickle('./data/store_address.pkl')


    def dataframe_display():
        """
        Функция для отображения справочника goods_store_amount и кнопок его
        редактирования
        """
        columns = goods_store_amount.columns
        height = goods_store_amount.shape[0]
        width = goods_store_amount.shape[1]

        labelframe = tk.LabelFrame(frames_s, text="Товар_магазин_количество",
                                       bg=dark, fg=text_color, width=450,
                                       height=210)
        labelframe.place(x=10, y=5)
        gsa_canvas = tk.Canvas(labelframe,
                               scrollregion=(0, 0, 220 + 220 * width,
                                             20 + 20 * height),
                               highlightthickness = 0, bg = dark)
        hsb['command'] = gsa_canvas.xview
        vsb['command'] = gsa_canvas.yview
        gsa_canvas.pack(side="left",expand=True,fill="both")
        gsa_canvas.config(width = 450, height = 220)
        hsb.pack(side="bottom", fill="x")
        vsb.pack(side="right", fill="y")
        gsa_canvas.config(xscrollcommand=hsb.set, yscrollcommand=vsb.set)
        pnt = np.empty(shape=(width, height), dtype="O")
        vrs = np.empty(shape=(width, height), dtype="O")
        for i in range(width):
            for j in range(height):
                vrs[i, j] = tk.StringVar()
        for i in range(width):
            a = tk.Label(gsa_canvas, text = columns[i], bg=dark,
                         fg=text_color)
            gsa_canvas.create_window(220 * i +100, 0, height = 20, width = 220,
                                anchor = "nw", window = a)
        for i in range(height):
            a = tk.Label(gsa_canvas, text = i + 1, bg=dark,
                         fg=text_color)
            gsa_canvas.create_window(0, 20 * (i + 1), height = 20, width = 100,
                                anchor = "nw", window = a)
        for i in range(width):
            for j in range(height):
                pnt[i, j] = tk.Entry(gsa_canvas, textvariable = vrs[i, j],
                                     justify='center')
                gsa_canvas.create_window(100 + 220 * i, 20 + 20 * j,
                                         window = pnt[i, j], anchor = 'nw',
                                         height = 20, width = 220)
        for i in range(width):
            for j in range(height):
                cnt = goods_store_amount.iloc[j, i]
                vrs[i, j].set(str(cnt))


    def row_addition():
        """
        Функция для добавления записи в справочник
        """
        addition_root = tk.Tk()
        addition_root.title("Добавление записи")

        labels = goods_store_amount.columns
        for i in range(len(labels)):
            a = tk.Label(addition_root, text = labels[i])
            a.grid(column = i, row = 0)

        for i in range(len(labels)):
            b = tk.Entry(addition_root)
            b.grid(column = i, row = 1)

        status_label = tk.Label(addition_root, text="Статус:")
        status_label.grid(column = 3, row = 2)

        def button_press():
            """
            Функция для подтверждения добавления записи
            """
            new_row = []
            for widget in addition_root.winfo_children():
                if isinstance(widget, tk.Entry):
                    new_row.append(widget.get())

            for i in range(len(new_row)):
                try:
                    new_row[i] = int(new_row[i])
                except ValueError:
                    new_row[i] = str(new_row[i])
            status = dm.add_row_to_gsa(goods_store_amount, store_address,
                                       goods_provider_price, new_row)
            status_label.config(text = "Статус: " + status)
            dataframe_display()

        button = tk.Button(addition_root, text="Добавить",
                           command = button_press)
        button.grid(column = 3, row = 3)


    def row_deletion():
        """
        Функция для удаления записи из справочника
        """
        deletion_root = tk.Tk()
        deletion_root.title("Удаление записи")
        deletion_root.geometry('400x90+100+100')

        label = tk.Label(deletion_root, text = "Номер удаляемого ряда")
        label.grid(column = 0, row = 0)
        entry = tk.Entry(deletion_root)
        entry.grid(column = 0, row = 1)
        status_label = tk.Label(deletion_root, text = "Статус:")
        status_label.grid(column = 0, row = 2)


        def button_press():
            """
            Функция для подтверждения удаления записи
            """
            number = entry.get()
            try:
                number = int(number)
                number -= 1
            except ValueError:
                number = str(number)
            status = dm.delete_row_from_gsa(goods_store_amount, number)
            status_label.config(text = "Статус: " + status)
            dataframe_display()

        button = tk.Button(deletion_root, text="Удалить",
                           command = button_press)
        button.grid(column = 0, row = 3)



    dataframe_display()

    menu1_1_save = lambda: dm.save_changes(goods_store_amount,
                                           "goods_store_amount.pkl")
    menu1_1.entryconfigure(0, command = menu1_1_save)
    menu1_1_saveas = lambda: dm.save_as(goods_store_amount)
    menu1_1.entryconfigure(1, command = menu1_1_saveas)
    menu1_2_excel = lambda: dm.save_to_excel(goods_store_amount,
                                             "goods_store_amount.xlsx",
                                             False)
    menu1_2.entryconfigure(0, command = menu1_2_excel)

    menu1_2_pickle = lambda: dm.save_to_pickle(goods_store_amount,
                                               "goods_store_amount.pkl")
    menu1_2.entryconfigure(1, command = menu1_2_pickle)

    button8 = Button_4(frame, "Добавить запись")
    button8.config(command=row_addition)
    button8.place(x = 5, y = 240, anchor = 'nw')

    button9 = Button_4(frame, "Удалить запись")
    button9.config(command=row_deletion)
    button9.place(x = 235, y = 240, anchor = 'nw')


def spr2(hsb, vsb):
    """
    Аргументы:
        hsb - объкет класса tkinter.Scrollbar()
        vsb - объкет класса tkinter.Scrollbar()

    Функция для отображения окна взаимодействия со справочником
    goods_provider_price
    """
    global menu1_2
    global frames_s
    global frame
    # global frames_all
    for widget in frames_s.winfo_children():
        if not widget==frame:
            widget.destroy()

    goods_provider_price = pd.read_pickle('./data/goods_provider_price.pkl')
    goods_store_amount = pd.read_pickle('./data/goods_store_amount.pkl')
    provider_contacts = pd.read_pickle('./data/provider_contacts.pkl')


    def dataframe_display():
        """
        Функция для отображения справочника goods_provider_price и кнопок его
        редактирования
        """
        columns = goods_provider_price.columns
        height = goods_provider_price.shape[0]
        width = goods_provider_price.shape[1]

        labelframe = tk.LabelFrame(frames_s, text="Товар_поставщик_цена",
                                       bg=dark, fg=text_color, width=450,
                                       height=220)
        labelframe.place(x=10, y=5)
        gsa_canvas = tk.Canvas(labelframe,
                               scrollregion=(0, 0, 220 + 220 * width,
                                             20 + 20 * height),
                               highlightthickness = 0, bg = dark)
        hsb['command'] = gsa_canvas.xview
        vsb['command'] = gsa_canvas.yview
        gsa_canvas.pack(side="left",expand=True,fill="both")
        gsa_canvas.config(width = 450, height = 220)
        hsb.pack(side="bottom", fill="x")
        vsb.pack(side="right", fill="y")
        gsa_canvas.config(xscrollcommand=hsb.set, yscrollcommand=vsb.set)
        pnt = np.empty(shape=(width, height), dtype="O")
        vrs = np.empty(shape=(width, height), dtype="O")
        for i in range(width):
            for j in range(height):
                vrs[i, j] = tk.StringVar()
        for i in range(width):
            a = tk.Label(gsa_canvas, text = columns[i], bg=dark,
                         fg=text_color)
            gsa_canvas.create_window(100 + 220 * i, 0, height = 20, width = 220,
                                anchor = "nw", window = a)
        for i in range(height):
            a = tk.Label(gsa_canvas, text = i + 1, bg=dark,
                         fg=text_color)
            gsa_canvas.create_window(0, 20 * (i + 1), height = 20, width = 100,
                                anchor = "nw", window = a)
        for i in range(width):
            for j in range(height):
                pnt[i, j] = tk.Entry(gsa_canvas, textvariable = vrs[i, j],
                                     justify='center')
                gsa_canvas.create_window(100 + 220 * i, 20 + 20 * j,
                                         window = pnt[i, j], anchor = 'nw',
                                         height = 20, width = 220)
        for i in range(width):
            for j in range(height):
                cnt = goods_provider_price.iloc[j, i]
                vrs[i, j].set(str(cnt))


    def row_addition():
        """
        Функция для добавления записи в справочник
        """
        addition_root = tk.Tk()
        addition_root.title("Добавление записи")

        labels = goods_provider_price.columns
        for i in range(len(labels)):
            a = tk.Label(addition_root, text = labels[i])
            a.grid(column = i, row = 0)

        for i in range(len(labels)):
            b = tk.Entry(addition_root)
            b.grid(column = i, row = 1)

        status_label = tk.Label(addition_root, text="Статус:")
        status_label.grid(column = 3, row = 2)

        def button_press():
            """
            Функция для подтверждения добавления записи
            """
            new_row = []
            for widget in addition_root.winfo_children():
                if isinstance(widget, tk.Entry):
                    new_row.append(widget.get())

            for i in range(len(new_row)):
                try:
                    new_row[i] = int(new_row[i])
                except ValueError:
                    new_row[i] = str(new_row[i])
            status = dm.add_row_to_gpp(goods_provider_price, provider_contacts,
                                       new_row)
            status_label.config(text = "Статус: " + status)
            dataframe_display()

        button = tk.Button(addition_root, text="Добавить",
                           command = button_press)
        button.grid(column = 3, row = 3)


    def row_deletion():
        """
        Функция для удаления записи из справочника
        """
        deletion_root = tk.Tk()
        deletion_root.title("Удаление записи")
        deletion_root.geometry('400x90+100+100')

        label = tk.Label(deletion_root, text = "Номер удаляемого ряда")
        label.grid(column = 0, row = 0)
        entry = tk.Entry(deletion_root)
        entry.grid(column = 0, row = 1)
        status_label = tk.Label(deletion_root, text = "Статус:")
        status_label.grid(column = 0, row = 2)


        def button_press():
            """
            Функция для подтверждения удаления записи
            """
            number = entry.get()
            try:
                number = int(number)
                number -= 1
            except ValueError:
                number = str(number)
            status = dm.delete_row_from_gpp(goods_provider_price,
                                            goods_store_amount, number)
            status_label.config(text = "Статус: " + status)
            dataframe_display()

        button = tk.Button(deletion_root, text="Удалить",
                           command = button_press)
        button.grid(column = 0, row = 3)


    dataframe_display()

    menu1_1_save = lambda: dm.save_changes(goods_provider_price,
                                           "goods_provider_price.pkl")
    menu1_1.entryconfigure(0, command = menu1_1_save)
    menu1_1_saveas = lambda: dm.save_as(goods_provider_price)
    menu1_1.entryconfigure(1, command = menu1_1_saveas)
    menu1_2_excel = lambda: dm.save_to_excel(goods_provider_price,
                                             "goods_provider_price.xlsx",
                                             False)
    menu1_2.entryconfigure(0, command = menu1_2_excel)

    menu1_2_pickle = lambda: dm.save_to_pickle(goods_provider_price,
                                               "goods_provider_price.pkl")
    menu1_2.entryconfigure(1, command = menu1_2_pickle)

    button8 = Button_4(frame, "Добавить запись")
    button8.config(command=row_addition)
    button8.place(x = 5, y = 240, anchor = 'nw')

    button9 = Button_4(frame, "Удалить запись")
    button9.config(command=row_deletion)
    button9.place(x = 235, y = 240, anchor = 'nw')


def spr3(hsb, vsb):
    """
    Аргументы:
        hsb - объкет класса tkinter.Scrollbar()
        vsb - объкет класса tkinter.Scrollbar()

    Функция для отображения окна взаимодействия со справочником
    goods_store_amount
    """
    global menu1_2
    global frames_s
    global frame
    # global frames_all
    for widget in frames_s.winfo_children():
        if not widget==frame:
            widget.destroy()

    goods_provider_price = pd.read_pickle('./data/goods_provider_price.pkl')
    provider_contacts = pd.read_pickle('./data/provider_contacts.pkl')


    def dataframe_display():
        """
        Функция для отображения справочника provider_contacts и кнопок его
        редактирования
        """
        columns = provider_contacts.columns
        height = provider_contacts.shape[0]
        width = provider_contacts.shape[1]

        labelframe = tk.LabelFrame(frames_s, text="Поставщик_контакты",
                                       bg=dark, fg=text_color, width=450,
                                       height=220)
        labelframe.place(x=10, y=5)
        gsa_canvas = tk.Canvas(labelframe,
                               scrollregion=(0, 0, 220 + 220 * width,
                                             20 + 20 * height),
                               highlightthickness = 0, bg = dark)
        hsb['command'] = gsa_canvas.xview
        vsb['command'] = gsa_canvas.yview
        gsa_canvas.pack(side="left",expand=True,fill="both")
        gsa_canvas.config(width = 450, height = 220)
        hsb.pack(side="bottom", fill="x")
        vsb.pack(side="right", fill="y")
        gsa_canvas.config(xscrollcommand=hsb.set, yscrollcommand=vsb.set)
        pnt = np.empty(shape=(width, height), dtype="O")
        vrs = np.empty(shape=(width, height), dtype="O")
        for i in range(width):
            for j in range(height):
                vrs[i, j] = tk.StringVar()
        for i in range(width):
            a = tk.Label(gsa_canvas, text = columns[i], bg=dark,
                         fg=text_color)
            gsa_canvas.create_window(100 + 220 * i, 0, height = 20, width = 220,
                                anchor = "nw", window = a)
        for i in range(height):
            a = tk.Label(gsa_canvas, text = i + 1, bg=dark,
                         fg=text_color)
            gsa_canvas.create_window(0, 20 * (i + 1), height = 20, width = 100,
                                anchor = "nw", window = a)
        for i in range(width):
            for j in range(height):
                pnt[i, j] = tk.Entry(gsa_canvas, textvariable = vrs[i, j],
                                     justify='center')
                gsa_canvas.create_window(100 + 220 * i, 20 + 20 * j,
                                         window = pnt[i, j], anchor = 'nw',
                                         height = 20, width = 220)
        for i in range(width):
            for j in range(height):
                cnt = provider_contacts.iloc[j, i]
                vrs[i, j].set(str(cnt))


    def row_addition():
        """
        Функция для добавления записи в справочник
        """
        addition_root = tk.Tk()
        addition_root.title("Добавление записи")

        labels = provider_contacts.columns
        for i in range(len(labels)):
            a = tk.Label(addition_root, text = labels[i])
            a.grid(column = i, row = 0)

        for i in range(len(labels)):
            b = tk.Entry(addition_root)
            b.grid(column = i, row = 1)

        status_label = tk.Label(addition_root, text="Статус:")
        status_label.grid(column = 1, row = 2)

        def button_press():
            """
            Функция для подтверждения добавления записи
            """
            new_row = []
            for widget in addition_root.winfo_children():
                if isinstance(widget, tk.Entry):
                    new_row.append(widget.get())

            for i in range(len(new_row)):
                try:
                    new_row[i] = int(new_row[i])
                except ValueError:
                    new_row[i] = str(new_row[i])
            status = dm.add_row_to_pc(provider_contacts, new_row)
            status_label.config(text = "Статус: " + status)
            dataframe_display()

        button = tk.Button(addition_root, text="Добавить",
                           command = button_press)
        button.grid(column = 1, row = 3)


    def row_deletion():
        """
        Функция для удаления записи из справочника
        """
        deletion_root = tk.Tk()
        deletion_root.title("Удаление записи")
        deletion_root.geometry('400x90+100+100')

        label = tk.Label(deletion_root, text = "Номер удаляемого ряда")
        label.grid(column = 0, row = 0)
        entry = tk.Entry(deletion_root)
        entry.grid(column = 0, row = 1)
        status_label = tk.Label(deletion_root, text = "Статус:")
        status_label.grid(column = 0, row = 2)


        def button_press():
            """
            Функция для подтверждения удаления записи
            """
            number = entry.get()
            try:
                number = int(number)
                number -= 1
            except ValueError:
                number = str(number)
            status = dm.delete_row_from_pc(provider_contacts,
                                           goods_provider_price, number)
            status_label.config(text = "Статус: " + status)
            dataframe_display()

        button = tk.Button(deletion_root, text="Удалить",
                           command = button_press)
        button.grid(column = 0, row = 3)



    dataframe_display()

    menu1_1_save = lambda: dm.save_changes(provider_contacts,
                                           "provider_contacts.pkl")
    menu1_1.entryconfigure(0, command = menu1_1_save)
    menu1_1_saveas = lambda: dm.save_as(provider_contacts)
    menu1_1.entryconfigure(1, command = menu1_1_saveas)
    menu1_2_excel = lambda: dm.save_to_excel(provider_contacts,
                                             "provider_contacts.xlsx",
                                             False)
    menu1_2.entryconfigure(0, command = menu1_2_excel)

    menu1_2_pickle = lambda: dm.save_to_pickle(provider_contacts,
                                               "provider_contacts.pkl")
    menu1_2.entryconfigure(1, command = menu1_2_pickle)

    button8 = Button_4(frame, "Добавить запись")
    button8.config(command=row_addition)
    button8.place(x = 5, y = 240, anchor = 'nw')

    button9 = Button_4(frame, "Удалить запись")
    button9.config(command=row_deletion)
    button9.place(x = 235, y = 240, anchor = 'nw')


def spr4(hsb, vsb):
    """
    Аргументы:
        hsb - объкет класса tkinter.Scrollbar()
        vsb - объкет класса tkinter.Scrollbar()

    Функция для отображения окна взаимодействия со справочником
    goods_store_amount
    """
    global menu1_2
    global frames_s
    global frame
    # global frames_all
    for widget in frames_s.winfo_children():
        if not widget==frame:
            widget.destroy()

    goods_store_amount = pd.read_pickle('./data/goods_store_amount.pkl')
    store_address = pd.read_pickle('./data/store_address.pkl')


    def dataframe_display():
        """
        Функция для отображения справочника store_address и кнопок его
        редактирования
        """
        columns = store_address.columns
        height = store_address.shape[0]
        width = store_address.shape[1]

        labelframe = tk.LabelFrame(frames_s, text="Магазин_адрес",
                                       bg=dark, fg=text_color, width=450,
                                       height=220)
        labelframe.place(x=10, y=5)
        gsa_canvas = tk.Canvas(labelframe,
                               scrollregion=(0, 0, 220 + 220 * width,
                                             20 + 20 * height),
                               highlightthickness = 0, bg = dark)
        hsb['command'] = gsa_canvas.xview
        vsb['command'] = gsa_canvas.yview
        gsa_canvas.pack(side="left",expand=True,fill="both")
        gsa_canvas.config(width = 450, height = 220)
        hsb.pack(side="bottom", fill="x")
        vsb.pack(side="right", fill="y")
        gsa_canvas.config(xscrollcommand=hsb.set, yscrollcommand=vsb.set)
        pnt = np.empty(shape=(width, height), dtype="O")
        vrs = np.empty(shape=(width, height), dtype="O")
        for i in range(width):
            for j in range(height):
                vrs[i, j] = tk.StringVar()
        for i in range(width):
            a = tk.Label(gsa_canvas, text = columns[i], bg=dark,
                         fg=text_color)
            gsa_canvas.create_window(100 + 220 * i, 0, height = 20, width = 220,
                                anchor = "nw", window = a)
        for i in range(height):
            a = tk.Label(gsa_canvas, text = i + 1, bg=dark,
                         fg=text_color)
            gsa_canvas.create_window(0, 20 * (i + 1), height = 20, width = 100,
                                anchor = "nw", window = a)
        for i in range(width):
            for j in range(height):
                pnt[i, j] = tk.Entry(gsa_canvas, textvariable = vrs[i, j],
                                     justify='center')
                gsa_canvas.create_window(100 + 220 * i, 20 + 20 * j,
                                         window = pnt[i, j], anchor = 'nw',
                                         height = 20, width = 220)
        for i in range(width):
            for j in range(height):
                cnt = store_address.iloc[j, i]
                vrs[i, j].set(str(cnt))


    def row_addition():
        """
        Функция для добавления записи в справочник
        """
        addition_root = tk.Tk()
        addition_root.title("Добавление записи")

        labels = store_address.columns
        for i in range(len(labels)):
            a = tk.Label(addition_root, text = labels[i])
            a.grid(column = i, row = 0)

        for i in range(len(labels)):
            b = tk.Entry(addition_root)
            b.grid(column = i, row = 1)
            if i == 1:
                b.config(width = 200)

        status_label = tk.Label(addition_root, text="Статус:")
        status_label.grid(column = 1, row = 2)

        def button_press():
            """
            Функция для подтверждения добавления записи
            """
            new_row = []
            for widget in addition_root.winfo_children():
                if isinstance(widget, tk.Entry):
                    new_row.append(widget.get())

            for i in range(len(new_row)):
                try:
                    new_row[i] = int(new_row[i])
                except ValueError:
                    new_row[i] = str(new_row[i])
            status = dm.add_row_to_sa(store_address, new_row)
            status_label.config(text = "Статус: " + status)
            dataframe_display()

        button = tk.Button(addition_root, text="Добавить",
                           command = button_press)
        button.grid(column = 1, row = 3)


    def row_deletion():
        """
        Функция для удаления записи из справочника
        """
        deletion_root = tk.Tk()
        deletion_root.title("Удаление записи")
        deletion_root.geometry('400x90+100+100')

        label = tk.Label(deletion_root, text = "Номер удаляемого ряда")
        label.grid(column = 0, row = 0)
        entry = tk.Entry(deletion_root)
        entry.grid(column = 0, row = 1)
        status_label = tk.Label(deletion_root, text = "Статус:")
        status_label.grid(column = 0, row = 2)


        def button_press():
            """
            Функция для подтверждения удаления записи
            """
            number = entry.get()
            try:
                number = int(number)
                number -= 1
            except ValueError:
                number = str(number)
            status = dm.delete_row_from_sa(store_address, goods_store_amount,
                                           number)
            status_label.config(text = "Статус: " + status)
            dataframe_display()

        button = tk.Button(deletion_root, text="Удалить",
                           command = button_press)
        button.grid(column = 0, row = 3)


    dataframe_display()

    menu1_1_save = lambda: dm.save_changes(store_address,
                                           "store_address.pkl")
    menu1_1.entryconfigure(0, command = menu1_1_save)
    menu1_1_saveas = lambda: dm.save_as(store_address)
    menu1_1.entryconfigure(1, command = menu1_1_saveas)
    menu1_2_excel = lambda: dm.save_to_excel(store_address,
                                             "store_address.xlsx",
                                             False)
    menu1_2.entryconfigure(0, command = menu1_2_excel)

    menu1_2_pickle = lambda: dm.save_to_pickle(store_address,
                                               "store_address.pkl")
    menu1_2.entryconfigure(1, command = menu1_2_pickle)

    button8 = Button_4(frame, "Добавить запись")
    button8.config(command=row_addition)
    button8.place(x = 5, y = 240, anchor = 'nw')

    button9 = Button_4(frame, "Удалить запись")
    button9.config(command=row_deletion)
    button9.place(x = 235, y = 240, anchor = 'nw')


# функции для текстовых отчетов
def f2(help_text):
    """
    Функция, создающая окно справки для текстовых отчетов
    """
    root1=tk.Tk()
    root1.geometry('1450x300+100+80')
    root1.title("Справка")
    reference_text = tk.Label(root1, text=help_text,
                              font=('Colibry', 12, 'bold'),
                              fg=rgb_hack((42,54,59)))
    reference_text.grid(column=0, row=1)
    root1.mainloop()

def tab_report(master, hsb, vsb): # Формирование вкладки Отчет
    """
    Аргументы:
        master - виджет
        hsb, vsb - объекты tkinter.Scrollbar()

    Функция, создающая вкладку "Отчет" в меню окна текстовых отчетов
    """
    global root
    menu3 = tk.Menu(root, tearoff=0)
    menu3.add_command(label="Отчет 1", command=lambda: report_1(hsb, vsb))
    menu3.add_command(label="Отчет 2", command=lambda: report_2(hsb, vsb))
    menu3.add_command(label="Отчет 3", command=lambda: report_3(hsb, vsb))
    menu3.add_command(label="Сводная таблица 1",
                      command=lambda: pivot_1(hsb, vsb))
    menu3.add_command(label="Сводная таблица 2",
                      command=lambda: pivot_2(hsb, vsb))
    menu3.add_command(label="Сводная таблица 3",
                      command=lambda: pivot_3(hsb, vsb))
    master.add_cascade(label="Отчет", menu=menu3)


def report_1(hsb, vsb):
    """
    Аргументы:
        hsb, vsb - объекты tkinter.Scrollbar()

    Данная функция открывает окно отчета goods_by_provider
    """
    global menu2_1, menu2_2, frames_t, frame1
    for widget in frames_t.winfo_children():
        if not widget==frame1:
            widget.destroy()

    hsb.pack_forget()
    vsb.pack_forget()

    # Формирование отчета
    gpp = pd.read_pickle('./data/goods_provider_price.pkl')
    gsa = pd.read_pickle('./data/goods_store_amount.pkl')
    pc = pd.read_pickle('./data/provider_contacts.pkl')
    sa = pd.read_pickle('./data/store_address.pkl')
    merged_table = dm.dataframe_merger(gpp, pc, gsa, sa)

    merged_table = dm.create_margin_column(merged_table)

    canvas4 = tk.Canvas(frames_t, bg=dark, width=180, height=20,
                        highlightthickness=0)
    canvas4.place(x=510, y=25)
    text_entry = tk.Label(frames_t, text="Поставщик", bg=dark, fg=text_color)
    text_entry.place(x=510, y=25)
    lb = tk.Listbox(frames_t, selectmode=tk.EXTENDED, height=9, width=25,
                    fg='black', font=("Times 14", 10))
    lst = pc["Поставщик"].unique()
    for i in lst:
        lb.insert(tk.END, i)
    lb.place(x=510, y=45)


    def create_report():
        """
        Данная функция генерирует таблицу отчета
        """
        global menu2_2

        w = lb.curselection()
        providers = [pc.at[k, "Поставщик"] for k in w]
        report_frame = tr.goods_by_provider(merged_table, providers)

        columns = report_frame.columns

        height = report_frame.shape[0]
        width = report_frame.shape[1]

        labelframe = tk.LabelFrame(frames_t, text="Товар_по_поставщикам",
                                       bg=dark, fg=text_color, width=450,
                                       height=250)
        labelframe.place(x=10, y=5)
        cr_canvas = tk.Canvas(labelframe,
                              scrollregion=(0, 0, 220 + 220 * width,
                                            20 + 20 * height),
                              highlightthickness = 0, bg = dark)
        hsb['command'] = cr_canvas.xview
        vsb['command'] = cr_canvas.yview
        cr_canvas.pack(side="left",expand=True,fill="both")
        cr_canvas.config(width = 450, height = 250)
        hsb.pack(side="bottom", fill="x")
        vsb.pack(side="right", fill="y")
        cr_canvas.config(xscrollcommand=hsb.set, yscrollcommand=vsb.set)

        pnt = np.empty(shape=(width, height), dtype="O")
        vrs = np.empty(shape=(width, height), dtype="O")
        for i in range(width):
            for j in range(height):
                vrs[i, j] = tk.StringVar()
        for i in range(width):
            a = tk.Label(cr_canvas, text = columns[i], bg=dark,
                         fg=text_color)
            cr_canvas.create_window(0 + 220 * i, 0, height = 20, width = 220,
                                anchor = "nw", window = a)
        for i in range(width):
            for j in range(height):
                pnt[i, j] = tk.Entry(cr_canvas, textvariable = vrs[i, j],
                                     justify='center')
                cr_canvas.create_window(0 + 220 * i, 20 + 20 * j,
                                         window = pnt[i, j], anchor = 'nw',
                                         height = 20, width = 220)
        for i in range(width):
            for j in range(height):
                cnt = report_frame.iloc[j, i]
                vrs[i, j].set(str(cnt))

        menu2_1_saveas = lambda: dm.save_as(report_frame)
        menu2_1.entryconfigure(0, command = menu2_1_saveas)
        menu2_2_excel = lambda: dm.save_to_excel(report_frame,
                                                 "goods_by_provider.xlsx",
                                                 False)
        menu2_2.entryconfigure(0, command = menu2_2_excel)

        menu2_2_pickle = lambda: dm.save_to_pickle(report_frame,
                                                   "goods_by_provider.pkl")
        menu2_2.entryconfigure(1, command = menu2_2_pickle)

    button41= Button_1(frames_t, text="Сформировать")
    button41.config(command=create_report)
    button41.place(x=510, y=220)


def report_2(hsb, vsb):
    """
    Аргументы:
        hsb, vsb - объекты tkinter.Scrollbar()

    Данная функция открывает окно отчета store_by_address
    """
    global menu2_2, frames_t, frame1
    for widget in frames_t.winfo_children():
        if not widget==frame1:
            widget.destroy()

    hsb.pack_forget()
    vsb.pack_forget()
    # Формирование отчета
    gpp = pd.read_pickle('./data/goods_provider_price.pkl')
    gsa = pd.read_pickle('./data/goods_store_amount.pkl')
    pc = pd.read_pickle('./data/provider_contacts.pkl')
    sa = pd.read_pickle('./data/store_address.pkl')
    merged_table = dm.dataframe_merger(gpp, pc, gsa, sa)

    merged_table = dm.create_margin_column(merged_table)


    def create_report():
        """
        Данная функция генерирует таблицу отчета
        """
        global menu2_2

        place = entry.get()
        report_frame = tr.find_store_by_address(merged_table, place)

        columns = report_frame.columns

        height = report_frame.shape[0]
        width = report_frame.shape[1]

        labelframe = tk.LabelFrame(frames_t, text="Магазин_по_адресу",
                                       bg=dark, fg=text_color, width=450,
                                       height=250)
        labelframe.place(x=10, y=5)
        cr_canvas = tk.Canvas(labelframe,
                              scrollregion=(0, 0, 220 + 220 * width,
                                            20 + 20 * height),
                              highlightthickness = 0, bg = dark)
        hsb['command'] = cr_canvas.xview
        vsb['command'] = cr_canvas.yview
        cr_canvas.pack(side="left",expand=True,fill="both")
        cr_canvas.config(width = 450, height = 250)
        hsb.pack(side="bottom", fill="x")
        vsb.pack(side="right", fill="y")
        cr_canvas.config(xscrollcommand=hsb.set, yscrollcommand=vsb.set)

        pnt = np.empty(shape=(width, height), dtype="O")
        vrs = np.empty(shape=(width, height), dtype="O")
        for i in range(width):
            for j in range(height):
                vrs[i, j] = tk.StringVar()
        for i in range(width):
            a = tk.Label(cr_canvas, text = columns[i], bg=dark,
                         fg=text_color)
            cr_canvas.create_window(0 + 220 * i, 0, height = 20, width = 220,
                                anchor = "nw", window = a)
        for i in range(width):
            for j in range(height):
                pnt[i, j] = tk.Entry(cr_canvas, textvariable = vrs[i, j],
                                     justify='center')
                cr_canvas.create_window(0 + 220 * i, 20 + 20 * j,
                                         window = pnt[i, j], anchor = 'nw',
                                         height = 20, width = 220)
        for i in range(width):
            for j in range(height):
                cnt = report_frame.iloc[j, i]
                vrs[i, j].set(str(cnt))

        menu2_1_saveas = lambda: dm.save_as(report_frame)
        menu2_1.entryconfigure(0, command = menu2_1_saveas)
        menu2_2_excel = lambda: dm.save_to_excel(report_frame,
                                                 "store_by_address.xlsx",
                                                 False)
        menu2_2.entryconfigure(0, command = menu2_2_excel)

        menu2_2_pickle = lambda: dm.save_to_pickle(report_frame,
                                                   "store_by_address.pkl")
        menu2_2.entryconfigure(1, command = menu2_2_pickle)


    entry = tk.Entry(frames_t)
    entry.place(x=510, y=45, width=180)
    canvas4 = tk.Canvas(frames_t, bg=dark, width=180, height=20,
                        highlightthickness=0)
    canvas4.place(x=510, y=25)
    text_entry = tk.Label(frames_t, text="Город/улица", bg=dark,
                          fg=text_color)
    text_entry.place(x=510, y=25)

    button41= Button_1(frames_t, text="Сформировать")
    button41.config(command=create_report)
    button41.place(x=510, y=220)


def report_3(hsb, vsb):
    """
    Аргументы:
        hsb, vsb - объекты tkinter.Scrollbar()

    Данная функция открывает окно отчета goods_by_price
    """
    global menu2_2, frames_t, frame1
    for widget in frames_t.winfo_children():
        if not widget==frame1:
            widget.destroy()

    hsb.pack_forget()
    vsb.pack_forget()
    # Формирование отчета
    gpp = pd.read_pickle('./data/goods_provider_price.pkl')
    gsa = pd.read_pickle('./data/goods_store_amount.pkl')
    pc = pd.read_pickle('./data/provider_contacts.pkl')
    sa = pd.read_pickle('./data/store_address.pkl')
    merged_table = dm.dataframe_merger(gpp, pc, gsa, sa)

    merged_table = dm.create_margin_column(merged_table)


    def create_report():
        """
        Данная функция генерирует таблицу отчета
        """
        global menu2_2

        try:
            price = int(entry.get())
        except ValueError:
            price = str(entry.get())


        report_frame = tr.goods_by_price(merged_table, price)

        columns = report_frame.columns

        height = report_frame.shape[0]
        width = report_frame.shape[1]

        labelframe = tk.LabelFrame(frames_t, text="Товар_по_цене",
                                       bg=dark, fg=text_color, width=450,
                                       height=250)
        labelframe.place(x=10, y=5)
        cr_canvas = tk.Canvas(labelframe,
                              scrollregion=(0, 0, 220 + 220 * width,
                                            20 + 20 * height),
                              highlightthickness = 0, bg = dark)
        hsb['command'] = cr_canvas.xview
        vsb['command'] = cr_canvas.yview
        cr_canvas.pack(side="left",expand=True,fill="both")
        cr_canvas.config(width = 450, height = 250)
        hsb.pack(side="bottom", fill="x")
        vsb.pack(side="right", fill="y")
        cr_canvas.config(xscrollcommand=hsb.set, yscrollcommand=vsb.set)

        pnt = np.empty(shape=(width, height), dtype="O")
        vrs = np.empty(shape=(width, height), dtype="O")
        for i in range(width):
            for j in range(height):
                vrs[i, j] = tk.StringVar()
        for i in range(width):
            a = tk.Label(cr_canvas, text = columns[i], bg=dark,
                         fg=text_color)
            cr_canvas.create_window(0 + 220 * i, 0, height = 20, width = 220,
                                anchor = "nw", window = a)
        for i in range(width):
            for j in range(height):
                pnt[i, j] = tk.Entry(cr_canvas, textvariable = vrs[i, j],
                                     justify='center')
                cr_canvas.create_window(0 + 220 * i, 20 + 20 * j,
                                         window = pnt[i, j], anchor = 'nw',
                                         height = 20, width = 220)
        for i in range(width):
            for j in range(height):
                cnt = report_frame.iloc[j, i]
                vrs[i, j].set(str(cnt))

        menu2_1_saveas = lambda: dm.save_as(report_frame)
        menu2_1.entryconfigure(0, command = menu2_1_saveas)
        menu2_2_excel = lambda: dm.save_to_excel(report_frame,
                                                 "goods_by_price.xlsx",
                                                 False)
        menu2_2.entryconfigure(0, command = menu2_2_excel)

        menu2_2_pickle = lambda: dm.save_to_pickle(report_frame,
                                                   "goods_by_price.pkl")
        menu2_2.entryconfigure(1, command = menu2_2_pickle)

    entry = tk.Entry(frames_t)
    entry.place(x=510, y=45, width=180)
    canvas4 = tk.Canvas(frames_t, bg=dark, width=180, height=20,
                        highlightthickness=0)
    canvas4.place(x=510, y=25)
    text_entry = tk.Label(frames_t, text="Цена", bg=dark, fg=text_color)
    text_entry.place(x=510, y=25)

    button41= Button_1(frames_t, text="Сформировать")
    button41.config(command=create_report)
    button41.place(x=510, y=220)


def pivot_1(hsb, vsb):
    """
    Аргументы:
        hsb, vsb - объекты tkinter.Scrollbar()

    Данная функция открывает окно отчета margin_by_provider
    """
    global menu2_2, frames_t, frame1
    for widget in frames_t.winfo_children():
        if not widget==frame1:
            widget.destroy()

    hsb.pack_forget()
    vsb.pack_forget()
    # Формирование отчета
    gpp = pd.read_pickle('./data/goods_provider_price.pkl')
    gsa = pd.read_pickle('./data/goods_store_amount.pkl')
    pc = pd.read_pickle('./data/provider_contacts.pkl')
    sa = pd.read_pickle('./data/store_address.pkl')
    merged_table = dm.dataframe_merger(gpp, pc, gsa, sa)

    merged_table = dm.create_margin_column(merged_table)


    def create_report():
        """
        Данная функция генерирует таблицу отчета
        """
        global menu2_2

        report_frame = tr.margin_by_provider(merged_table)

        columns = report_frame.columns
        rows = report_frame.index
        height = report_frame.shape[0]
        width = report_frame.shape[1]

        labelframe = tk.LabelFrame(frames_t, text="Наценка_по_поставщикам",
                                       bg=dark, fg=text_color, width=450,
                                       height=250)
        labelframe.place(x=10, y=5)
        cr_canvas = tk.Canvas(labelframe,
                              scrollregion=(0, 0, 220 * (width + 1),
                                            20 * (height + 1)),
                              highlightthickness = 0, bg = dark)
        hsb['command'] = cr_canvas.xview
        vsb['command'] = cr_canvas.yview
        cr_canvas.pack(side="left",expand=True,fill="both")
        cr_canvas.config(width = 450, height = 250)
        hsb.pack(side="bottom", fill="x")
        vsb.pack(side="right", fill="y")
        cr_canvas.config(xscrollcommand=hsb.set, yscrollcommand=vsb.set)

        pnt = np.empty(shape=(width, height), dtype="O")
        vrs = np.empty(shape=(width, height), dtype="O")
        for i in range(width):
            for j in range(height):
                vrs[i, j] = tk.StringVar()
        for i in range(width):
            a = tk.Label(cr_canvas, text = columns[i], bg=dark,
                         fg=text_color)
            cr_canvas.create_window(220 + 220 * i, 0, height = 20, width = 220,
                                anchor = "nw", window = a)
        for i in range(height):
            a = tk.Label(cr_canvas, text = rows[i], bg=dark,
                         fg=text_color)
            cr_canvas.create_window(0, 20 + 20 * i, height = 20, width = 220,
                                anchor = "nw", window = a)
        for i in range(width):
            for j in range(height):
                pnt[i, j] = tk.Entry(cr_canvas, textvariable = vrs[i, j],
                                     justify='center')
                cr_canvas.create_window(220 + 220 * i, 20 + 20 * j,
                                         window = pnt[i, j], anchor = 'nw',
                                         height = 20, width = 220)
        for i in range(width):
            for j in range(height):
                cnt = report_frame.iloc[j, i]
                vrs[i, j].set(str(cnt)[0:5])

        menu2_1_saveas = lambda: dm.save_as(report_frame)
        menu2_1.entryconfigure(0, command = menu2_1_saveas)
        menu2_2_excel = lambda: dm.save_to_excel(report_frame,
                                                 "margin_by_provider.xlsx",
                                                 False)
        menu2_2.entryconfigure(0, command = menu2_2_excel)

        menu2_2_pickle = lambda: dm.save_to_pickle(report_frame,
                                                   "margin_by_provider.pkl")
        menu2_2.entryconfigure(1, command = menu2_2_pickle)


    button41= Button_1(frames_t, text="Сформировать")
    button41.config(command=create_report)
    button41.place(x=510, y=220)

def pivot_2(hsb, vsb):
    """
    Аргументы:
        hsb, vsb - объекты tkinter.Scrollbar()

    Данная функция открывает окно отчета margin_by_store
    """
    global menu2_2, frames_t, frame1
    for widget in frames_t.winfo_children():
        if not widget==frame1:
            widget.destroy()

    hsb.pack_forget()
    vsb.pack_forget()
    # Формирование отчета
    gpp = pd.read_pickle('./data/goods_provider_price.pkl')
    gsa = pd.read_pickle('./data/goods_store_amount.pkl')
    pc = pd.read_pickle('./data/provider_contacts.pkl')
    sa = pd.read_pickle('./data/store_address.pkl')
    merged_table = dm.dataframe_merger(gpp, pc, gsa, sa)

    merged_table = dm.create_margin_column(merged_table)


    def create_report():
        """
        Данная функция генерирует таблицу отчета
        """
        global menu2_2

        report_frame = tr.margin_by_store(merged_table)

        columns = report_frame.columns
        rows = report_frame.index
        height = report_frame.shape[0]
        width = report_frame.shape[1]

        labelframe = tk.LabelFrame(frames_t, text="Наценка_по_магазинам",
                                       bg=dark, fg=text_color, width=450,
                                       height=250)
        labelframe.place(x=10, y=5)
        cr_canvas = tk.Canvas(labelframe,
                              scrollregion=(0, 0, 100 + 220 * width,
                                            20 + 20 * height),
                              highlightthickness = 0, bg = dark)
        hsb['command'] = cr_canvas.xview
        vsb['command'] = cr_canvas.yview
        cr_canvas.pack(side="left",expand=True,fill="both")
        cr_canvas.config(width = 450, height = 250)
        hsb.pack(side="bottom", fill="x")
        vsb.pack(side="right", fill="y")
        cr_canvas.config(xscrollcommand=hsb.set, yscrollcommand=vsb.set)

        pnt = np.empty(shape=(width, height), dtype="O")
        vrs = np.empty(shape=(width, height), dtype="O")
        for i in range(width):
            for j in range(height):
                vrs[i, j] = tk.StringVar()
        for i in range(width):
            a = tk.Label(cr_canvas, text = columns[i], bg=dark,
                         fg=text_color)
            cr_canvas.create_window(100 + 220 * i, 0, height = 20, width = 220,
                                anchor = "nw", window = a)
        for i in range(height):
            a = tk.Label(cr_canvas, text = "ID магазина: " + str(rows[i][0]),
                         bg=dark, fg=text_color)
            cr_canvas.create_window(0, 20 + 20 * i, height = 20, width = 100,
                                anchor = "nw", window = a)
        for i in range(width):
            for j in range(height):
                pnt[i, j] = tk.Entry(cr_canvas, textvariable = vrs[i, j],
                                     justify='center')
                cr_canvas.create_window(100 + 220 * i, 20 + 20 * j,
                                         window = pnt[i, j], anchor = 'nw',
                                         height = 20, width = 220)
        for i in range(width):
            for j in range(height):
                cnt = report_frame.iloc[j, i]
                vrs[i, j].set(str(cnt)[0:5])

        menu2_1_saveas = lambda: dm.save_as(report_frame)
        menu2_1.entryconfigure(0, command = menu2_1_saveas)
        menu2_2_excel = lambda: dm.save_to_excel(report_frame,
                                                 "margin_by_store.xlsx",
                                                 False)
        menu2_2.entryconfigure(0, command = menu2_2_excel)

        menu2_2_pickle = lambda: dm.save_to_pickle(report_frame,
                                                   "margin_by_store.pkl")
        menu2_2.entryconfigure(1, command = menu2_2_pickle)

    button41= Button_1(frames_t, text="Сформировать")
    button41.config(command=create_report)
    button41.place(x=510, y=220)


def pivot_3(hsb, vsb):
    """
    Аргументы:
        hsb, vsb - объекты tkinter.Scrollbar()

    Данная функция открывает окно отчета pivot_table_first_version
    """
    global menu2_2, frames_t, frame1
    for widget in frames_t.winfo_children():
        if not widget==frame1:
            widget.destroy()

    hsb.pack_forget()
    vsb.pack_forget()
    # Формирование отчета
    gpp = pd.read_pickle('./data/goods_provider_price.pkl')
    gsa = pd.read_pickle('./data/goods_store_amount.pkl')
    pc = pd.read_pickle('./data/provider_contacts.pkl')
    sa = pd.read_pickle('./data/store_address.pkl')
    merged_table = dm.dataframe_merger(gpp, pc, gsa, sa)

    merged_table = dm.create_margin_column(merged_table)


    def create_report():
        """
        Данная функция генерирует таблицу отчета
        """
        global menu2_2

        report_frame = tr.pivot_table_first_version(merged_table)

        columns = report_frame.columns
        rows = report_frame.index
        height = report_frame.shape[0]
        width = report_frame.shape[1]

        labelframe = tk.LabelFrame(frames_t, text="Наценка_по_магазинам",
                                       bg=dark, fg=text_color, width=450,
                                       height=250)
        labelframe.place(x=10, y=5)
        cr_canvas = tk.Canvas(labelframe,
                              scrollregion=(0, 0, 220 + 220 * width,
                                            20 + 20 * height),
                              highlightthickness = 0, bg = dark)
        hsb['command'] = cr_canvas.xview
        vsb['command'] = cr_canvas.yview
        cr_canvas.pack(side="left",expand=True,fill="both")
        cr_canvas.config(width = 450, height = 250)
        hsb.pack(side="bottom", fill="x")
        vsb.pack(side="right", fill="y")
        cr_canvas.config(xscrollcommand=hsb.set, yscrollcommand=vsb.set)

        pnt = np.empty(shape=(width, height), dtype="O")
        vrs = np.empty(shape=(width, height), dtype="O")
        for i in range(width):
            for j in range(height):
                vrs[i, j] = tk.StringVar()
        for i in range(width):
            a = tk.Label(cr_canvas, text = columns[i], bg=dark,
                         fg=text_color)
            cr_canvas.create_window(220 + 220 * i, 0, height = 20, width = 220,
                                anchor = "nw", window = a)
        for i in range(height):
            a = tk.Label(cr_canvas, text = rows[i], bg=dark, fg=text_color)
            cr_canvas.create_window(0, 20 + 20 * i, height = 20, width = 220,
                                anchor = "nw", window = a)
        for i in range(width):
            for j in range(height):
                pnt[i, j] = tk.Entry(cr_canvas, textvariable = vrs[i, j],
                                     justify='center')
                cr_canvas.create_window(220 + 220 * i, 20 + 20 * j,
                                         window = pnt[i, j], anchor = 'nw',
                                         height = 20, width = 220)
        for i in range(width):
            for j in range(height):
                cnt = report_frame.iloc[j, i]
                vrs[i, j].set(str(cnt)[0:5])

        menu2_1_saveas = lambda: dm.save_as(report_frame)
        menu2_1.entryconfigure(0, command = menu2_1_saveas)
        menu2_2_excel = lambda: dm.save_to_excel(report_frame,
                                                 "pivot_of_margin_between_store_and_provider.xlsx",
                                                 False)
        menu2_2.entryconfigure(0, command = menu2_2_excel)

        menu2_2_pickle = lambda: dm.save_to_pickle(report_frame,
                                                   "pivot_of_margin_between_store_and_provider.pkl")
        menu2_2.entryconfigure(1, command = menu2_2_pickle)


    button41= Button_1(frames_t, text="Сформировать")
    button41.config(command=create_report)
    button41.place(x=510, y=220)


# Функции для графических отчетов

def f3(help_graph):
    """
    Данная функция создает окно справки для графических отчетов
    """
    root1=tk.Tk()
    root1.geometry('1400x300+100+80')
    root1.title("Справка")
    reference_text = tk.Label(root1, text=help_graph,
                              font=('Colibry', 12, 'bold'),
                              fg=rgb_hack((42,54,59)))
    reference_text.grid(column=0, row=1)
    root1.mainloop()

def tab_report_graph(master): # Формирование вкладки Отчет
    """
    Аргументы:
        master - виджет
        hsb, vsb - объекты tkinter.Scrollbar()

    Функция, создающая вкладку "Отчет" в меню окна графических отчетов
    """
    menu4 = tk.Menu(root, tearoff=0)
    menu4.add_command(label="Графический отчет 1", command=graph_report_1)
    menu4.add_command(label="Графический отчет 2", command=graph_report_2)
    menu4.add_command(label="Графический отчет 3", command=graph_report_3)
    menu4.add_command(label="Графический отчет 4", command=graph_report_4)
    menu4.add_command(label="Графический отчет 5", command=graph_report_5)
    master.add_cascade(label="Отчет", menu=menu4)

def graph_report_1():
    """
    Данная функция создает окно графического отчета amount_after_restock
    """
    global frames_g, frame_g
    for widget in frames_g.winfo_children():
        if not widget==frame_g:
            widget.destroy()

    gpp = pd.read_pickle('./data/goods_provider_price.pkl')
    gsa = pd.read_pickle('./data/goods_store_amount.pkl')
    pc = pd.read_pickle('./data/provider_contacts.pkl')
    sa = pd.read_pickle('./data/store_address.pkl')
    merged_table = dm.dataframe_merger(gpp, pc, gsa, sa)

    merged_table = dm.create_margin_column(merged_table)


    def create_graph():
        """
        Данная функция генерирует сам график в интерфейсе
        """
        for widget in frames_g.winfo_children():
            if (isinstance(widget, FigureCanvasTkAgg) or
                isinstance(widget, NavigationToolbar2Tk)):
                widget.destroy()

        fig = mpl.figure.Figure(figsize = (6.5, 4.5), dpi = 65)
        gm.amount_after_restock(merged_table, sa, fig)
        canvas = FigureCanvasTkAgg(fig, master = frames_g)
        canvas.draw()
        canvas.get_tk_widget().place(x = 30, y = 5)
        NavigationToolbar2Tk.toolitems = (('Home', 'Reset original view', 'home', 'home'),
                                          ('Back', 'Back to  previous view', 'back', 'back'),
                                          ('Forward', 'Forward to next view', 'forward', 'forward'),
                                          (None, None, None, None),
                                          ('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),
                                          ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
                                          (None, None, None, None),
                                          ('Save', 'Save the figure', 'filesave', 'save_figure'))
        toolbar = NavigationToolbar2Tk(canvas, frames_g)
        toolbar.update()
        canvas.get_tk_widget().place(x = 30, y = 5)

    button42 = Button_1(frame_g, text="Сформировать")
    button42.config(command = lambda: create_graph())
    button42.place(x=510, y=220)


def graph_report_2():
    """
    Данная функция создает окно графического отчета restock_stats
    """
    global frames_g, frame_g
    for widget in frames_g.winfo_children():
        if not widget==frame_g:
            widget.destroy()

    gpp = pd.read_pickle('./data/goods_provider_price.pkl')
    gsa = pd.read_pickle('./data/goods_store_amount.pkl')
    pc = pd.read_pickle('./data/provider_contacts.pkl')
    sa = pd.read_pickle('./data/store_address.pkl')
    merged_table = dm.dataframe_merger(gpp, pc, gsa, sa)

    merged_table = dm.create_margin_column(merged_table)

    entry = tk.Entry(frames_g)
    entry.place(x=510, y=45, width=180)
    canvas4 = tk.Canvas(frames_g, bg=dark, width=180, height=20,
                        highlightthickness=0)
    canvas4.place(x=510, y=25)
    text_entry = tk.Label(frames_g, text="ID товара", bg=dark,
                          fg=text_color)
    text_entry.place(x=510, y=25)


    def create_graph(entry):
        """
        Данная функция генерирует сам график в интерфейсе
        """
        for widget in frames_g.winfo_children():
            if (isinstance(widget, FigureCanvasTkAgg) or
                isinstance(widget, NavigationToolbar2Tk)):
                widget.destroy()

        try:
            goods_id = int(entry.get())
        except:
            goods_id = str(entry.get())
        fig = mpl.figure.Figure(figsize = (6.5, 4.5), dpi = 65)
        gm.restock_stats(merged_table, sa, goods_id, fig)
        canvas = FigureCanvasTkAgg(fig, master = frames_g)
        canvas.draw()
        canvas.get_tk_widget().place(x = 30, y = 5)
        NavigationToolbar2Tk.toolitems = (('Home', 'Reset original view', 'home', 'home'),
                                          ('Back', 'Back to  previous view', 'back', 'back'),
                                          ('Forward', 'Forward to next view', 'forward', 'forward'),
                                          (None, None, None, None),
                                          ('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),
                                          ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
                                          (None, None, None, None),
                                          ('Save', 'Save the figure', 'filesave', 'save_figure'))
        toolbar = NavigationToolbar2Tk(canvas, frames_g)
        toolbar.update()
        canvas.get_tk_widget().place(x = 30, y = 5)


    button42 = Button_1(frame_g, text="Сформировать")
    button42.config(command = lambda: create_graph(entry))
    button42.place(x=510, y=220)


def graph_report_3():
    """
    Данная функция создает окно графического отчета stock_by_goods
    """
    global frames_g, frame_g
    for widget in frames_g.winfo_children():
        if not widget==frame_g:
            widget.destroy()

    gpp = pd.read_pickle('./data/goods_provider_price.pkl')
    gsa = pd.read_pickle('./data/goods_store_amount.pkl')
    pc = pd.read_pickle('./data/provider_contacts.pkl')
    sa = pd.read_pickle('./data/store_address.pkl')
    merged_table = dm.dataframe_merger(gpp, pc, gsa, sa)

    merged_table = dm.create_margin_column(merged_table)
    def create_graph():
        """
        Данная функция генерирует сам график в интерфейсе
        """
        for widget in frames_g.winfo_children():
            if (isinstance(widget, FigureCanvasTkAgg) or
                isinstance(widget, NavigationToolbar2Tk)):
                widget.destroy()

        fig = mpl.figure.Figure(figsize = (6.5, 4.5), dpi = 65)
        gm.stock_by_goods(merged_table, fig)
        canvas = FigureCanvasTkAgg(fig, master = frames_g)
        canvas.draw()
        canvas.get_tk_widget().place(x = 30, y = 5)
        NavigationToolbar2Tk.toolitems = (('Home', 'Reset original view', 'home', 'home'),
                                          ('Back', 'Back to  previous view', 'back', 'back'),
                                          ('Forward', 'Forward to next view', 'forward', 'forward'),
                                          (None, None, None, None),
                                          ('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),
                                          ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
                                          (None, None, None, None),
                                          ('Save', 'Save the figure', 'filesave', 'save_figure'))
        toolbar = NavigationToolbar2Tk(canvas, frames_g)
        toolbar.update()
        canvas.get_tk_widget().place(x = 30, y = 5)

    button42 = Button_1(frame_g, text="Сформировать")
    button42.config(command = lambda: create_graph())
    button42.place(x=510, y=220)


def graph_report_4():
    """
    Данная функция создает окно графического отчета scatter_ratio
    """
    global frames_g, frame_g
    for widget in frames_g.winfo_children():
        if not widget==frame_g:
            widget.destroy()

    gpp = pd.read_pickle('./data/goods_provider_price.pkl')
    gsa = pd.read_pickle('./data/goods_store_amount.pkl')
    pc = pd.read_pickle('./data/provider_contacts.pkl')
    sa = pd.read_pickle('./data/store_address.pkl')
    merged_table = dm.dataframe_merger(gpp, pc, gsa, sa)

    merged_table = dm.create_margin_column(merged_table)
    def create_graph():
        """
        Данная функция генерирует сам график в интерфейсе
        """
        for widget in frames_g.winfo_children():
            if (isinstance(widget, FigureCanvasTkAgg) or
                isinstance(widget, NavigationToolbar2Tk)):
                widget.destroy()

        fig = mpl.figure.Figure(figsize = (6.5, 4.5), dpi = 65)
        gm.scatter_ratio(merged_table, fig)
        canvas = FigureCanvasTkAgg(fig, master = frames_g)
        canvas.draw()
        canvas.get_tk_widget().place(x = 30, y = 5)
        NavigationToolbar2Tk.toolitems = (('Home', 'Reset original view', 'home', 'home'),
                                          ('Back', 'Back to  previous view', 'back', 'back'),
                                          ('Forward', 'Forward to next view', 'forward', 'forward'),
                                          (None, None, None, None),
                                          ('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),
                                          ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
                                          (None, None, None, None),
                                          ('Save', 'Save the figure', 'filesave', 'save_figure'))
        toolbar = NavigationToolbar2Tk(canvas, frames_g)
        toolbar.update()
        canvas.get_tk_widget().place(x = 30, y = 5)

    button42 = Button_1(frame_g, text="Сформировать")
    button42.config(command = lambda: create_graph())
    button42.place(x=510, y=220)


def graph_report_5():
    """
    Данная функция создает окно графического box_whisker
    """
    global frames_g, frame_g
    for widget in frames_g.winfo_children():
        if not widget==frame_g:
            widget.destroy()

    gpp = pd.read_pickle('./data/goods_provider_price.pkl')
    gsa = pd.read_pickle('./data/goods_store_amount.pkl')
    pc = pd.read_pickle('./data/provider_contacts.pkl')
    sa = pd.read_pickle('./data/store_address.pkl')
    merged_table = dm.dataframe_merger(gpp, pc, gsa, sa)

    merged_table = dm.create_margin_column(merged_table)
    def create_graph():
        """
        Данная функция генерирует сам график в интерфейсе
        """
        for widget in frames_g.winfo_children():
            if (isinstance(widget, FigureCanvasTkAgg) or
                isinstance(widget, NavigationToolbar2Tk)):
                widget.destroy()

        fig = mpl.figure.Figure(figsize = (6.5, 4.5), dpi = 65)
        gm.box_whisker(merged_table, fig)
        canvas = FigureCanvasTkAgg(fig, master = frames_g)
        canvas.draw()
        canvas.get_tk_widget().place(x = 30, y = 5)
        NavigationToolbar2Tk.toolitems = (('Home', 'Reset original view', 'home', 'home'),
                                          ('Back', 'Back to  previous view', 'back', 'back'),
                                          ('Forward', 'Forward to next view', 'forward', 'forward'),
                                          (None, None, None, None),
                                          ('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),
                                          ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
                                          (None, None, None, None),
                                          ('Save', 'Save the figure', 'filesave', 'save_figure'))
        toolbar = NavigationToolbar2Tk(canvas, frames_g)
        toolbar.update()
        canvas.get_tk_widget().place(x = 30, y = 5)

    button42 = Button_1(frame_g, text="Сформировать")
    button42.config(command = lambda: create_graph())
    button42.place(x=510, y=220)
# Для вызова окна со справочниками

def spravochniki():
    """
    Данная функция создает заготовку для окон справочников
    """
    global root, frames_all, frames_s, frame, white, light, dark, help_spr
    global mainmenu1, menu1_1, menu1_2, menu1_3
    global mainmenu2, menu2_1, menu2_2, menu2_3
    global mainmenu3, menu3_1, menu3_2, menu3_3

    for widget in frames_all.winfo_children():
        widget.destroy()
    mainmenu2.destroy()
    mainmenu3.destroy()

    mainmenu1 = tk.Menu(root, tearoff=0)
    menu1_1 = tk.Menu(mainmenu1, tearoff=0)
    menu1_2 = tk.Menu(mainmenu1, tearoff=0)
    menu1_3 = tk.Menu(mainmenu1, tearoff=0)

    menu1_3.add_command(label="Светлая тема", command=light_theme)
    menu1_3.add_command(label="Темная тема", command=dark_theme)
    menu1_3.add_command(label="Настройки интерфейса...", command=ini_change)

    menu1_2.add_command(label="В Excel")
    menu1_2.add_command(label="В бинарный формат")

    menu1_1.add_command(label="Сохранить")
    menu1_1.add_command(label="Сохранить как...")
    menu1_1.add_cascade(label="Экспортировать...", menu = menu1_2)

    mainmenu1.add_cascade(label="Файл", menu = menu1_1)
    mainmenu1.add_cascade(label="Вид", menu = menu1_3)
    mainmenu1.add_command(label="Справка", command = lambda:f1(help_spr))

    frames_all.config(bg=light)
    frames_s = tk.Frame(frames_all, bd = 1, bg=light)
    frames_s.pack(fill="both", expand=1, padx=5, pady=5)

    frame = tk.Frame(frames_s, bd = 1, bg=light)
    frame.pack(fill="both", expand=1, padx=5, pady=5)

    hsb = tk.Scrollbar(frame, orient="horizontal")
    vsb = tk.Scrollbar(frame, orient="vertical")

    button1= Button_1(frame, text="Справочник 1")
    button1.config(command=lambda: spr1(hsb, vsb))
    button1.place(x=510, y=25)

    button2= Button_1(frame, text="Справочник 2")
    button2.config(command=lambda: spr2(hsb, vsb))
    button2.place(x=510, y=85)

    button3= Button_1(frame, text="Справочник 3")
    button3.config(command=lambda: spr3(hsb, vsb))
    button3.place(x=510, y=145)

    button4= Button_1(frame, text="Справочник 4")
    button4.config(command=lambda: spr4(hsb, vsb))
    button4.place(x=510, y=205)

    button5= Button_2(frame, text="Текстовый отчет")
    button5.config(command=text_report)
    button5.place(x=20, y=310)

    button6= Button_2(frame, text="Графический отчет")
    button6.config(command=graphical_report)
    button6.place(x=250, y=310)

    button7= Button_3(frame, text="Закрыть", color=text_color)
    button7.config(bg=dark, command=root.destroy)
    button7.place(x=510, y=310)

    root.config(menu=mainmenu1, bg=light)
    root.mainloop()

# Для вызова окна с текстовыми отчетами

def text_report():
    """
    Данная функция создает заготовку для окон текстовых отчетов
    """
    global root, frames_all, frames_t, frame1, frame, white, light, help_text
    global mainmenu1, menu1_1, menu1_2, menu1_3
    global mainmenu2, menu2_1, menu2_2, menu2_3
    global mainmenu3, menu3_1, menu3_2, menu3_3

    for widget in frames_all.winfo_children():
        widget.destroy()
    mainmenu1.destroy()
    mainmenu3.destroy()

    mainmenu2 = tk.Menu(root, tearoff=0)
    menu2_1 = tk.Menu(mainmenu2, tearoff=0)
    menu2_2 = tk.Menu(mainmenu2, tearoff=0)
    menu2_3 = tk.Menu(mainmenu2, tearoff=0)

    menu2_3.add_command(label="Светлая тема", command=light_theme)
    menu2_3.add_command(label="Темная тема", command=dark_theme)
    menu2_3.add_command(label="Настройки интерфейса...", command=ini_change)

    menu2_2.add_command(label="В Excel")
    menu2_2.add_command(label="В бинарный формат")

    menu2_1.add_cascade(label="Сохранить как...")
    menu2_1.add_cascade(label="Экспортировать...", menu = menu2_2)

    mainmenu2.add_cascade(label="Файл", menu = menu2_1)

    frames_all.config(bg=light)
    frames_t = tk.Frame(frames_all, bd = 1, bg=light)
    frames_t.pack(fill="both", expand=1, padx=5, pady=5)

    frame1 = tk.Frame(frames_t, bd = 1, bg=light)
    frame1.pack(fill="both", expand=1, padx=5, pady=5)

    hsb = tk.Scrollbar(frame1, orient="horizontal")
    vsb = tk.Scrollbar(frame1, orient="vertical")
    tab_report(mainmenu2, hsb, vsb)
    mainmenu2.add_cascade(label="Вид", menu = menu2_3)
    mainmenu2.add_command(label="Справка", command = lambda: f2(help_text))

    button51= Button_2(frame1, text="Справочники")
    button51.config(command=spravochniki)
    button51.place(x=20, y=310)

    button61= Button_2(frame1, text="Графический отчет")
    button61.config(command=graphical_report)
    button61.place(x=250, y=310)

    button71= Button_3(frame1, text="Закрыть", color=text_color)
    button71.config(bg=dark, command=root.destroy)
    button71.place(x=510, y=310)

    report_1(hsb, vsb)

    root.config(menu=mainmenu2, bg=light)
    root.mainloop()


# Для вызова графических отчетов

def graphical_report():
    """
    Данная функция создает заготовку для окон графических отчетов
    """
    global root, frames_all, frames_g, frame_g, frame, white, light, help_graph
    global mainmenu1, menu1_1, menu1_2, menu1_3
    global mainmenu2, menu2_1, menu2_2, menu2_3
    global mainmenu3, menu3_1, menu3_2, menu3_3

    for widget in frames_all.winfo_children():
        widget.destroy()
    mainmenu1.destroy()
    mainmenu2.destroy()

    mainmenu3 = tk.Menu(root, tearoff=0)
    menu3_3 = tk.Menu(mainmenu3, tearoff=0)
    menu3_3.add_command(label="Светлая тема", command=light_theme)
    menu3_3.add_command(label="Темная тема", command=dark_theme)
    menu3_3.add_command(label="Настройки интерфейса...", command=ini_change)

    menu3_2 = tk.Menu(mainmenu3, tearoff=0) # Создаем объект класса Menu
    menu3_2.add_command(label="В Excel")
    menu3_2.add_command(label="В бинарный формат")

    # Формирование вкладки Файл
    menu3_1 = tk.Menu(mainmenu3, tearoff=0)
    menu3_1.add_cascade(label="Экспортировать...", menu = menu3_2)

    # Размещение пунктов в меню
    tab_report_graph(mainmenu3)
    mainmenu3.add_cascade(label="Вид", menu = menu3_3)
    mainmenu3.add_command(label="Справка", command = lambda: f3(help_graph))

    frames_all.config(bg=light)
    frames_g = tk.Frame(frames_all, bd = 1, bg=light)
    frames_g.pack(fill="both", expand=1, padx=5, pady=5)

    frame_g = tk.Frame(frames_g, bd = 1, bg=light)
    frame_g.pack(fill="both", expand=1, padx=5, pady=5)

    button52= Button_2(frame_g, text="Справочники")
    button52.config(command=spravochniki)
    button52.place(x=20, y=310)

    button62= Button_2(frame_g, text="Текстовый отчет")
    button62.config(command=text_report)
    button62.place(x=250, y=310)

    button72= Button_3(frame_g, text="Закрыть", color=text_color)
    button72.config(bg=dark, command=root.destroy)
    button72.place(x=510, y=310)

    graph_report_1()

    root.config(menu=mainmenu3, bg=light)
    root.mainloop()


def ini_change():
    global ini_text
    ini_root = tk.Tk()
    ini_root.title("Редактирование файла config.ini")
    ini_root.geometry('800x450+100+100')
    field = tk.Text(ini_root)
    field.insert("1.0", ini_text)
    field.pack(fill = 'both')
    
    
    def save_ini():
        text = field.get("1.0", "end")
        try:
            with open("./scripts/config.ini", "w", encoding = "utf-8") as f:
                f.write(text)
                button.config(text = 'Сохранено')
        except FileNotFoundError:
            button.config(text = 'Ошибка')

    button = Button_1(ini_root, "Сохранить")
    button.config(command = save_ini)
    button.pack(side = 'bottom')
    label = tk.Label(ini_root, text = "Изменения применятся после" +
                     " перезапуска приложения")
    label.pack(side = 'bottom')


# Парсинг .ini файла
try:
    with open("./scripts/config.ini", "r", encoding = "utf-8") as f:
        a = f.readlines()
        f.seek(0)
        ini_text = f.read()

    for i in range(len(a)):
        a[i] = a[i].rstrip('\n')

    font = a[0].split()

    buffer = a[1].split()
    l = (int(buffer[1]), int(buffer[2]), int(buffer[3]))
    buffer = a[2].split()
    d = (int(buffer[1]), int(buffer[2]), int(buffer[3]))
    buffer = a[3].split()
    w = (int(buffer[1]), int(buffer[2]), int(buffer[3]))
    buffer = a[4].split()
    t = (int(buffer[1]), int(buffer[2]), int(buffer[3]))

    bool_weight = {"да":"bold", "нет":"normal"}
    bool_slant = {"да":"italic", "нет":"roman"}
    bool_bool = {"да":1, "нет":0}

    font_family = font[1]
    font_size = int(font[2].split('=')[1])
    font_weight = bool_weight[font[3].split('=')[1]]
    font_slant = bool_slant[font[4].split('=')[1]]
    font_underline = bool_bool[font[5].split('=')[1]]
    font_overstrike = bool_bool[font[6].split('=')[1]]

except (IndexError, FileNotFoundError) as error:
    # Вывод сообщения об ошибке в config.ini и завершение работы
    if str(error) == "list index out of range":
        print("\nФайл config.ini заполнен не по образцу!")
    else:
        print("\nФайл config.ini не найден! Необходимо его создать в " +
              "директории ./work/scripts строго по образцу!")
    a = ["\nОбразец:\n\n",
         "Шрифт: TkDefaultFont шрифт=10 полужирное=да курсив=нет" +
         " подчеркивание=да перечеркивание=нет\n",
         "Цвет_светлый: 170 207 208\n",
         "Цвет_темный: 121 168 169\n",
         "Цвет_белый: 244 247 247\n",
         "Цвет_текста: 0 0 0\n"]
    print(*a, sep = '')
    print("Приложение не запущено! Работа скрипта завершена!\n")
    sys.exit()


root = tk.Tk() # Запуск интерпретатора tcl/tk и создание базового окна
root.geometry('820x450+100+80')
root.minsize(820,450)
root.maxsize(820,450)
root.title("База данных")
default_font = tk.font.nametofont("TkDefaultFont")
default_font.configure(family = font_family, size = font_size,
                       weight=font_weight,
                       slant=font_slant,
                       underline=font_underline,
                       overstrike=font_overstrike)

# Инициализация глобальных переменных
light = rgb_hack(l)
dark = rgb_hack(d)
white = rgb_hack(w)
text_color = rgb_hack(t)

frames_all = tk.Frame(root, bd = 1, bg=rgb_hack((255,255,255)))
frames_all.pack(fill="both", expand=1, padx=5, pady=5)

mainmenu1 = tk.Menu(root, tearoff=0)
menu1_1 = tk.Menu(mainmenu1, tearoff=0)
menu1_2 = tk.Menu(mainmenu1, tearoff=0)
menu1_3 = tk.Menu(mainmenu1, tearoff=0)

menu1_3.add_command(label="Светлая тема", command=light_theme)
menu1_3.add_command(label="Темная тема", command=dark_theme)
menu1_3.add_command(label="Настройки интерфейса...", command=ini_change)

menu1_2.add_command(label="В Excel")
menu1_2.add_command(label="В бинарный формат")

menu1_1.add_command(label="Сохранить")
menu1_1.add_command(label="Сохранить как...")
menu1_1.add_cascade(label="Экспортировать...", menu = menu1_2)

mainmenu1.add_cascade(label="Файл", menu = menu1_1)
mainmenu1.add_cascade(label="Вид", menu = menu1_3)
mainmenu1.add_command(label="Справка", command = lambda:f1(help_spr))

frames_all.config(bg=light)
frames_s = tk.Frame(frames_all, bd = 1, bg=light)
frames_s.pack(fill="both", expand=1, padx=5, pady=5)

frame = tk.Frame(frames_s, bd = 1, bg=light)
frame.pack(fill="both", expand=1, padx=5, pady=5)


mainmenu2 = tk.Menu(root, tearoff=0)
menu2_1 = tk.Menu(mainmenu2, tearoff=0)
menu2_2 = tk.Menu(mainmenu2, tearoff=0)
menu2_3 = tk.Menu(mainmenu2, tearoff=0)

menu2_3.add_command(label="Светлая тема", command=light_theme)
menu2_3.add_command(label="Темная тема", command=dark_theme)
menu2_3.add_command(label="Настройки интерфейса...", command=ini_change)

menu2_2.add_command(label="В Excel")
menu2_2.add_command(label="В бинарный формат")

menu2_1.add_cascade(label="Сохранить как...")
menu2_1.add_cascade(label="Экспортировать...", menu = menu2_2)

mainmenu2.add_cascade(label="Файл", menu = menu2_1)
mainmenu2.add_cascade(label="Вид", menu = menu2_3)
mainmenu2.add_command(label="Справка", command = lambda: f2(help_text))

frames_all.config(bg=light)
frames_t = tk.Frame(frames_all, bd = 1, bg=light)
frames_t.pack(fill="both", expand=1, padx=5, pady=5)

frame1 = tk.Frame(frames_t, bd = 1, bg=light)
frame1.pack(fill="both", expand=1, padx=5, pady=5)


mainmenu3 = tk.Menu(root, tearoff=0)
menu3_3 = tk.Menu(mainmenu3, tearoff=0)
menu3_3.add_command(label="Светлая тема", command=light_theme)
menu3_3.add_command(label="Темная тема", command=dark_theme)
menu3_3.add_command(label="Настройки интерфейса...", command=ini_change)

# Размещение пунктов в меню
mainmenu3.add_cascade(label="Вид", menu = menu3_3)
mainmenu3.add_command(label="Справка", command = lambda: f3(help_graph))

frames_all.config(bg=light)
frames_g = tk.Frame(frames_all, bd = 1, bg=light)
frames_g.pack(fill="both", expand=1, padx=5, pady=5)

frame_g = tk.Frame(frames_g, bd = 1, bg=light)
frame_g.pack(fill="both", expand=1, padx=5, pady=5)


help_spr = ("Справочник 1 – ID товара, ID магазина, Количество после" +
" последней закупки, Продажи после последней закупки, Дата последней" +
" закупки,\nКоличество последней закупки, Стоимость последней закупки.\n" +
"\nСправочник 2 – ID товара, Наименование, Поставщик, Единица измерения," +
" Цена продажи, Количество за цену.\n" +
"\nСправочник 3 – Поставщик, E-mail, Телефон\n" +
"\nСправочник 4 – ID магазина, Адрес")

help_text = ("Отчет 1 – выдает информацию (Наименование, Адрес, " +
"ID магазина, Количество после последней покупки)\nпо запросу Поставщика " +
"(возможен множественный выбор через клавишу Ctrl). "
"\n\nОтчет 2 – выдает информацию о ID-магазинах и их адресах по запросу " +
"Город/улица. " +
"\n\nОтчет 3 – выдает информацию о товарах, цена продажи которых превышает " +
"запрос Цена." +
"\n\nСводная таблица 1 – отображает средний процент наценки каждого " +
"магазина, а также среднеквадратичное отклонение от этой величины. "
"\n\nСводная таблица 2 – отображает средний процент наценки каждого " +
"поставщика, а также среднеквадратичное отклонение от этой величины. " +
"\n\nСводная таблица 3 – отображает информацию в разрезе Поставщик и "+
"ID-магазина по проценту наценки и выводит среднее арифметическое и " +
"среднеквадратичное отклонение. ")

help_graph = ("Графический отчет 1 – кластеризованная столбчатая диаграмма " +
"по аргументам: ID товара и ID магазина.\nПоказывает Количество в единицу " +
"товара по каждому товару, в каждом магазине. " +
"\n\nГрафический отчет 2 - кластеризованная столбчатая диаграмма по " +
"аргументам: ID магазина, Количество после последней закупки, Продажи "+
"после последней закупки.\nПринимается запрос ID товара, по которому "+
"будет строиться данная диаграмма. "+
"\n\nГрафический отчет 3 – категоризированная гистограмма по аргументам: "+
"ID товара и количество магазинов,\nв которых присутствует данный товар. "+
"\n\nГрафический отчет 4 – категоризированная диаграмма рассеивания по "+
"аргументам:\nКоличество после последней закупки, Продажи после последней "+
"закупки.Отображение идет для всех товаров и магазинов. "+
"\n\nГрафический отчет 5 – категоризированная диаграмма Бокса-Вискера\nпо"+
"аргументам: ID товара и Процент наценки "+
"(данный аргумент высчитывается автоматически). ")
# Начальное окно приложения
spravochniki()
root.mainloop()
