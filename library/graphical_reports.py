# -*- coding: utf-8 -*-
"""
Talibov S. M., Goncharova K. V., brigade 4, BIV221
"""
import numpy as np


def amount_after_restock(frame, stores, figure):
    """
    Аргументы:
        frame - объединенный dataframe
        stores - dataframe образца store_address
        figure - объект типа matplotlib.figure.Figure(), в который помещается
        график

    Данная функция создает кластеризованную столбцовую диаграмму, которая
    показывает количество каждого товара во всех магазинах, внутри интерфейса
    приложения
    """

    frame = frame.sort_values(by=["ID магазина", "ID товара"])
    mx1 = 0
    mx2 = 0
    try:
        mx1 = max(frame["ID товара"].unique())
    except ValueError:
        mx1 = 0
    try:
        mx2 = max(frame["ID магазина"].unique())
    except ValueError:
        mx2 = 0
    goods = [i + 1 for i in range(mx1)]
    store = [i + 1 for i in range(mx2)]

    width = 0
    try:
        width = 0.5 / len(stores)
    except ZeroDivisionError:
        width = 0

    columns = [[0 for i in range(len(goods))] for j in range(len(stores))]

    for i in range(len(frame)):
        columns[frame["ID магазина"].iloc[i] - 1][frame["ID товара"].iloc[i] - 1] = frame["Количество после последней закупки"].iloc[i]

    plot_bar = figure.add_subplot(111)
    for i in range(len(store)):
        x = [j + 1 + i * width for j in range(len(goods))]
        plot_bar.bar(x, columns[i], label = "Магазин с ID " + str(i + 1),
                     width = width)

    x_labels = [i + 1 for i in range(len(goods))]
    x = [j + 1 for j in range(len(goods))]

    plot_bar.set_xlabel("ID товара")
    plot_bar.set_ylabel("Количество в единицах товара")
    plot_bar.set_title("Графический отчет 1")
    plot_bar.set_xticks(x, x_labels)
    if width != 0:
        plot_bar.legend()


def restock_stats(frame, stores, goods_id, figure):
    """
    Аргументы:
        frame - объединенный dataframe
        stores - dataframe образца store_address
        goods_id - целое число
        figure - объект типа matplotlib.figure.Figure(), в который помещается
        график

    Данная функция создает кластеризованную столбцовую диаграмму, которая
    показывает количество последней закупки и продажи после последней закупки
    для продукта с ID, совпадающим с числом goods_id, по каждому магазину
    """
    frame = frame.sort_values(by="ID магазина")
    buffer = stores["ID магазина"].unique()
    x_labels = [i for i in buffer]
    columns_1 = [0] * len(x_labels)
    columns_2 = [0] * len(x_labels)

    if isinstance(goods_id, int):
        for i in range(len(frame)):
            if frame["ID товара"].iloc[i] == goods_id:
                a = -1
                for j in range(len(x_labels)):
                    if frame["ID магазина"].iloc[i] == x_labels[j]:
                        a = j
                        break
                columns_1[a] = frame["Количество последней закупки"].iloc[i]
                columns_2[a] = frame["Продажи после последней закупки"].iloc[i]

    w = 0.3
    buffer = np.arange(len(x_labels))
    x_1 = [i - (w / 2) for i in buffer]
    x_2 = [i + (w / 2) for i in buffer]
    x_3 = [i for i in buffer]

    plot_bar = figure.add_subplot(111)
    plot_bar.bar(x_1, columns_1, width = w, label = "Количество последней закупки")
    plot_bar.bar(x_2, columns_2, width = w,
            label = "Продажи после последней закупки")
    plot_bar.set_xlabel("ID магазина")
    plot_bar.set_ylabel("Количество в единицах товара")
    plot_bar.set_title("Графический отчет 2")
    plot_bar.set_xticks(x_3, x_labels)
    plot_bar.legend()


def stock_by_goods(frame, figure):
    """
    Аргументы:
        frame - объединенный dataframe
        figure - объект типа matplotlib.figure.Figure(), в который помещается
        график

    Данная функция создает гистограмму, показывающую количество магазинов, в
    в котором находится каждый его товар по его ID
    """
    data = [frame["ID товара"].iloc[i] for i in range(len(frame["ID товара"]))]
    mn, mx = 0, 0
    try:
        mn = min(data) - 1
        mx = max(data) + 1
    except ValueError:
        mn, mx = 0, 0

    plot_hist = figure.add_subplot(111)
    plot_hist.hist(data, 30, range = (mn, mx))
    plot_hist.set_xlabel("ID товара")
    plot_hist.set_ylabel("В скольких магазинах встречается")
    plot_hist.set_title("Графический отчет 3")


def scatter_ratio(frame, figure):
    """
    Аргументы:
        frame - объединенный dataframe
        figure - объект типа matplotlib.figure.Figure(), в который помещается
        график

    Данная функция создает график рассеяния, по оси X которого указано
    количество после последней закупки, а по оси Y указаны продажи после
    последней закупки. Каждая точка указывает на конкретный товар в конкретном
    магазине
    """
    plot_scat = figure.add_subplot(111)
    for i in range(len(frame)):
        x = frame["Количество после последней закупки"].iloc[i]
        y = frame["Продажи после последней закупки"].iloc[i]
        z = frame["ID товара"].iloc[i]
        w = frame["ID магазина"].iloc[i]
        plot_scat.scatter(x, y, label = "Товар " + str(z) + " в магазине " + str(w))

    plot_scat.set_xlabel("Количество после последней закупки")
    plot_scat.set_ylabel("Продажи после последней закупки")
    plot_scat.set_title("Графический отчет 4")
    if len(frame) != 0:
        plot_scat.legend()


def box_whisker(frame, figure):
    """
    Аргументы:
        frame - объединенный dataframe
        figure - объект типа matplotlib.figure.Figure(), в который помещается
        график

    Данная функция создает график типа "Ящик с усами", который показывает
    информацию о наценке (ось Y) товаров (ось X). Вследствие разных стоимостей
    закупки в разных магазинах, наценка может различаться от магазина к
    магазину
    """
    mn, mx = 0, 0
    try:
        mn = min(frame["ID товара"].unique())
        mx = max(frame["ID товара"].unique()) + 1
    except ValueError:
        mn, mx = 0, 0

    goods = [i for i in range(mn, mx)]
    data = []
    for i in range(len(goods)):
        buffer = []
        for j in range(len(frame)):
            if frame["ID товара"].iloc[j] == goods[i]:
                buffer.append(frame["Процент наценки"].iloc[j])
        data.append(buffer)

    plot_bw = figure.add_subplot(111)
    plot_bw.boxplot(data)
    plot_bw.set_xlabel("ID товара")
    plot_bw.set_ylabel("Процент наценки")
    plot_bw.set_title("Графический отчет 5")
