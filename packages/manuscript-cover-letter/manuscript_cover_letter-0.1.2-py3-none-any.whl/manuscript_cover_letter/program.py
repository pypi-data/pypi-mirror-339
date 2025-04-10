#!/usr/bin/python3

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QFormLayout, QLineEdit, QTextEdit,
    QVBoxLayout, QHBoxLayout, QRadioButton, QPushButton, QFrame,
    QFileDialog, QGroupBox, QLabel, QButtonGroup, QComboBox, QMessageBox,
    QMainWindow, QAction, QToolBar
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import signal
import json
import os

from manuscript_cover_letter.modules.lib_cover_basic  import generate_cover_basic1
from manuscript_cover_letter.modules.lib_cover_style1 import generate_cover_style1
from manuscript_cover_letter.desktop import create_desktop_file
import manuscript_cover_letter.about as about


class DocForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(about.__program_name__)
        self.setGeometry(50, 50, 1200, 400)

        ## Icon
        # Get base directory for icons
        base_dir_path = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_dir_path, 'icons', 'logo.png')
        self.setWindowIcon(QIcon(icon_path)) 
        

        # Dados de exemplo
        self.fields = {
            "journal": "Name of journal, ex: Journal of Artificial Intelligence and Urban Systems",
            "complete_name": "Full name of corresponding author",
            "university": "University of corresponding author.",
            "country": "Country of corresponding author.",
            "address": "Address of corresponding author, ex: Lavras MG, CEP 37.200-000, Caixa Postal 3037",
            "emails": "john.doe@datainscience.edu\nj.doe.research@gmail.com",
            "telephone": "Tel. +1 416 555 0134 Office",
            "title": "Title of manuscript",
            "summary": "A paragraph explaining why the article is relevant, what is the main contribution, ex: \nThis study..."
        }

        self.input_widgets = {}

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Criação dos campos dinamicamente
        for key, value in self.fields.items():
            if len(value) > 100 or '\n' in value:
                widget = QTextEdit()
            else:
                widget = QLineEdit()
            widget.setPlaceholderText(value)
            widget.setToolTip(value)
            self.input_widgets[key] = widget
            form_layout.addRow(key.capitalize().replace("_", " ") + ":", widget)

            if key in ["journal", "telephone"]:
                tmp = QLabel("")
                tmp.setFixedHeight(widget.fontMetrics().height() * 1)
                form_layout.addRow(tmp,tmp)
                

        self.input_widgets["emails"].setFixedHeight(widget.fontMetrics().height() * 3)

        layout.addLayout(form_layout)

        # Estilo com QComboBox (mais compacto e escalável)
        style_box = QGroupBox("Choose style")
        style_layout = QVBoxLayout()
        self.style_combo = QComboBox()
        self.style_combo.addItems(["basic", "style1", "json"])
        style_layout.addWidget(self.style_combo)
        style_box.setLayout(style_layout)
        layout.addWidget(style_box)

        # Botão Save As
        self.save_button = QPushButton("Save the cover letter")
        self.save_button.clicked.connect(self.save_as_docx)
        layout.addWidget(self.save_button)

        central_widget.setLayout(layout)

        # Adiciona a toolbar
        self.create_toolbar()

    def create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        open_action = QAction(QIcon.fromTheme("x-office-address-book"),"Open JSON", self)
        open_action.triggered.connect(self.load_from_json)
        open_action.setToolTip("Load information from JSON file.")
        toolbar.addAction(open_action)

    def load_from_json(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open JSON files", "", "JSON Files (*.json)")
        if filename:
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Atualiza os widgets com os dados do JSON
                for key, widget in self.input_widgets.items():
                    if key in data:
                        value = data[key]
                        if isinstance(widget, QTextEdit):
                            widget.setPlainText(value)
                        else:
                            widget.setText(value)

                QMessageBox.information(self, "Sucess", "Successful charged data from JSON!")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error loading JSON:\n{str(e)}")

    def save_as_docx(self):
        fields_dict = {}
        for key, widget in self.input_widgets.items():
            if isinstance(widget, QTextEdit):
                value = widget.toPlainText().strip()
            else:
                value = widget.text().strip()
            if not value:
                QMessageBox.critical(
                    self,
                    "Void field",
                    f"The field <b>'{key.replace('_', ' ').capitalize()}'</b> is void. Please fill in all the fields before saving."
                )
                return
            fields_dict[key] = value

        filename, _ = QFileDialog.getSaveFileName(self, "Save cover letter", "", "Word Documents (*.docx);;JSON Files (*.json)")
        if filename:
            style = self.style_combo.currentText()
            if style == "json":
                if not filename.endswith(".json"):
                    filename += ".json"
            else:
                if not filename.endswith(".docx"):
                    filename += ".docx"

            self.generate_docx(filename, fields_dict, style)

    @staticmethod
    def generate_docx(filename, fields_dict, style="basic"):
        if style == "basic":
            generate_cover_basic1(filename, fields_dict)
        elif style == "style1":
            generate_cover_style1(filename, fields_dict)
        elif style == "json":
            with open(filename, 'w', encoding='utf-8') as arquivo:
                json.dump(fields_dict, arquivo, indent=4, ensure_ascii=False)
        else:
            generate_cover_basic1(filename, fields_dict)

def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    create_desktop_file()
    app = QApplication(sys.argv)
    app.setApplicationName(about.__package__) 
    window = DocForm()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

