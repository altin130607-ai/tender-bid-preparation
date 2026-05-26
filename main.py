import sys
import os
import shutil
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                               QComboBox, QPushButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox,
                               QFormLayout, QGroupBox)
from PySide6.QtCore import Qt

# ---------- Окно авторизации ----------
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Авторизация")
        self.setFixedSize(350, 250)

        layout = QVBoxLayout()

        self.loginEdit = QLineEdit()
        self.loginEdit.setPlaceholderText("Логин")
        self.passwordEdit = QLineEdit()
        self.passwordEdit.setPlaceholderText("Пароль")
        self.passwordEdit.setEchoMode(QLineEdit.Password)

        self.roleCombo = QComboBox()
        self.roleCombo.addItems(["Специалист", "Руководитель"])

        self.loginBtn = QPushButton("Войти")

        layout.addWidget(QLabel("Логин:"))
        layout.addWidget(self.loginEdit)
        layout.addWidget(QLabel("Пароль:"))
        layout.addWidget(self.passwordEdit)
        layout.addWidget(QLabel("Роль:"))
        layout.addWidget(self.roleCombo)
        layout.addWidget(self.loginBtn)

        self.setLayout(layout)
        self.loginBtn.clicked.connect(self.check_auth)

    def check_auth(self):
        login = self.loginEdit.text().strip()
        password = self.passwordEdit.text().strip()
        role = self.roleCombo.currentText()

        if (role == "Специалист" and login == "spec" and password == "1"):
            self.main_window = MainWindow(role)
            self.main_window.show()
            self.close()
        elif (role == "Руководитель" and login == "chief" and password == "1"):
            QMessageBox.information(self, "Авторизация", "Успешная авторизация руководителя")
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")


