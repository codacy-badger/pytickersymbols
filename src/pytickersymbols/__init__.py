#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" pytickersymbols
  Copyright 2019 Slash Gordon
  Use of this source code is governed by an MIT-style license that
  can be found in the LICENSE file.
"""
import os
import yaml


class PyTickerSymbols:

    def __init__(self):
        self.__stocks = None
        yaml_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "data", "stocks.yaml"
        )
        with open(yaml_path) as stocks:
            self.__stocks = yaml.safe_load(stocks)

    def get_all_indices(self):
        """
        Returns all available indices
        :return: list of index names
        """
        return self.__get_sub_items("indices")

    def get_all_industries(self):
        """
        Returns all available industries
        :return: list of industries
        """
        return self.__get_sub_items("industries")

    def get_all_countries(self):
        """
        Returns all available countries
        :return: list of country names
        """
        items = [stock["country"] for stock in self.__stocks["companies"]]
        return list(set(items))

    def get_stocks_by_index(self, index):
        """
        Returns a list with stocks who belongs to given index.
        :param index: name of index
        :return: list of stocks
        """
        return self.__get_items("indices", index)

    def get_yahoo_ticker_symbols_by_index(self, index):
        """
        Returns a list with yahoo ticker symbols who belongs to given index.
        :param index: name of index
        :return: list of yahoo ticker symbols
        """
        my_items = self.__get_items("indices", index)
        return self.__filter_data(my_items, False, True)

    def get_google_ticker_symbols_by_index(self, index):
        """
        Returns a list with google ticker symbols who belongs to given index.
        :param index: name of index
        :return: list of google ticker symbols
        """
        my_items = self.__get_items("indices", index)
        return self.__filter_data(my_items, True, False)

    def get_stocks_by_industry(self, industry):
        """
        Returns a list with stocks who belongs to given index.
        :param industry: name of index
        :return: list of stocks
        """
        return self.__get_items("industries", industry)

    def get_stocks_by_country(self, country):
        """
        Returns a list with stocks who belongs to given country.
        :param country: name of country
        :return: list of stocks
        """

        def __valid(cou, st_cou):
            return isinstance(cou, str) and st_cou.lower() == cou.lower()

        return [
            stock
            for stock in self.__stocks["companies"]
            if __valid(country, stock["country"])
        ]

    def index_to_yahoo_symbol(self, index_name):
        """
        Returns the yahoo symbol for index name.
        :param country: name of index
        :return: yahoo symbol
        """
        yahoo_symbol = None
        for index_item in self.__stocks["indices"]:
            if index_item['name'] == index_name:
                yahoo_symbol = index_item['yahoo']
                break
        return yahoo_symbol

    def __get_items(self, key, val):
        stocks = [
            stock
            for stock in self.__stocks["companies"]
            for item in stock[key]
            if isinstance(val, str) and val.lower() == item.lower()
        ]
        return stocks

    def __get_sub_items(self, key):
        sub_items = list(
            set(
                [
                    item
                    for stock in self.__stocks["companies"]
                    for item in stock[key]
                ]
            )
        )
        return sub_items

    @staticmethod
    def __filter_data(stocks, google, yahoo):
        ticker_list = []
        for stock in stocks:
            sub_list = []
            for symbol in stock["symbols"]:
                if google and "google" in symbol and symbol["google"] != "-":
                    sub_list.append(symbol["google"])
                if yahoo and "yahoo" in symbol and symbol["yahoo"] != "-":
                    sub_list.append(symbol["yahoo"])
            ticker_list.append(sub_list)
        return ticker_list
