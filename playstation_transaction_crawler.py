# -*- coding:utf-8 -*-
# author: Tony Chang
# Class: PlayStationTransactionCrawler
# Description: bala...

import requests
import json
from datetime import *
import os
from urllib.parse import *


class PlayStationTransactionCrawler:
    api_version_2: bool = False
    basic_url_v1 = "https://web.np.playstation.com/api/graphql/v1/transact/transaction/history?"
    basic_url_v2 = "https://web.np.playstation.com/api/transactions/v2/history?"
    transactions_list: list[dict] = []
    order_items_list: list[dict] = []
    has_more_flag: bool = True
    limit_per_page: int = 25
    date_today: str = datetime.today().strftime("%Y-%m-%d")
    start_date: str = "2010-01-01T00:00:00.000Z"
    end_date: str
    date_time_now: str
    terms_dict = {
        'PRODUCT_PURCHASE': 'Product Purchase',
        'WALLET_DEBIT': 'Wallet Debit',
        'DEPOSIT_CHARGE': 'Deposit Charge',
        'DEPOSIT_VOUCHER': 'Deposit Voucher',
        'VOUCHER_PURCHASE': 'Voucher Purchase',
        'WALLET_FUNDING': 'Wallet Funding',
        'COMPLETE': 'Complete'
    }

    def __init__(self, start_date: str = "None", end_date: str = "None",
                 limit_per_page: int = 25, api_version_2: str = "False"):
        self.__init_session__()
        self.updateDateTimeNow()
        self.updateStartEndDate(start_date=start_date, end_date=end_date)
        self.updateLimitPerPage(limit_per_page=limit_per_page)
        self.updateAPIVersion2(api_version_2=api_version_2)
        path_root = os.path.join("json_files", self.date_today)
        file_paths = self.searchFiles(path_root=path_root, search_key="Transactions_List")
        if file_paths.__len__():
            file_path = file_paths[0]
            file = open(file=file_path, mode='r', encoding='utf-8')
            self.transactions_list = json.load(fp=file)
            file.close()
        file_paths = self.searchFiles(path_root=path_root, search_key="Order_Items_List")
        if file_paths.__len__():
            file_path = file_paths[0]
            file = open(file=file_path, mode='r', encoding='utf-8')
            self.order_items_list = json.load(fp=file)
            file.close()

    def __init_session__(self):
        self.session = requests.session()
        request_header = {
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 '
                          '(KHTML, like Gecko) Version/15.3 Safari/605.1.15'
        }
        self.session.headers.update(request_header)
        return 0

    def updateStartEndDate(self, start_date: str = "None", end_date: str = "None"):
        if not start_date == "None":
            self.start_date = start_date
        if not end_date == "None":
            self.end_date = end_date
        else:
            self.end_date = self.date_time_now
        # print(self.start_date, self.end_date)
        return 0

    def updateDateTimeNow(self):
        self.date_time_now = str(datetime.utcnow())[:-3].replace(' ', 'T') + "Z"
        return 0

    def updateLimitPerPage(self, limit_per_page: int) -> int:
        self.limit_per_page = limit_per_page
        return self.limit_per_page

    def updateAPIVersion2(self, api_version_2: str = "False"):
        self.api_version_2 = True if (api_version_2 == "True") else False
        return self.api_version_2

    @staticmethod
    def dumpToFile(data_to_dump, file_name: str):
        date_today = datetime.today().strftime("%Y-%m-%d")
        time_now = datetime.now().strftime("%H-%M-%S")
        dump_path = os.path.join("json_files", date_today)
        if not os.path.exists(dump_path):
            os.makedirs(name=dump_path, exist_ok=True)
        new_file_name = file_name + "_" + time_now + ".json"
        dump_file_path = os.path.join("json_files", date_today, new_file_name)
        dump_file = open(file=dump_file_path, mode='w', encoding='utf-8')
        json.dump(obj=data_to_dump, fp=dump_file)
        dump_file.close()
        return 0

    @staticmethod
    def searchFiles(path_root: str, search_key: str):
        file_paths = []
        if os.path.exists(path=path_root):
            for root, lists, files in os.walk(top=path_root):
                for file in files:
                    if search_key in file:
                        file_path = os.path.join(root, file)
                        file_paths.append(file_path)
        return file_paths

    def updateSession(self, str_authorization: str = "None", str_pdccws_p: str = "None"):
        if self.api_version_2 \
                and not str_authorization == "None":
            request_header = {
                'authorization': str_authorization
            }
        elif not str_pdccws_p == "None":
            str_cookie = "pdccws_p=" + str_pdccws_p
            request_header = {
                'Cookie': str_cookie
            }
        else:
            print("FAILED! Session update failed!")
            return 255
        self.session.headers.update(request_header)
        # print(self.session.headers)
        return 0

    def requestURL(self) -> str:
        url_parameters = {
            'limit': str(self.limit_per_page),
            'startDate': self.start_date[:-1] + "+0000",
            'endDate': self.end_date[:-1] + "+0000",
            'includePurged': 'false',
            'transactionTypes': 'CREDIT,CYCLE_SUBSCRIPTION,DEBIT,DEPOSIT_CHARGE,'
                                'DEPOSIT_VOUCHER,PRODUCT_PURCHASE,VOUCHER_PURCHASE'
        }
        append_url_parameters = urlencode(url_parameters)
        if self.api_version_2:
            request_url = self.basic_url_v2 + append_url_parameters
        else:
            request_url = self.basic_url_v1 + append_url_parameters
        # print(request_url)
        return request_url

    def getJSONData(self):
        path_root = os.path.join("json_files", self.date_today)
        file_paths = self.searchFiles(path_root=path_root, search_key=self.end_date)
        if file_paths.__len__():
            file_path = file_paths[0]
            file = open(file=file_path, mode='r', encoding='utf-8')
            json_data = json.load(fp=file)
            file.close()
        else:
            request_url = self.requestURL()
            response = self.session.get(url=request_url)
            json_data = response.json()
            file_name = self.end_date + '_' + str(self.limit_per_page)
            self.dumpToFile(data_to_dump=json_data, file_name=file_name)
        return json_data

    def aLoopGettingJSONData(self):
        json_data = self.getJSONData()
        if json_data.__contains__('nextEndDate'):
            self.has_more_flag = True
            self.end_date = json_data['nextEndDate']
        else:
            self.has_more_flag = False
        if json_data.__contains__('transactions'):
            for transaction_dict in json_data['transactions']:
                # print(transaction_dict)
                self.transactions_list.append(transaction_dict)
        return 0

    def getTransactions(self, str_authorization: str = "None", str_pdccws_p: str = "None"):
        if not self.transactions_list.__len__():
            self.updateSession(str_authorization=str_authorization, str_pdccws_p=str_pdccws_p)
            while self.has_more_flag:
                self.aLoopGettingJSONData()
            self.dumpToFile(data_to_dump=self.transactions_list, file_name="Transactions_List")
        return self.transactions_list

    def generateOrderItemsList(self):
        if not self.order_items_list.__len__():
            for transaction_dict in self.transactions_list:
                trans_additional_info = transaction_dict['additionalInfo']
                trans_detail = transaction_dict['transactionDetail']
                if trans_additional_info.__contains__('orderItems'):
                    for order_item_dict in trans_additional_info['orderItems']:
                        if trans_additional_info.__contains__('walletPayments'):
                            wallet_payment = trans_additional_info['walletPayments'][0]
                            payment_type_key = wallet_payment['transactionType']
                            ledger_status_key = transaction_dict['ledgerStatus']
                            new_order_item_dict = {
                                'productName': order_item_dict['productName'].replace(',', '-'),
                                'totalPrice': order_item_dict['totalPrice']['formattedValue'],
                                'currencyCode': transaction_dict['currencyCode'],
                                'marketCode': transaction_dict['countryCode'],
                                'transactionId': order_item_dict['transactionId'],
                                'transactionDate': trans_detail['transactionDate'],
                                'paymentTypeText': self.terms_dict[payment_type_key],
                                'paymentAmount': wallet_payment['amount']['formattedValue'],
                                'billingInfo': self.terms_dict[payment_type_key],
                                'paymentMethod': self.terms_dict[payment_type_key],
                                'transactionTypeText': trans_detail['transactionTypeText'],
                                'platformId': trans_detail['platformId'],
                                'ledgerStatus': self.terms_dict[ledger_status_key],
                            }
                            self.order_items_list.append(new_order_item_dict)
                        if trans_additional_info.__contains__('chargePayments'):
                            charge_payment = trans_additional_info['chargePayments'][0]
                            payment_type_key = charge_payment['transactionType']
                            ledger_status_key = transaction_dict['ledgerStatus']
                            new_order_item_dict = {
                                'productName': order_item_dict['productName'].replace(',', '-'),
                                'totalPrice': order_item_dict['totalPrice']['formattedValue'],
                                'currencyCode': transaction_dict['currencyCode'],
                                'marketCode': transaction_dict['countryCode'],
                                'transactionId': order_item_dict['transactionId'],
                                'transactionDate': trans_detail['transactionDate'],
                                'paymentTypeText': self.terms_dict[payment_type_key],
                                'paymentAmount': charge_payment['chargeAmount']['formattedValue'],
                                'billingInfo': charge_payment['billingInfo'],
                                'paymentMethod': charge_payment['paymentMethod'],
                                'transactionTypeText': trans_detail['transactionTypeText'],
                                'platformId': trans_detail['platformId'],
                                'ledgerStatus': self.terms_dict[ledger_status_key],
                            }
                            self.order_items_list.append(new_order_item_dict)
                        if trans_additional_info.__contains__('voucherPayments'):
                            voucher_payment = trans_additional_info['voucherPayments'][0]
                            payment_type_key = voucher_payment['transactionType']
                            ledger_status_key = transaction_dict['ledgerStatus']
                            new_order_item_dict = {
                                'productName': order_item_dict['productName'].replace(',', '-'),
                                'totalPrice': order_item_dict['totalPrice']['formattedValue'],
                                'currencyCode': transaction_dict['currencyCode'],
                                'marketCode': transaction_dict['countryCode'],
                                'transactionId': order_item_dict['transactionId'],
                                'transactionDate': trans_detail['transactionDate'],
                                'paymentTypeText': self.terms_dict[payment_type_key],
                                'paymentAmount': voucher_payment['amount']['formattedValue'],
                                'billingInfo': voucher_payment['voucherCode'],
                                'paymentMethod': self.terms_dict[payment_type_key],
                                'transactionTypeText': trans_detail['transactionTypeText'],
                                'platformId': trans_detail['platformId'],
                                'ledgerStatus': self.terms_dict[ledger_status_key],
                            }
                            self.order_items_list.append(new_order_item_dict)
                        if not trans_additional_info.__contains__('walletPayments') \
                                and not trans_additional_info.__contains__('chargePayments') \
                                and not trans_additional_info.__contains__('voucherPayments'):
                            ledger_status_key = transaction_dict['ledgerStatus']
                            new_order_item_dict = {
                                'productName': order_item_dict['productName'].replace(',', '-'),
                                'totalPrice': order_item_dict['totalPrice']['formattedValue'],
                                'currencyCode': transaction_dict['currencyCode'],
                                'marketCode': transaction_dict['countryCode'],
                                'transactionId': order_item_dict['transactionId'],
                                'transactionDate': trans_detail['transactionDate'],
                                'paymentTypeText': "None",
                                'paymentAmount': transaction_dict['invoicePaymentTotal']['formattedValue'],
                                'billingInfo': "None",
                                'paymentMethod': "None",
                                'transactionTypeText': trans_detail['transactionTypeText'],
                                'platformId': trans_detail['platformId'],
                                'ledgerStatus': self.terms_dict[ledger_status_key],
                            }
                            self.order_items_list.append(new_order_item_dict)
                if not trans_additional_info.__contains__('orderItems') \
                        and trans_additional_info.__contains__('voucherPayments'):
                    voucher_payment = trans_additional_info['voucherPayments'][0]
                    product_name_key = transaction_dict['invoiceType']
                    payment_type_key = voucher_payment['transactionType']
                    ledger_status_key = transaction_dict['ledgerStatus']
                    new_order_item_dict = {
                        'productName': self.terms_dict[product_name_key].replace(',', '-'),
                        'totalPrice': transaction_dict['invoiceOrderTotal']['formattedValue'],
                        'currencyCode': transaction_dict['currencyCode'],
                        'marketCode': transaction_dict['countryCode'],
                        'transactionId': trans_detail['transactionId'],
                        'transactionDate': trans_detail['transactionDate'],
                        'paymentTypeText': self.terms_dict[payment_type_key],
                        'paymentAmount': voucher_payment['amount']['formattedValue'],
                        'billingInfo': voucher_payment['voucherCode'],
                        'paymentMethod': self.terms_dict[payment_type_key],
                        'transactionTypeText': trans_detail['transactionTypeText'],
                        'platformId': trans_detail['platformId'],
                        'ledgerStatus': self.terms_dict[ledger_status_key],
                    }
                    self.order_items_list.append(new_order_item_dict)
            self.dumpToFile(data_to_dump=self.order_items_list, file_name="Order_Items_List")
        # print(self.order_items_list)
        # print(self.order_items_list.__len__())
        return self.order_items_list

    def generateCSVFile(self):
        if self.order_items_list.__len__():
            csv_file_path_root = os.path.join("csv_files", self.date_today)
            if not os.path.exists(csv_file_path_root):
                os.makedirs(name=csv_file_path_root, exist_ok=True)
            time_now = datetime.now().strftime("%H-%M-%S")
            csv_file_name = "csv_file_" + time_now + ".csv"
            csv_file_path = os.path.join(csv_file_path_root, csv_file_name)
            csv_file = open(file=csv_file_path, mode='w', encoding='utf-8')
            csv_file.writelines("productName,totalPrice,currencyCode,"
                                + "marketCode,transactionId,transactionDate,"
                                + "paymentTypeText,paymentAmount,billingInfo,"
                                + "paymentMethod,transactionTypeText,platformId,"
                                + "ledgerStatus\n")
            for item_dict in self.order_items_list:
                values = [
                    str(item_dict['productName']), str(item_dict['totalPrice']), str(item_dict['currencyCode']),
                    str(item_dict['marketCode']), str(item_dict['transactionId']), str(item_dict['transactionDate']),
                    str(item_dict['paymentTypeText']), str(item_dict['paymentAmount']), str(item_dict['billingInfo']),
                    str(item_dict['paymentMethod']), str(item_dict['transactionTypeText']), str(item_dict['platformId']),
                    str(item_dict['ledgerStatus'])
                ]
                line_to_write = ",".join(values) + '\n'
                csv_file.writelines(line_to_write)
            csv_file.close()
        else:
            print("self.new_orders_list is empty!")
            return 255
        return 0