# ---------- Основное окно (только для специалиста) ----------
class MainWindow(QWidget):
    def __init__(self, role):
        super().__init__()
        self.role = role
        self.setWindowTitle(f"Подготовка тендерной заявки — {role}")
        self.setMinimumSize(1000, 500)

        self.upload_dir = "uploaded_files"
        os.makedirs(self.upload_dir, exist_ok=True)

        self.bids = []

        # Таблица (6 колонок)
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels([
            "Номер извещения", "Себестоимость (₽)", "НДС (%)", "Рентабельность (%)", "Файлы", "Действия"
        ])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        self.build_specialist_ui()

        layout = QVBoxLayout()
        layout.addLayout(self.input_layout)
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.load_test_data()

    # ------------------------------------------------------------
    # Для специалиста
    # ------------------------------------------------------------
    def build_specialist_ui(self):
        self.input_layout = QVBoxLayout()

        # Группа 1: Извещение и контракт
        g1 = QGroupBox("Извещение и проект контракта")
        f1 = QFormLayout()
        self.noticeEdit = QLineEdit()
        self.noticeEdit.setPlaceholderText("Номер извещения")
        self.contractBtn = QPushButton("Загрузить проект контракта")
        self.contractLabel = QLabel("Файл не выбран")
        self.contractFile = None
        f1.addRow("Номер извещения:", self.noticeEdit)
        f1.addRow("Проект контракта:", self.contractBtn)
        f1.addRow("", self.contractLabel)
        g1.setLayout(f1)
        self.input_layout.addWidget(g1)

        # Группа 2: Учредительные документы
        g2 = QGroupBox("Учредительные документы")
        f2 = QFormLayout()
        self.legalBtn = QPushButton("Загрузить документы")
        self.legalLabel = QLabel("Файлов: 0")
        self.legalFiles = []
        f2.addRow("", self.legalBtn)
        f2.addRow("", self.legalLabel)
        g2.setLayout(f2)
        self.input_layout.addWidget(g2)

        # Группа 3: Экономические параметры
        g3 = QGroupBox("Экономические параметры")
        f3 = QFormLayout()
        self.costEdit = QLineEdit()
        self.costEdit.setPlaceholderText("0.00")
        self.vatEdit = QLineEdit()
        self.vatEdit.setPlaceholderText("20")
        self.marginEdit = QLineEdit()
        self.marginEdit.setPlaceholderText("0")
        f3.addRow("Себестоимость (₽):", self.costEdit)
        f3.addRow("НДС (%):", self.vatEdit)
        f3.addRow("Рентабельность (%):", self.marginEdit)
        g3.setLayout(f3)
        self.input_layout.addWidget(g3)

        # Кнопки (только "Добавить заявку")
        btn_layout = QHBoxLayout()
        self.addBtn = QPushButton("Добавить заявку")
        btn_layout.addWidget(self.addBtn)
        self.input_layout.addLayout(btn_layout)

        self.contractBtn.clicked.connect(self.load_contract)
        self.legalBtn.clicked.connect(self.load_legal)
        self.addBtn.clicked.connect(self.add_bid)

        # ------------------------------------------------------------
        # Загрузка файлов
        # ------------------------------------------------------------

    def load_contract(self):
        path, _ = QFileDialog.getOpenFileName(self, "Выберите файл контракта")
        if path:
            dest = os.path.join(self.upload_dir, os.path.basename(path))
            shutil.copy(path, dest)
            self.contractFile = dest
            self.contractLabel.setText(os.path.basename(path))

    def load_legal(self):
        paths, _ = QFileDialog.getOpenFileNames(self, "Выберите учредительные документы")
        for p in paths:
            dest = os.path.join(self.upload_dir, os.path.basename(p))
            shutil.copy(p, dest)
            self.legalFiles.append(dest)
        self.legalLabel.setText(f"Файлов: {len(self.legalFiles)}")

        # ------------------------------------------------------------
        # Работа с заявками
        # ------------------------------------------------------------

    def add_bid(self):
        notice = self.noticeEdit.text().strip()
        if not notice:
            QMessageBox.warning(self, "Ошибка", "Введите номер извещения")
            return
        if not self.contractFile:
            QMessageBox.warning(self, "Ошибка", "Загрузите контракт")
            return
        if not self.legalFiles:
            QMessageBox.warning(self, "Ошибка", "Загрузите учредительные документы")
            return

        try:
            cost = float(self.costEdit.text() or 0)
            vat = float(self.vatEdit.text() or 0)
            margin = float(self.marginEdit.text() or 0)
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Проверьте введённые числа")
            return

        files_list = self.legalFiles.copy()
        if self.contractFile:
            files_list.append(self.contractFile)

        self.bids.append({
            "notice": notice,
            "cost": cost,
            "vat": vat,
            "margin": margin,
            "files": files_list
        })
        self.refresh_table()
        self.clear_form()

    def delete_bid_row(self, row):
        self.bids.pop(row)
        self.refresh_table()

    def refresh_table(self):
        self.table.setRowCount(0)
        for idx, bid in enumerate(self.bids):
            self.table.insertRow(idx)
            self.table.setItem(idx, 0, QTableWidgetItem(bid["notice"]))
            self.table.setItem(idx, 1, QTableWidgetItem(f"{bid['cost']:.2f}"))
            self.table.setItem(idx, 2, QTableWidgetItem(f"{bid['vat']:.2f}"))
            self.table.setItem(idx, 3, QTableWidgetItem(f"{bid['margin']:.2f}"))
            files_str = ", ".join([os.path.basename(f) for f in bid["files"]])
            self.table.setItem(idx, 4, QTableWidgetItem(files_str))

            btn = QPushButton("Удалить")
            btn.clicked.connect(lambda _, r=idx: self.delete_bid_row(r))
            self.table.setCellWidget(idx, 5, btn)

    def clear_form(self):
        self.noticeEdit.clear()
        self.costEdit.clear()
        self.vatEdit.setText("20")
        self.marginEdit.clear()
        self.contractFile = None
        self.contractLabel.setText("Файл не выбран")
        self.legalFiles.clear()
        self.legalLabel.setText("Файлов: 0")

    def load_test_data(self):
        self.bids.append({
            "notice": "0348300000125000015",
            "cost": 2000000.00,
            "vat": 20.00,
            "margin": 15.00,
            "files": ["contract_1.pdf", "ustav_ooo.pdf", "inn_ooo.pdf"]
        })
        self.bids.append({
            "notice": "223-12345678-01",
            "cost": 700000.00,
            "vat": 20.00,
            "margin": 12.00,
            "files": ["contract_2.pdf", "ustav_ao.pdf", "inn_ao.pdf", "egrul_ao.pdf"]
        })
        self.refresh_table()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec())
