import sys
import os
import shutil
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                               QPushButton, QVBoxLayout, QFormLayout,
                               QFileDialog, QMessageBox, QGroupBox)
from PySide6.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ввод данных для автоматизированной подготовки заявки")
        self.setMinimumSize(600, 400)

        self.upload_dir = "uploaded_files"
        os.makedirs(self.upload_dir, exist_ok=True)

        # ---- 1. Извещение и проект контракта ----
        group1 = QGroupBox("1. Извещение о закупке и проект контракта")
        form1 = QFormLayout()
        self.noticeEdit = QLineEdit()
        self.noticeEdit.setPlaceholderText("Введите номер извещения")
        self.contractBtn = QPushButton("Загрузить файл")
        self.contractLabel = QLabel("Файл не выбран")
        self.contractFile = None
        form1.addRow("Номер извещения:", self.noticeEdit)
        form1.addRow("Извещение / контракт:", self.contractBtn)
        form1.addRow("", self.contractLabel)
        group1.setLayout(form1)

        # ---- 2. Учредительные и регистрационные документы ----
        group2 = QGroupBox("2. Учредительные и регистрационные документы")
        form2 = QFormLayout()
        self.legalBtn = QPushButton("Загрузить документы")
        self.legalLabel = QLabel("Файлов: 0")
        self.legalFiles = []
        form2.addRow("", self.legalBtn)
        form2.addRow("", self.legalLabel)
        group2.setLayout(form2)

        # ---- 3. Экономические параметры ----
        group3 = QGroupBox("3. Экономические параметры")
        form3 = QFormLayout()
        self.costEdit = QLineEdit()
        self.costEdit.setPlaceholderText("0.00")
        self.vatEdit = QLineEdit()
        self.vatEdit.setPlaceholderText("20")
        self.marginEdit = QLineEdit()
        self.marginEdit.setPlaceholderText("0")
        form3.addRow("Себестоимость (₽):", self.costEdit)
        form3.addRow("НДС (%):", self.vatEdit)
        form3.addRow("Рентабельность (%):", self.marginEdit)
        group3.setLayout(form3)

        # ---- Кнопка сохранения ----
        self.saveBtn = QPushButton("Сохранить данные и запустить подготовку")
        self.saveBtn.setStyleSheet("background-color: #2c7da0; color: white; font-weight: bold; padding: 10px;")

        # ---- Макет ----
        layout = QVBoxLayout()
        layout.addWidget(group1)
        layout.addWidget(group2)
        layout.addWidget(group3)
        layout.addWidget(self.saveBtn)
        self.setLayout(layout)

        # ---- Привязка кнопок ----
        self.contractBtn.clicked.connect(self.load_contract)
        self.legalBtn.clicked.connect(self.load_legal)
        self.saveBtn.clicked.connect(self.save_data)

    def load_contract(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл извещения или контракта")
        if file_path:
            dest = os.path.join(self.upload_dir, os.path.basename(file_path))
            shutil.copy(file_path, dest)
            self.contractFile = dest
            self.contractLabel.setText(os.path.basename(file_path))

    def load_legal(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Выберите учредительные документы")
        for f in files:
            dest = os.path.join(self.upload_dir, os.path.basename(f))
            shutil.copy(f, dest)
            self.legalFiles.append(dest)
        self.legalLabel.setText(f"Файлов: {len(self.legalFiles)}")

    def save_data(self):
        if not self.noticeEdit.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите номер извещения")
            return
        if not self.contractFile:
            QMessageBox.warning(self, "Ошибка", "Загрузите файл извещения/контракта")
            return
        if len(self.legalFiles) == 0:
            QMessageBox.warning(self, "Ошибка", "Загрузите учредительные документы")
            return

        QMessageBox.information(self, "Успех", "Данные сохранены. Система запускает автоматическую подготовку заявки.")
        # Здесь в реальной системе запускался бы парсинг, расчёт, генерация документов
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
