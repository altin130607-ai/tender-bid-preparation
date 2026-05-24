import sys
import os
import shutil
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QDateEdit,
                               QComboBox, QPushButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox)
from PySide6.QtCore import QDate

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Подготовка тендерной заявки")

        # Папка для хранения прикреплённых файлов
        self.upload_dir = "uploaded_files"
        os.makedirs(self.upload_dir, exist_ok=True)

        # --- Поля ввода ---
        noticeLabel = QLabel("Номер извещения:")
        self.noticeEdit = QLineEdit()

        companyLabel = QLabel("Организация:")
        self.companyEdit = QLineEdit()

        nmckLabel = QLabel("НМЦК (₽):")
        self.nmckEdit = QLineEdit()
        self.nmckEdit.setPlaceholderText("0")

        # Загрузка файлов
        self.filesList = []
        self.uploadBtn = QPushButton("Загрузить файлы")
        self.filesLabel = QLabel("Файлов: 0")

        # Статус и срок
        statusLabel = QLabel("Статус подготовки:")
        self.statusCombo = QComboBox()
        self.statusCombo.addItems(["На проверке", "Согласована", "Отклонена"])

        deadlineLabel = QLabel("Срок подачи:")
        self.deadlineEdit = QDateEdit()
        self.deadlineEdit.setCalendarPopup(True)
        self.deadlineEdit.setDate(QDate.currentDate())

        # --- Кнопки ---
        addButton = QPushButton("Добавить")
        deleteButton = QPushButton("Удалить")

        # --- Таблица ---
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels([
            "Номер извещения", "Организация", "НМЦК (₽)",
            "Прикреплённые файлы", "Статус", "Срок подачи"
        ])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        # --- Компоновка ---
        row1 = QHBoxLayout()
        row1.addWidget(noticeLabel)
        row1.addWidget(self.noticeEdit)
        row1.addWidget(companyLabel)
        row1.addWidget(self.companyEdit)
        row1.addWidget(nmckLabel)
        row1.addWidget(self.nmckEdit)

        row2 = QHBoxLayout()
        row2.addWidget(self.uploadBtn)
        row2.addWidget(self.filesLabel)
        row2.addWidget(statusLabel)
        row2.addWidget(self.statusCombo)
        row2.addWidget(deadlineLabel)
        row2.addWidget(self.deadlineEdit)
        row2.addWidget(addButton)
        row2.addWidget(deleteButton)

        mainLayout = QVBoxLayout(self)
        mainLayout.addLayout(row1)
        mainLayout.addLayout(row2)
        mainLayout.addWidget(self.table)

        # --- Сигналы ---
        self.uploadBtn.clicked.connect(self.load_files)
        addButton.clicked.connect(self.add_record)
        deleteButton.clicked.connect(self.delete_record)

    def load_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Выберите файлы для заявки")
        if not files:
            return
        for file_path in files:
            # Копируем файл в папку uploaded_files
            base_name = os.path.basename(file_path)
            dest_path = os.path.join(self.upload_dir, base_name)
            shutil.copy(file_path, dest_path)
            self.filesList.append(dest_path)
        self.filesLabel.setText(f"Файлов: {len(self.filesList)}")

    def add_record(self):
        if not self.noticeEdit.text().strip():
            QMessageBox.warning(self, "Ошибка", "Заполните номер извещения")
            return
        if not self.companyEdit.text().strip():
            QMessageBox.warning(self, "Ошибка", "Заполните организацию")
            return

        row = self.table.rowCount()
        self.table.insertRow(row)

        self.table.setItem(row, 0, QTableWidgetItem(self.noticeEdit.text()))
        self.table.setItem(row, 1, QTableWidgetItem(self.companyEdit.text()))
        self.table.setItem(row, 2, QTableWidgetItem(self.nmckEdit.text() if self.nmckEdit.text() else "0"))

        # Отображаем имена файлов (без полного пути)
        file_names = "\n".join([os.path.basename(f) for f in self.filesList]) if self.filesList else "—"
        self.table.setItem(row, 3, QTableWidgetItem(file_names))

        self.table.setItem(row, 4, QTableWidgetItem(self.statusCombo.currentText()))
        self.table.setItem(row, 5, QTableWidgetItem(self.deadlineEdit.date().toString("yyyy-MM-dd")))

        self.clear_form()

    def delete_record(self):
        row = self.table.currentRow()
        if row >= 0:
            self.table.removeRow(row)
        else:
            QMessageBox.warning(self, "Ошибка", "Выберите строку для удаления")

    def clear_form(self):
        self.noticeEdit.clear()
        self.companyEdit.clear()
        self.nmckEdit.clear()
        # Удаляем физические файлы из папки uploaded_files
        for f in self.filesList:
            try:
                os.remove(f)
            except:
                pass
        self.filesList.clear()
        self.filesLabel.setText("Файлов: 0")
        self.statusCombo.setCurrentIndex(0)
        self.deadlineEdit.setDate(QDate.currentDate())
        self.noticeEdit.setFocus()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
