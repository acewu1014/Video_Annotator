from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QSlider, QStyle, QSizePolicy, QFileDialog, QScrollArea, QFormLayout, QGridLayout
from PyQt5.QtCore import Qt
from functools import partial
import json 

class VideoLabel(QWidget):
    def __init__(self, videoplayer):
        super().__init__()
        self.file_name = ""
        self.file_path = ""
        self.videoplayer = videoplayer
        self.entries = []
        self.buttons_shots = []
        self.buttons_keywords = [[]]
        self.buttons_artists = [[]]
        self.init_ui()
        
        
    
    def init_ui(self):
        # self.setGeometry(350, 100, 300, 300)
        self.scroll = QScrollArea(self)
        # self.scroll.setGeometry(350, 100, 700, 500)
        self.name = QLabel()
        self.name.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        # self.button = QPushButton("Shot: {index}".format(index = 20), self.scroll)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.info_scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.name)
        self.hbox.addWidget(self.scroll)
        self.hbox.addWidget(self.info_scroll)
        self.setLayout(self.hbox)
        self.show()

    def change_text(self, text):
        self.name.setText(str(text))
        self.name.show()


    def open_file(self, file_path):
        # print(self.video_name)
        
        if len(self.entries):
            #save
            self.save_file()
        self.file_path = file_path
        self.entries = []
        self.buttons_shots = []
        self.file_name = file_path.split('/')[-1].split('.')[0]
        if file_path != '':
            for entry in open(file_path, "r", encoding = "utf-8"):
                entry = json.loads(entry)
                self.entries.append(entry)
            self.init_shot_bar()

    def clear(self):
        for i in reversed(range(self.hbox.count())): 
            self.hbox.itemAt(i).widget().deleteLater()

    def init_shot_bar(self):
        shot_area = QWidget()
        form = QFormLayout()
        for i in range(len(self.entries)):
            entry =  self.entries[i]["boundary_timecode"]
            button = QPushButton("Shot: {index} \nStart: {start} \nEnd: {end}".format(index = i, start = entry[0], end = entry[1]))
            form.addRow(button)
            self.buttons_shots.append(button)
            button.clicked.connect(partial(self.videoplayer.set_position, entry[0]))
            button.clicked.connect(partial(self.init_shot_info, i))
        # self.scroll.show()
        shot_area.setLayout(form)
        self.scroll.setWidget(shot_area)
        # hbox = QHBoxLayout()
        print(self.hbox.count())
        # self.hbox.addWidget(self.scroll)
        # hbox.addWidget(self.scroll)
        self.setLayout(self.hbox)
        self.show()

    def init_shot_info(self, j):
        #List the info of No.j entry
        info_area = QWidget()
        entry = self.entries[j]
        keywords = entry["keywords"]
        artists = entry["artists"]
        grid = QGridLayout()
        label1 = QLabel("keywords")
        label2 = QLabel("atrists")
        grid.addWidget(label1, 0, 0)
        grid.addWidget(label2, 0, 2)
        #Create buttons for each tag
        for i in range(len(keywords)):
            button = QPushButton(keywords[i])
            grid.addWidget(button, i+1, 0)
            self.buttons_keywords.append(button)
            button.clicked.connect(partial(self.delete_keywords, j, keywords[i]))
            button.clicked.connect(partial(self.change_color, button))
        for i in range(len(artists)):
            button = QPushButton(artists[i])
            grid.addWidget(button, i+1, 2)
            self.buttons_artists.append(button)
            button.clicked.connect(partial(self.delete_artists, j, artists[i]))
            button.clicked.connect(partial(self.change_color, button))
        info_area.setLayout(grid)
        self.info_scroll.setWidget(info_area)
        info_area = QWidget()
        form = QFormLayout()
        
    #TODO: delete button and corresponding entry
    def delete_keywords(self, index, keyword_name):
        # self.entries[index]['keywords'] = self.entries[index]['keywords'].remove(keyword_name)
        self.entries[index]['keywords'].remove(keyword_name)
        print(self.entries[index]['keywords'])

    def delete_artists(self, index, artists_name):
        # self.entries[index]['keywords'] = self.entries[index]['keywords'].remove(keyword_name)
        self.entries[index]['artists'].remove(artists_name)
        print(self.entries[index]['artists'])

    def change_color(self, button):
        button.setStyleSheet("background-color: red")

    def save_file(self):
        with open(self.file_path , 'w',encoding="utf-8") as outputfile:
            for entry in self.entries:
                json.dump(entry, outputfile, ensure_ascii=False)
                outputfile.write('\n')
