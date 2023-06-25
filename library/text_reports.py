# -*- coding: utf-8 -*-
"""
Talibov S. M., Goncharova K. V., brigade 4, BIV221
"""
import os
import numpy as np
import pandas as pd

os.chdir("C:/work")


def goods_by_provider(frame, providers):
    """
    Аргументы:
        providers - массив строк
        frame - dataframe, над которым производятся операции

    Результат:
        output_frame - dataframe, в котором содержится следующая информация о
        продуктах, поставщиком которых является один из перечисленных в массиве
        providers: Наименование, Поставщик, ID магазина, Адрес,
        Количество после последней закупки
    """
    bool_column = (k in providers for k in frame["Поставщик"])
    output_frame = frame.loc[bool_column, ["Наименование", "Поставщик",
                                           "ID магазина", "Адрес",
                                           "Количество после последней закупки"]]
    return output_frame


def goods_by_price(frame, price):
    """
    Аргументы:
        price - вещественное число
        frame - dataframe, над которым производятся операции

    Результат:
        output_frame - dataframe, в котором содержится следующая информация о
        продуктах, цена продажи которых не меньше, чем price: Наименование,
        Поставщик, ID магазина, Адрес, Цена продажи
    """
    if isinstance(price, int):
        bool_column = (frame["Цена продажи"] >= price)
        output_frame = frame.loc[bool_column, ["Наименование", "Поставщик",
                                               "ID магазина", "Адрес",
                                               "Цена продажи"]]
    else:
        bool_column = [False for i in range(len(frame))]
        output_frame = frame.loc[bool_column]
    return output_frame


def find_store_by_address(frame, place):
    """
    Аргументы:
        place - строка
        frame - dataframe, над которым производятся операции

    Результат:
        output_frame - dataframe, в котором содержится следующая информация о
        магазинах, в адресе которых содержится строка place: ID магазина, Адрес
    """
    bool_column = (place in k for k in frame["Адрес"])
    output_frame = frame.loc[bool_column, ["ID магазина", "Адрес"]]
    return output_frame


def pivot_table_first_version(frame):
    """
    Аргументы:
        frame - dataframe, над которым производятся операции

    Результат:
        frame - dataframe, который является сводной таблицей о проценте наценки
        в разрезе атрибутов Поставщик и ID магазина
    """
    frame = pd.pivot_table(frame, index="Поставщик", columns="ID магазина",
                             values="Процент наценки", aggfunc=['mean','std'])

    return frame


def margin_by_provider(frame):
    """
    Аргументы:
        frame - dataframe, над которым производятся операции

    Результат:
        frame - dataframe, который содержит описательную характеристику наценок
        в зависимости от атрибута Поставщик
    """
    frame = frame[["Процент наценки",
               "Поставщик"]].groupby(["Поставщик"]).agg([np.max, np.min,
                                                         np.mean, np.std,
                                                         np.var])
    return frame


def margin_by_store(frame):
    """
    Аргументы:
        frame - dataframe, над которым производятся операции

    Результат:
        frame - dataframe, который содержит описательную характеристику наценок
        в зависимости от атрибута ID магазин
    """
    frame = frame[["Адрес",
                 "ID магазина",
                 "Процент наценки"]].groupby(["ID магазина",
                                              "Адрес"]).agg([np.max, np.min,
                                                             np.mean, np.std,
                                                             np.var])
    return frame
