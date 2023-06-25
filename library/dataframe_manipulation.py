# -*- coding: utf-8 -*-
"""
Talibov S. M., Goncharova K. V., brigade 4, BIV221
"""
import os
import tkinter as tk
import pandas as pd

os.chdir("C:/work")


# Dataframe text report prerender
def dataframe_merger(goods_provider_price, provider_contacts,
                     goods_store_amount, store_address):
    """
    Аргументы:
        goods_provider_price - dataframe
        provider_contacts - dataframe
        goods_store_amount - dataframe
        store_address - dataframe

    Результат:
        output_frame - dataframe, созданный объединением данных аргументов по
        соответствующим столбцам
    """
    merger_1 = pd.merge(goods_provider_price, provider_contacts,
                        on = "Поставщик")
    merger_2 = pd.merge(goods_store_amount, store_address, on="ID магазина")
    output_frame = pd.merge(merger_1, merger_2, on="ID товара")
    return output_frame

def create_margin_column(frame):
    """
    Добавляет новые столбцы в объединенный справочник frame\n
    "Цена последней закупки":
        "Стоимость последней закупки" делить на
        "Количество последней закупки";\n
    "Цена за единицу измерения":
        "Цена продажи" делить на "Количество за цену";\n
    "Процент наценки":
        "Цена за единицу измерения" делить на "Цена последней закупки"
    """
    last_stock_price = [frame["Стоимость последней закупки"].loc[i] /
         frame["Количество последней закупки"].loc[i]
         for i in range(len(frame))]
    frame.insert(0, "Цена последней закупки", last_stock_price)

    price_for_unit = [frame["Цена продажи"].loc[i] /
         frame["Количество за цену"].loc[i]
         for i in range(len(frame))]
    frame.insert(0, "Цена за единицу измерения", price_for_unit)

    margin_percentage = [frame["Цена за единицу измерения"].loc[i] /
         frame["Цена последней закупки"].loc[i] - 1
         for i in range(len(frame))]
    frame.insert(0, "Процент наценки", margin_percentage)

    return frame
# Dataframe text report prerender


# Dataframe entry addition
def add_row_to_gpp(frame, providers, new_row):
    """
    Аргументы:
        new_row - массив
        frame - dataframe, над которым производятся операции
        providers - dataframe, который содержит список поставщиков

    Результат:
        frame - dataframe "goods_provider_price", в который добавлена новая
        запись
    """
    if len(new_row) == 6 and type(new_row[0]) == type(new_row[4]) == type(new_row[5]) == int and type(new_row[1]) == type(new_row[2]) == type(new_row[3]) == str:
        if new_row[0] not in frame["ID товара"].unique():
            if new_row[2] in (providers.at[i, "Поставщик"] for i in range(len(providers["Поставщик"]))):
                frame.loc[len(frame)] = new_row
                return "добавление успешно!"
            return "такого поставщика не существует!"
        return "товар с таким ID уже есть в таблице!"
    return "неправильный формат входных данных!"


def add_row_to_pc(frame, new_row):
    """
    Аргументы:
        new_row - массив
        frame - dataframe, над которым производятся операции

    Результат:
        frame - dataframe "provider_contacts", в который добавлена новая
        запись
    """
    if len(new_row) == 3 and type(new_row[0]) == type(new_row[1]) == type(new_row[2]) == str:
        frame.loc[len(frame)] = new_row
        return "добавлено успешно!"
    return "неправильный формат входных данных!"


def add_row_to_sa(frame, new_row):
    """
    Аргументы:
        new_row - массив
        frame - dataframe, над которым производятся операции

    Результат:
        frame - dataframe "store_address", в который добавлена новая
        запись
    """
    if len(new_row) == 2 and type(new_row[0]) == int and type(new_row[1]) == str:
        if new_row[0] not in frame["ID магазина"].unique():
            frame.loc[len(frame)] = new_row
            return "добавлено успешно!"
        return "магазин с таким ID уже существует!"
    return "неправильный формат входных данных!"


