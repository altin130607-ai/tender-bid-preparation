#Обновлено 20.05.2026,добавлена проверка статуса
import sys
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QDateEdit,
                               QComboBox, QPushButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QHBoxLayout)
from PySide6.QtCore import QDate

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление тендерными заявками")

        # Поля ввода
        noticeLabel = QLabel("Номер извещения:")
        self.noticeEdit = QLineEdit()

        companyLabel = QLabel("Организация:")
        self.companyEdit = QLineEdit()

        nmckLabel = QLabel("НМЦК (₽):")
        self.nmckEdit = QLineEdit()
        self.nmckEdit.setPlaceholderText("0")

        statusLabel = QLabel("Статус:")
        self.statusCombo = QComboBox()
        self.statusCombo.addItems(["На проверке", "Согласована", "Отклонена"])

        deadlineLabel = QLabel("Срок подачи:")
        self.deadlineEdit = QDateEdit()
        self.deadlineEdit.setCalendarPopup(True)
        self.deadlineEdit.setDate(QDate.currentDate())

        # Кнопка
        addButton = QPushButton("Добавить")

        # Таблица (колонки: Извещение, Организация, НМЦК, Статус, Срок)
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels([
            "Номер извещения", "Организация", "НМЦК (₽)", "Статус", "Срок подачи"
        ])

        # Компоновка полей в одну строку
        inputLayout = QHBoxLayout()
        inputLayout.addWidget(noticeLabel)
        inputLayout.addWidget(self.noticeEdit)
        inputLayout.addWidget(companyLabel)
        inputLayout.addWidget(self.companyEdit)
        inputLayout.addWidget(nmckLabel)
        inputLayout.addWidget(self.nmckEdit)
        inputLayout.addWidget(statusLabel)
        inputLayout.addWidget(self.statusCombo)
        inputLayout.addWidget(deadlineLabel)
        inputLayout.addWidget(self.deadlineEdit)
        inputLayout.addWidget(addButton)

        # Основной вертикальный слой
        mainLayout = QVBoxLayout(self)
        mainLayout.addLayout(inputLayout)
        mainLayout.addWidget(self.table)

        # Связь кнопки
        addButton.clicked.connect(self.add_record)

    def add_record(self):
        row = self.table.rowCount()
        self.table.insertRow(row)

        self.table.setItem(row, 0, QTableWidgetItem(self.noticeEdit.text()))
        self.table.setItem(row, 1, QTableWidgetItem(self.companyEdit.text()))
        self.table.setItem(row, 2, QTableWidgetItem(self.nmckEdit.text()))
        self.table.setItem(row, 3, QTableWidgetItem(self.statusCombo.currentText()))
        self.table.setItem(row, 4, QTableWidgetItem(
            self.deadlineEdit.date().toString("yyyy-MM-dd")
        ))

        # Очистка полей
        self.noticeEdit.clear()
        self.companyEdit.clear()
        self.nmckEdit.clear()
        self.statusCombo.setCurrentIndex(0)
        self.deadlineEdit.setDate(QDate.currentDate())
        self.noticeEdit.setFocus()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
