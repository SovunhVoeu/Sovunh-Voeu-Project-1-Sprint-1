"""
Author: Sovunh Voeu
Created: 3/7/2025
"""
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QPushButton,
    QLabel,
    QComboBox
    )
# import sys
import sqlite3


class UserSelectionWindow(QWidget):
    def __init__(self, db_path = "jobs.db"):
        super().__init__()
        self.db_path = db_path
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Select User Profiles")
        self.setGeometry(100, 500, 800, 600)

        layout = QVBoxLayout()

        self.user_drop_down = QComboBox()
        self.insert_users()
        self.user_drop_down.currentIndexChanged.connect(self.show_user_info)

        self.user_info = QLabel("To see user information, select a user from the drop down.")

        self.select_button = QPushButton("Confirm Selected User")
        self.select_button.clicked.connect(self.user_selected)

        layout.addWidget(self.user_drop_down)
        layout.addWidget(self.user_info)
        layout.addWidget(self.select_button)

        self.setLayout(layout)

    def insert_users (self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM user_data")
        self.users = cursor.fetchall()

        conn.close()

        for user in self.users:
            self.user_drop_down.addItem(user[1], user[0])

    def show_user_info(self):
        user_id = self.user_drop_down.currentData()
        if user_id is None:
            self.user_info.setText("No user selected.")
            return

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_data WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        conn.close()

        if user:
            name, email, phone, github, linkedin, projects, classes, other = user[1], user[2], user[3], user[4], user[5], user[6], user[7], user[8]
            self.user_info.setText(
                f"Name: {name}\n"
                f"Email: {email}\n"
                f"Phone: {phone}\n"
                f"Github: {github}\n"
                f"LinkedIn: {linkedin}\n"
                f"Projects: {projects}\n"
                f"Classes: {classes}\n"
                f"Other: {other}"
            )

    #THIS IS WHERE YOU WILL TIE THE AI.py to the program
    def user_selected(self):
        user_id = self.user_drop_down.currentData()
        if user_id:
            print(f"User {user_id} selected!")
        self.close()
