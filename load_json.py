from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QSlider, QStyle, QSizePolicy, QFileDialog, QScrollArea
from PyQt5.QtCore import Qt

import json 

class VideoLabel(QWidget):
    def __init__(self):
        super().__init__()
        self.file_name = ""
        self.entries = []
        self.buttons = []
        self.init_ui()
        
        
    
    def init_ui(self):
        self.scroll = QScrollArea(self)
        self.scroll.setGeometry(350, 100, 700, 500)
        self.name = QLabel(self.scroll)
        self.name.setText("Name of the video label")
        self.name.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        # self.button = QPushButton("Shot: {index}".format(index = 20), self.scroll)
        self.scroll_area = QWidget()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.scroll_area)

        hboxlayout = QHBoxLayout()
        hboxlayout.addWidget(self.scroll)
        self.setLayout(hboxlayout)

    def change_text(self, text):
        print(str(text))
        # self.test_label.setText(text)
        # self.test_label.show()

    def open_file(self, file_path):
        # print(self.video_name)
        self.file_name = file_path.split('/')[-1].split('.')[0]
        self.name.setText(str(self.file_name))
        if file_path != '':
            for entry in open(file_path, "r", encoding = "utf-8"):
                entry = json.loads(entry)
                self.entries.append(entry)
            self.init_shot_bar()
    
    def init_shot_bar(self):
        for i in range(len(self.entries)):
            button = QPushButton("Shot: {index}".format(index = i), self.scroll_area)
            button.move(0, 40*i)
            button.show()
            self.buttons.append(button)
        # self.scroll.show()
        print(len(self.buttons))