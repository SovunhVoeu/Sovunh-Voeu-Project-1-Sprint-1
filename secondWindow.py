"""
Author: Sovunh Voeu
Created: 2/18/2025
Edited: 3/4/2025
"""
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QPushButton,
    QLineEdit,
    QFormLayout,
    QMessageBox,
    QLabel,
    QTextEdit,
    QApplication
    )
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
# import sqlite3
# from ai import prompts, example_main
from thirdWindow import UserSelectionWindow


class SecondWindow(QWidget):
    def __init__(self, db: QSqlDatabase):
        super().__init__()
        self.db = db

        self.setWindowTitle("User Profile Input Window")
        self.setGeometry(1000, 100, 800, 600)

        layout = QVBoxLayout()
        self.details_label = QLabel("Add your information to the boxes that apply to you. Once each box is filled or "
                                    "left blank you may click the Save Information button at the bottom of the page.\n"
                                    " If you would like to create a resume and cover letter click the Open User "
                                    "Selection Window button.")
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

        # RESUME BUTTON CREATE THE FUNCTION FOR THIS
        # self.create_resume_button = QPushButton("Create Resume And Cover Letter")
        # self.create_resume_button.clicked.connect(self.create_resume)
        # layout.addWidget(self.create_resume_button)

        self.selection_window_button = QPushButton("Open User Selection Window")
        self.selection_window_button.clicked.connect(self.open_users_profiles_window)
        layout.addWidget(self.selection_window_button)

        self.setLayout(layout)

    def save_user_data(self):
        if not self.db.isOpen():
            self.db.open()

        query = QSqlQuery(self.db)
        query.prepare("""
                INSERT INTO user_data (name, email, phone, github, linkedin, projects, classes, other)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """)
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        phone = self.phone_input.text().strip()
        github = self.github_input.text().strip()
        linkedin = self.linkedin_input.text().strip()
        projects = self.projects_input.toPlainText().strip()
        classes = self.classes_input.toPlainText().strip()
        other = self.other_input.toPlainText().strip()

        query.addBindValue(name)
        query.addBindValue(email)
        query.addBindValue(phone)
        query.addBindValue(github)
        query.addBindValue(linkedin)
        query.addBindValue(projects)
        query.addBindValue(classes)
        query.addBindValue(other)

        if query.exec():
            self.db.commit()
            QMessageBox.information(self, "Successful", "The User Information was saved, "
                                                        "Refresh the db for updated info.")
        else:
            QMessageBox.critical(self, "Database Error", f"Error saving data: {query.lastError().text()}")

    # def create_resume(self, window):
    #     try:
    #         example_main()
    #         QMessageBox.information(window, "Resume and Cover Letter", "Resume and cover letter successfully created")
    #     except Exception as e:
    #         QMessageBox.critical(window, "Error", f"Error creating resume and cover letter: {e}")

    def open_users_profiles_window(self):
        self.user_data_window = UserSelectionWindow("jobs.db")
        self.user_data_window.show()

    def quit(self):
        QApplication.instance().quit()