def add_row_to_gsa(frame, stores, goods, new_row):
    """
    Аргументы:
        new_row - массив
        frame - dataframe, над которым производятся операции
        stores - dataframe, в котором хранится информация о магазинах
        goods - dataframe, в котором находится информация о продуктах

    Результат:
        frame - dataframe "store_address", в который добавлена новая
        запись
    """
    if len(new_row) == 7 and type(new_row[0]) == type(new_row[1]) == type(new_row[2]) == type(new_row[3]) == type(new_row[5]) == type(new_row[6]) == int and type(new_row[4]) == str:
        i = 0
        while i < len(frame) and (new_row[0] != frame.at[i, "ID магазина"] or new_row[1] != frame.at[i, "ID товара"]):
            i += 1
        if i == len(frame):
            if new_row[1] in goods["ID товара"]:
                if new_row[0] in stores["ID магазина"]:
                    frame.loc[len(frame)] = new_row
                    return "добавление успешно!"
                return "магазина с таким ID не существует!"
            return "товара с таким ID не существует!"
        return "товар с таким ID уже есть в данном магазине!"
    return "неправильный формат входных данных!"

# Dataframe entry addition


# Dataframe entry deletion
def delete_row_from_gsa(frame, number):
    """
    Аргументы:
        frame - dataframe, над которым производятся операции
        number - целое число

    Результаты:
        frame - dataframe "goods_store_amount" c удаленной строкой под номером
        number
    """
    if type(number) != int:
        return "неправильный тип входных данных!"
    if number >= len(frame) or number < 0:
        return "строки под данным номером не существует!"
    frame.drop(frame.index[number], inplace = True)
    return "удаление было выполнено успешно!"


def delete_row_from_gpp(frame, goods, number):
    """
    Аргументы:
        frame - dataframe, над которым производятся операции
        goods - dataframe "goods_store_amount"
        number - целое число

    Результаты:
        frame - dataframe "goods_provider_price" с удаленной строкой под
        номером number
    """
    if type(number) != int:
        return "неправильный тип входных данных!"
    if number >= len(frame) or number < 0:
        return "строки под данным номером не существует!"
    if frame["ID товара"].iloc[number] in goods["ID товара"].unique():
        return "данный товар есть в справочнике 1! Удаление невозможно!"
    frame.drop(frame.index[number], inplace = True)
    return "удаление было выполнено успешно!"


def delete_row_from_pc(frame, goods, number):
    """
    Аргументы:
        frame - dataframe, над которым производятся операции
        goods - dataframe "goods_provider_price"
        number - целое число

    Результаты:
        frame - dataframe "provider_contacts" с удаленной строкой под номером
        number
    """
    if type(number) != int:
        return "неправильный тип входных данных!"
    if number >= len(frame) or number < 0:
        return "строки под данным номером не существует!"
    if frame["Поставщик"].iloc[number] in goods["Поставщик"].unique():
        return "данный товар есть в справочнике 2! Удаление невозможно!"
    frame.drop(frame.index[number], inplace = True)
    return "удаление было выполнено успешно!"



def delete_row_from_sa(frame, goods, number):
    """
    Аргументы:
        frame - dataframe, над которым производятся операции
        goods - dataframe "goods_store_amount"
        number - целое число

    Результаты:
        frame - dataframe "store_address" с удаленной строкой под номером
        number
    """
    if type(number) != int:
        return "неправильный тип входных данных!"
    if number >= len(frame) or number < 0:
        return "строки под данным номером не существует!"
    if frame["ID магазина"].iloc[number] in goods["ID магазина"].unique():
        return "данный магазин есть в справочнике 1! Удаление невозможно!"
    frame.drop(frame.index[number], inplace = True)
    return "удаление было выполнено успешно!"
# Dataframe entry deletion


# Dataframe export
def save_to_excel(frame, filename, flag):
    """
    Аргументы:
        frame - сохраняемый dataframe
        filename - название файла
        flag - bool

    Данная функция сохраняет frame в .xlsx файл
    """
    frame.to_excel(f"./output/{filename}", index = flag)


def save_to_pickle(frame, filename):
    """
    Аргументы:
        frame - сохраняемый dataframe
        filename - название файла

    Данная функция сохраняет frame в .pkl файл
    """
    frame.to_pickle(f"./output/{filename}")


def save_changes(frame, filename):
    """
    Аргументы:
        frame - сохраняемый dataframe
        filename - название файла

    Данная функция сохраняет изменения frame в .pkl файл
    """
    frame.to_pickle(f"./data/{filename}")


def save_as(frame):
    """
    Аргументы:
        frame - сохраняемый dataframe

    Данная функция открываыет окно "Сохранить как..." для сохранения frame в
    .xlsx файл с именем файла, введенным пользователем
    """
    sa = tk.filedialog.asksaveasfilename(defaultextension = '.xlsx',
                                         filetypes = [("MS Excel file", "*.xlsx")])
    if len(sa) != 0:
        frame.to_excel(sa)
