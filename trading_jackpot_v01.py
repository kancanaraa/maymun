from typing import Any, Collection
from PyQt5 import QtCore, QtGui, QtWidgets
from tradingchecker_v01 import Ui_MainWindow
import json;
import time
import requests

class Payload(object):
    def __init__(self, date, coin, resolutionNo,resolution, signal, price, algorithm):
        self.date = date
        self.coin = coin
        self.resolutionNo = resolutionNo
        self.resolution = resolution
        self.signal = signal
        self.price = price
        self.algorithm = algorithm

ui = Ui_MainWindow()

def as_payload(dct):
    return Payload(dct["date"], dct["coin"], dct["resolutionNo"],dct["resolution"], dct["signal"], dct["price"],dct["algorithm"])



# print(payload[-1].date)
obj =     {"coinName":"",
"Algorithm":"",
"res1":"",
"res2":"",
"res3":"",
"res4":"",
"res5":"",
"status":"",
"jackpot":"",
"price":"",
}

od = {}


def loaddata():
    global obj
    x = requests.get("http://35.157.241.163/getCoinInfos")

    payload = json.loads(x.text, object_hook=as_payload)
    coin = payload[-1].coin
    if (coin not in od):
        od[coin] = {
            "coinName":"",
            "Algorithm":"",
            "res1":"",
            "res2":"",
            "res3":"",
            "res4":"",
            "res5":"",
            "status":"",
            "jackpot":"",
            "price":"",
        }
    od[coin]["coinName"] = coin
    od[coin]["Algorithm"] = payload[-1].algorithm
    od[coin]["res"+str(payload[-1].resolutionNo)] = payload[-1].signal
    od[coin]["price"] = payload[-1].price
    coins=list(od.values())
    row=0
    ui.coinTable.setRowCount(len(coins))
    col_coinName=0
    col_Algorithm=1
    col_res1=2
    col_res2=3
    col_res3=4
    col_res4=5
    col_res5=6
    col_status=7
    col_jackpot=8
    col_price=9
    for coin in coins:
        ui.coinTable.setItem(row, col_coinName, QtWidgets.QTableWidgetItem(coin["coinName"]))
        ui.coinTable.setItem(row, col_Algorithm, QtWidgets.QTableWidgetItem(coin["Algorithm"]))
        ui.coinTable.setItem(row, col_res1, QtWidgets.QTableWidgetItem(coin["res1"]))
        ui.coinTable.setItem(row, col_res2, QtWidgets.QTableWidgetItem(coin["res2"]))
        ui.coinTable.setItem(row, col_res3, QtWidgets.QTableWidgetItem(coin["res3"]))
        ui.coinTable.setItem(row, col_res4, QtWidgets.QTableWidgetItem(coin["res4"]))
        ui.coinTable.setItem(row, col_res5, QtWidgets.QTableWidgetItem(coin["res5"]))
        ui.coinTable.setItem(row, col_status, QtWidgets.QTableWidgetItem(coin["status"]))
        ui.coinTable.setItem(row, col_jackpot, QtWidgets.QTableWidgetItem(coin["jackpot"]))
        ui.coinTable.setItem(row, col_price, QtWidgets.QTableWidgetItem(coin["price"]))
        row=row+1

def btcdata():
    btcs=[{"Algorithm":"kopke",
    "res1":"Buy",
    "res2":"Buy",
    "res3":"Buy",
    "res4":"Buy",
    "status":"Yes",
    "price":"ss3212"}]
    row=0
    ui.btcTable.setRowCount(len(btcs))
    for btc in btcs:
        ui.btcTable.setItem(row, 0, QtWidgets.QTableWidgetItem(btc["Algorithm"]))
        ui.btcTable.setItem(row, 1, QtWidgets.QTableWidgetItem(btc["res1"]))
        ui.btcTable.setItem(row, 2, QtWidgets.QTableWidgetItem(btc["res2"]))
        ui.btcTable.setItem(row, 3, QtWidgets.QTableWidgetItem(btc["res3"]))
        ui.btcTable.setItem(row, 4, QtWidgets.QTableWidgetItem(btc["res4"]))
        ui.btcTable.setItem(row, 5, QtWidgets.QTableWidgetItem(btc["status"]))
        ui.btcTable.setItem(row, 6, QtWidgets.QTableWidgetItem(btc["price"]))
        row=row+1

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui.setupUi(MainWindow)
    btcdata()
    loaddata()
    MainWindow.show()
    qtimer = QtCore.QTimer()
    qtimer.timeout.connect(loaddata)
    qtimer.start(1000)
    sys.exit(app.exec_())

