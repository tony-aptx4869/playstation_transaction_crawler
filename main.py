# -*- coding:utf-8 -*-
# author: Tony Chang
# Python: main.py
# Description: bala...

import os
import configparser
from playstation_transaction_crawler import PlayStationTransactionCrawler


def crawler_method():
    config_file = "config.conf"
    conf = configparser.RawConfigParser()
    if os.path.isfile(config_file):
        conf.read(config_file)
    else:
        print("The file `%s` not exist." % config_file)
        exit(255)
    str_pdccws_p = conf.get("api_version_1", "str_pdccws_p")
    # print(str_pdccws_p)
    str_authorization = conf.get("api_version_2", "str_authorization")
    # print(str_authorization)
    start_date = conf.get("main", "start_date")
    end_date = conf.get("main", "end_date")
    # print(start_date, end_date)
    api_version_2 = conf.get("main", "api_version_2")

    crawler = PlayStationTransactionCrawler(start_date=start_date,
                                            end_date=end_date,
                                            limit_per_page=50,
                                            api_version_2=api_version_2)
    crawler.getTransactions(str_pdccws_p=str_pdccws_p)
    # crawler.getTransactions(str_authorization=str_authorization)
    crawler.generateOrderItemsList()
    crawler.generateCSVFile()


if __name__ == '__main__':
    crawler_method()
