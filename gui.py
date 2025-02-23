"""
Author: Sovunh Voeu
Date: 2/18/2025
"""
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QTableView, QPushButton,
                             QLineEdit, QFormLayout, QMessageBox, QLabel, QTextEdit)
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
from PyQt5.QtCore import Qt


class SecondWindow(QWidget):
    def __init__(self, db):
        super().__init__()

        self.db = db
        self.setWindowTitle("User Profile Input Window")
        self.setGeometry(1000, 100, 800, 600)

        layout = QVBoxLayout()
        self.details_label = QLabel("Add your information to the boxes that apply to you. Once each box is filled or "
                                    "left blank you may click the Save Information button at the bottom of the page.")
        layout.addWidget(self.details_label)

        form_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.github_input = QLineEdit()
        self.linkedin_input = QLineEdit()
        self.projects_input = QTextEdit()
        self.classes_input = QTextEdit()
        self.other_input = QTextEdit()

        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Phone:", self.phone_input)
        form_layout.addRow("Github:", self.github_input)
        form_layout.addRow("LinkedIn:", self.linkedin_input)
        form_layout.addRow("Projects:", self.projects_input)
        form_layout.addRow("Classes:", self.classes_input)
        form_layout.addRow("Other:", self.other_input)

        layout.addLayout(form_layout)

        self.save_button = QPushButton("Save Information")
        self.save_button.clicked.connect(self.save_user_data)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_user_data(self):
        name = self.name_input.text()
        email = self.email_input.text()
        phone = self.phone_input.text()
        github = self.github_input.text()
        linkedin = self.linkedin_input.text()
        projects = self.projects_input.toPlainText()
        classes = self.classes_input.toPlainText()
        other = self.other_input.toPlainText()

        query = QSqlQuery(self.db)
        query.prepare("""
            INSERT INTO user_data (name, email, phone, github, linkedin, projects, classes, other)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?)
        """)

        query.addBindValue(name)
        query.addBindValue(email)
        query.addBindValue(phone)
        query.addBindValue(github)
        query.addBindValue(linkedin)
        query.addBindValue(projects)
        query.addBindValue(classes)
        query.addBindValue(other)

        if query.exec():
            QMessageBox.information(self, "Successful", "The User Information was saved, "
                                                        "Refresh the db for updated info.")
        else:
            QMessageBox.critical(self, "Database Error", f"Error saving data: {query.lastError().text()}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Database Viewer")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        self.details_label = QLabel("Select a job title from either two of the lists to view the full details. "
                                    "There may be two jobs with the same title but they are from different companies.\n"
                                    "You can expand the title to see the full job by dragging the right side of the "
                                    "title box or by double clicking the right side of the title box .\n"
                                    "Use the scroll bar or scroll wheel to navigate through the list. "
                                    "Full screen the window for the best view of the data. \n"
                                    "To save information about yourself click the Open User Input Data button.")
        layout.addWidget(self.details_label)

        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('jobs.db')
        if not self.db.open():
            QMessageBox.critical(self, "Database Error", "Unable to open database")
            return

        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        layout.addWidget(self.details_text)

        self.table_view1 = QTableView()
        self.model1 = QSqlQueryModel()
        self.model1.setQuery("SELECT * FROM rapidResults", self.db)
        self.table_view1.setModel(self.model1)
        for col in range(self.model1.columnCount()):
            if col != 4:
                self.table_view1.setColumnHidden(col, True)
        self.table_view1.clicked.connect(self.display_details1)
        layout.addWidget(self.table_view1)

        self.table_view2 = QTableView()
        self.model2 = QSqlQueryModel()
        self.model2.setQuery("SELECT * FROM rapid_jobs2", self.db)
        self.table_view2.setModel(self.model2)
        for col in range(self.model2.columnCount()):
            if col != 1:
                self.table_view2.setColumnHidden(col, True)
        self.table_view2.clicked.connect(self.display_details2)
        layout.addWidget(self.table_view2)

        self.create_user_data_table()

        self.user_data_button = QPushButton("Open User Input Data")
        self.user_data_button.clicked.connect(self.open_second_window)
        layout.addWidget(self.user_data_button)

    def create_user_data_table(self):
        query = QSqlQuery(self.db)
        query.exec("""
        CREATE TABLE IF NOT EXISTS user_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(255),
        email VARCHAR(255),
        phone VARCHAR(255),
        github VARCHAR(255),
        linkedin VARCHAR(255),
        projects VARCHAR(255),
        classes VARCHAR(255),
        other VARCHAR(255)
        )
        """)

    def open_second_window(self):
        self.user_data_window = SecondWindow(self.db)
        self.user_data_window.show()

    def display_details1(self, index):
        row = index.row()
        job_details = []
        for col in range(self.model1.columnCount()):
            column_name = self.model1.headerData(col, Qt.Orientation.Horizontal)
            column_value = self.model1.data(self.model1.index(row, col))
            job_details.append(f"{column_name}: {column_value}")
        self.details_text.setText("\n".join(job_details))

    def display_details2(self, index):
        row = index.row()
        job_details = []
        for col in range(self.model2.columnCount()):
            column_name = self.model2.headerData(col, Qt.Orientation.Horizontal)
            column_value = self.model2.data(self.model2.index(row, col))
            job_details.append(f"{column_name}: {column_value}")
        self.details_text.setText("\n".join(job_details))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
