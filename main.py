# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import mariadb
import sys
import csv
import requests
import config as cfg
from PyQt6 import QtCore,QtWidgets,QtGui
from PyQt6.QtCore import QDate, QPoint


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.button = QtWidgets.QPushButton("Speichern in die Datenbank")
        self.button.setStyleSheet("background-color: green")
        self.generate = QtWidgets.QPushButton("Generiere Daten für das Jahr")
        self.generate.setStyleSheet("background-color: green")
        self.btn_feier = QtWidgets.QPushButton("Hole und setze Feiertage")
        self.btn_feier.setStyleSheet("background-color: orange")
        self.addyear = QtWidgets.QPushButton("Springe ein Jahr weiter")
        self.addyear.setStyleSheet("background-color: green")
        self.trunc = QtWidgets.QPushButton("Zurücksetzen der Datenbank")
        self.trunc.setStyleSheet("background-color: red")
        self.delete = QtWidgets.QPushButton("Löschen von Daten aus der Datenbank")
        self.delete.setStyleSheet("background-color: red")

        self.feiertag = QtWidgets.QComboBox()
        self.feiertag.addItem("0")
        self.feiertag.addItem("1")
        self.feiertag.addItem("2")

        self.gruppe = QtWidgets.QComboBox()
        for i in range(1,20):
            self.gruppe.addItem(str(i))
        self.gruppe.setToolTip("Anzahl der Nachdienstgruppen im Jahr:")
        self.gruppe_start = QtWidgets.QComboBox()
        for i in range(1,20):
            self.gruppe_start.addItem(str(i))
        self.gruppe_start.setToolTip("Das Jahr beginnt mit folgender Gruppe:")

        self.start = QtWidgets.QCalendarWidget()
        self.start.setGridVisible(True)
        self.start.setFixedHeight(170)
        #self.start.setGeometry(10,10,100,150)
        currentDate = QDate.currentDate()
        date = QDate()
        date.setDate(currentDate.year(),1,1)
        self.start.setSelectedDate(date)

        self.end = QtWidgets.QCalendarWidget()
        self.end.setGridVisible(True)
        self.end.setFixedHeight(170)
        #self.end.setGeometry(10,10,100,150)
        date = QDate()
        date.setDate(currentDate.year(),12,31)
        self.end.setSelectedDate(date)

        self.table = QtWidgets.QTableWidget()
        #self.table.setGeometry(10,10,100,150)
        self.table.setColumnCount(8)
        self.table.setRowCount(3)
        self.table.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.table.setHorizontalHeaderLabels(["tag_im_jahr","datum","wochentag","textnummer","tag","monat","jahr","feiertag"])
        self.table.setToolTip('feiertag 0=regulaer =1 wenn Feiertag von 8 Uhr beginnt 2 Halberwerktag')
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1,QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2,QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3,QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4,QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(5,QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(6,QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(7,QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(QtWidgets.QLabel("Anzahl der Gruppen: "))
        self.layout.addWidget(self.gruppe)
        self.layout.addWidget(QtWidgets.QLabel("Startgruppe: "))
        self.layout.addWidget(self.gruppe_start)
        self.layout.addWidget(QtWidgets.QLabel("Startdatum: "))
        self.layout.addWidget(self.start)
        self.layout.addWidget(QtWidgets.QLabel("Enddatum: "))
        self.layout.addWidget(self.end)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.addyear)
        self.layout.addWidget(self.generate)
        self.layout.addWidget(self.btn_feier)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.delete)
        self.layout.addWidget(self.trunc)
        self.setLayout(self.layout)

        self.generate.clicked.connect(self.on_generate)
        self.addyear.clicked.connect(self.on_addyear)
        self.button.clicked.connect(self.on_click)
        self.delete.clicked.connect(self.on_delete)
        self.trunc.clicked.connect(self.on_trunc)
        self.btn_feier.clicked.connect(self.on_feier)

    def on_feier(self):
        CSV_URL = cfg.CSV_URL

        if self.table.rowCount() < 5:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
            message = f"Bitte zuerst die Daten laden"
            msg.setText(message)
            msg.setWindowTitle("Info")
            msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            msg.exec()

        else:
            with requests.Session() as s:
                download = s.get(CSV_URL)
                decoded_content = download.content.decode('utf-8')
                cr = csv.reader(decoded_content.splitlines(), delimiter=',')
                my_list = list(cr)
                for row in my_list:
                    for index in range(self.table.rowCount()):
                        if row[2] == self.table.item(index,1).text():
                            if not cfg.Karfreitag:
                                if row[5]=='Karfreitag':
                                    break
                            if int(self.table.item(index,2).text()) < 7:
                                    cb = self.table.indexWidget(self.table.model().index(index, 7))
                                    cb.setCurrentIndex(1)
                            if int(self.table.item(index,5).text()) == 12:
                                    if int(self.table.item(index,4).text()) == 24 or int(self.table.item(index,4).text()) == 31:
                                        cb = self.table.indexWidget(self.table.model().index(index, 7))
                                        cb.setCurrentIndex(2)

    def on_addyear(self):
        self.start.setSelectedDate(self.start.selectedDate().addYears(1))
        self.end.setSelectedDate(self.end.selectedDate().addYears(1))


    def on_delete(self):
        #text, okPressed = QtWidgets.QInputDialog.getText(self,"Jahr zum Löschen:","Jahr", QtWidgets.QLineEdit, "")
        text,okPressed = QtWidgets.QInputDialog.getText(self,'Jahr zum Löschen','Bitte das Jahr eingeben')
        if okPressed and text != '':
            conn = mariadb.connect(
                host=cfg.db_host,
                port=cfg.db_port,
                user=cfg.db_user,
                password=cfg.db_password,
                database=cfg.db_database)

            # Instantiate Cursor
            cur = conn.cursor()
            query = f"DELETE FROM tag_text WHERE jahr ='{text}'"
            cur.execute(query)
            rows = cur.rowcount
            conn.commit()
            conn.close()
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
            message = f"Es wurden {rows} Datensätze aus der Datenbank entfernt"
            msg.setText(message)
            msg.setWindowTitle("Info")
            msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            msg.exec()

    def on_trunc(self):

        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        msg.setText("Wollen Sie Datenbank wirklich zurücksetzen?")
        msg.setWindowTitle("Warnung")
        msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        retvalue = msg.exec()
        if retvalue == QtWidgets.QMessageBox.StandardButton.Yes:
            conn = mariadb.connect(
                host=cfg.db_host,
                port=cfg.db_port,
                user=cfg.db_user,
                password=cfg.db_password,
                database=cfg.db_database)
            cur = conn.cursor()
            query = f"TRUNCATE Table tag_text"
            cur.execute(query)
            print(cur.rowcount)
            conn.commit()
            conn.close()
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
            msg.setText("Datenbank zurückgesetzt")
            msg.setWindowTitle("Info")
            msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            msg.exec()


    def on_click(self):
        #date = self.start.selectedDate()
        #print(date)
        #print(date.dayOfWeek())
        #print(date.daysTo(self.end.selectedDate()))
        #print("----------------------------")
        #while date.__lt__(self.end.selectedDate()):
        #    date = date.addDays(1)
        #    print(date)
        #print("---------------------------")
        #print(self.gruppe.currentText())
        #print("clicked")

        conn = mariadb.connect(
            host=cfg.db_host,
            port=cfg.db_port,
            user=cfg.db_user,
            password=cfg.db_password,
            database=cfg.db_database)

        # Instantiate Cursor
        cur = conn.cursor()
        for index in range(self.table.rowCount()):
            dayofyear = int(self.table.item(index,0).text())
            date = self.table.item(index,1).text()
            weekday = self.table.item(index,2).text()
            textnumber = int(self.table.item(index,3).text())
            tag = int(self.table.item(index,4).text())
            month = int(self.table.item(index,5).text())
            year = int(self.table.item(index,6).text())
            cb = self.table.indexWidget(self.table.model().index(index,7))
            feiertag = cb.currentText()
            #print(dayofyear,date,weekday,textnumber,tag,month,year,feiertag)
            query = (f"INSERT INTO tag_text (tag_im_jahr,datum,wochentag,text_nr,tag,monat,jahr,feiertag)"
                 f" VALUES ('{dayofyear}', '{date}', '{weekday}', '{textnumber}', '{tag}', '{month}', '{year}', '{feiertag}')")
            cur.execute(query)
            #print(cur.rowcount)
            conn.commit()


        conn.close()

        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
        msg.setText("Daten erfolgreich eingetragen")
        msg.setWindowTitle("Info")
        msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        msg.exec()




    def on_generate(self):
        self.table.setRowCount(self.start.selectedDate().daysTo(self.end.selectedDate())+1)
        date = self.start.selectedDate()
        gruppe = int(self.gruppe_start.currentText())
        for index in range(self.table.rowCount()):
            #self.table.setItem(index,1,str(index))

            self.table.setItem(index,0,QtWidgets.QTableWidgetItem(str(date.dayOfYear())))
            self.table.setItem(index,1,QtWidgets.QTableWidgetItem(str(date.toPyDate())))
            self.table.setItem(index,2,QtWidgets.QTableWidgetItem(str(date.dayOfWeek())))
            if gruppe <= int(self.gruppe.currentText()):
                self.table.setItem(index,3,QtWidgets.QTableWidgetItem(str(gruppe)))
            else:
                gruppe = 1
                self.table.setItem(index, 3, QtWidgets.QTableWidgetItem(str(gruppe)))
            self.table.setItem(index,4,QtWidgets.QTableWidgetItem(str(date.day())))
            self.table.setItem(index,5,QtWidgets.QTableWidgetItem(str(date.month())))
            self.table.setItem(index,6,QtWidgets.QTableWidgetItem(str(date.year())))

            combo = QtWidgets.QComboBox()
            combo.addItem("0")
            combo.addItem("1")
            combo.addItem("2")
            self.table.setIndexWidget(self.table.model().index(index,7),combo)
            date = date.addDays(1)
            gruppe += 1

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Strg+F8 to toggle the breakpoint.

    conn = mariadb.connect(
        host="10.100.160.169",
        port=3306,
        user="bitnami",
        password="bitnami")

    # Instantiate Cursor
    cur = conn.cursor()
    print(cur)
    conn.close()




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    widget = MyWidget()
    widget.resize(1000,800)
    widget.show()
    sys.exit(app.exec())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
