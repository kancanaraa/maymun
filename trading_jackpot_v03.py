from typing import Any, Collection
from PyQt5 import QtCore, QtGui, QtWidgets
from tradingchecker_v01 import Ui_MainWindow
import json;
import time
import requests
import datetime


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


def deltatime(coins):
    coin = coinInfo.coin
    for coin in coins:
        gTime=time.gmtime()
        gloTime=time.strftime("%Y-%m-%dT%H:%M:%SZ", gTime)
        coinDate=datetime.datetime(*time.strptime(coinInfo.date, "%Y-%m-%dT%H:%M:%SZ")[:6])
        globTime=datetime.datetime(*time.strptime(gloTime, "%Y-%m-%dT%H:%M:%SZ")[:6])
        coinTime=coinDate
        globalTime=globTime
        timeDif=round((globalTime-coinTime).total_seconds()/60.0,2)
        # print(timeDif)
        od[coin]["res"+str(coinInfo.resolutionNo)+"_date"] = timeDif

def loaddata():
    global obj
    x = requests.get("http://35.157.241.163/getCoinInfosTake")
    payload = json.loads(x.text, object_hook=as_payload)

    for coinInfo in reversed(payload):
        coin = coinInfo.coin
        if (coin not in od):
            od[coin] = {
                "coinName":"",
                "Algorithm":"",
                "res1":"",
                "res2":"",
                "res3":"",
                "res4":"",
                "res5":"",
                "res1_date":"",
                "res2_date":"",
                "res3_date":"",
                "res4_date":"",
                "res5_date":"",
                "status":"",
                "jackpot":"",
                "price":"",
            }
        od[coin]["coinName"] = coin
        od[coin]["Algorithm"] = coinInfo.algorithm
        od[coin]["res"+str(coinInfo.resolutionNo)] = coinInfo.signal
        od[coin]["res"+str(coinInfo.resolutionNo)+"_date"] = coinInfo.date
        od[coin]["price"] = coinInfo.price


    coins=list(od.values())
    deltatime(coins)
    row=0
    ui.coinTable.setRowCount(2*len(coins))
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
        ui.coinTable.setItem(row, col_coinName, QtWidgets.QTableWidgetItem(coin["coinName"]+" Date"))
        ui.coinTable.setItem(row, col_Algorithm, QtWidgets.QTableWidgetItem(coin["Algorithm"]))
        ui.coinTable.setItem(row, col_res1, QtWidgets.QTableWidgetItem(coin["res1_date"]))
        ui.coinTable.setItem(row, col_res2, QtWidgets.QTableWidgetItem(coin["res2_date"]))
        ui.coinTable.setItem(row, col_res3, QtWidgets.QTableWidgetItem(coin["res3_date"]))
        ui.coinTable.setItem(row, col_res4, QtWidgets.QTableWidgetItem(coin["res4_date"]))
        ui.coinTable.setItem(row, col_res5, QtWidgets.QTableWidgetItem(coin["res5_date"]))
        ui.coinTable.setItem(row, col_status, QtWidgets.QTableWidgetItem(coin["status"]))
        ui.coinTable.setItem(row, col_jackpot, QtWidgets.QTableWidgetItem(coin["jackpot"]))
        # ui.coinTable.setItem(row, col_price, QtWidgets.QTableWidgetItem(coin["price"]))
        row=row+1


        ui.coinTable.setItem(row, col_coinName, QtWidgets.QTableWidgetItem(coin["coinName"]))
        ui.coinTable.setItem(row, col_Algorithm, QtWidgets.QTableWidgetItem(coin["Algorithm"]))
        ui.coinTable.setItem(row, col_res1, QtWidgets.QTableWidgetItem(coin["res1"]))
        ui.coinTable.setItem(row, col_res2, QtWidgets.QTableWidgetItem(coin["res2"]))
        ui.coinTable.setItem(row, col_res3, QtWidgets.QTableWidgetItem(coin["res3"]))
        ui.coinTable.setItem(row, col_res4, QtWidgets.QTableWidgetItem(coin["res4"]))
        ui.coinTable.setItem(row, col_res5, QtWidgets.QTableWidgetItem(coin["res5"]))
        for x in range(2,7):
            y="res"+str(x-1)
            if(str(coin[y]) == "buy"):
                ui.coinTable.item(row, x).setBackground(QtGui.QColor(100,100,255))
            elif(str(coin[y]) == "sell"):
                ui.coinTable.item(row, x).setBackground(QtGui.QColor(255,100,100))
            else:
                ui.coinTable.item(row, x).setBackground(QtGui.QColor(255,255,255))
        ui.coinTable.setItem(row, col_status, QtWidgets.QTableWidgetItem(coin["status"]))
        ui.coinTable.setItem(row, col_jackpot, QtWidgets.QTableWidgetItem(coin["jackpot"]))
        ui.coinTable.setItem(row, col_price, QtWidgets.QTableWidgetItem(coin["price"]))
        row=row+1


        if ("BTC" in coin["coinName"]):
            btcs=coin
            btcrow=0   
            ui.btcTable.setRowCount(1)
            ui.btcTable.setItem(btcrow, 0, QtWidgets.QTableWidgetItem(btcs["Algorithm"]))
            ui.btcTable.setItem(btcrow, 1, QtWidgets.QTableWidgetItem(btcs["res1"]))
            ui.btcTable.setItem(btcrow, 2, QtWidgets.QTableWidgetItem(btcs["res2"]))
            ui.btcTable.setItem(btcrow, 3, QtWidgets.QTableWidgetItem(btcs["res3"]))
            ui.btcTable.setItem(btcrow, 4, QtWidgets.QTableWidgetItem(btcs["res4"]))
            for x in range(1,5):
                y="res"+str(x)
                if(str(btcs[y]) == "buy"):
                    ui.btcTable.item(btcrow, x).setBackground(QtGui.QColor(100,100,255))
                elif(str(btcs[y]) == "sell"):
                    ui.btcTable.item(btcrow, x).setBackground(QtGui.QColor(255,100,100))
                else:
                    ui.btcTable.item(btcrow, x).setBackground(QtGui.QColor(255,255,255))
            ui.btcTable.setItem(btcrow, 5, QtWidgets.QTableWidgetItem(btcs["status"]))
            ui.btcTable.setItem(btcrow, 6, QtWidgets.QTableWidgetItem(btcs["price"]))

    


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    qtimer = QtCore.QTimer()
    qtimer.timeout.connect(loaddata)
    qtimer.start(1000)
    sys.exit(app.exec_())

