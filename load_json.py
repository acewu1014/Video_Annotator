from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QSlider, QStyle, QSizePolicy, QFileDialog, QScrollArea, QFormLayout, QGridLayout, QShortcut
from PyQt5.QtCore import Qt
from functools import partial
import json 

class VideoLabel(QWidget):
    def __init__(self, videoplayer):
        super().__init__()
        self.file_name = ""
        self.file_path = ""
        self.videoplayer = videoplayer
        self.shot_idx = 0
        self.entries = []
        self.keywords_origin = []
        self.genres_origin = []
        self.buttons_shots = []
        self.buttons_keywords = [[]]
        self.buttons_artists = [[]]
        self.buttons_genres = [[]]
        self.init_ui()
        self.init_sc()
        
        
    
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
        #keep track of the origins, to reconvery from changes
        self.read_recovery()
        
    def read_recovery(self):
        if len(self.entries):
            self.keywords_origin = self.entries[len(self.entries)-1]['keywords']
            self.genres_origin = self.entries[len(self.entries)-1]['genres']
        print(self.keywords_origin)
        print(type(self.keywords_origin))
        print(self.genres_origin)
        print(type(self.genres_origin))

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
            # button.clicked.connect(partial(self.videoplayer.set_position, entry[0]))
            button.clicked.connect(partial(self.videoplayer.play_segment, entry))
            button.clicked.connect(partial(self.init_shot_info, i))
            button.clicked.connect(partial(self.change_now_shot_index, i))
            button.clicked.connect(partial(self.change_color_shot, button))
        # self.scroll.show()
        shot_area.setLayout(form)
        self.scroll.setWidget(shot_area)
        # hbox = QHBoxLayout()
        print(self.hbox.count())
        # self.hbox.addWidget(self.scroll)
        # hbox.addWidget(self.scroll)
        self.setLayout(self.hbox)
        self.show()

    def init_sc(self):
        self.sc_pause = QShortcut("C", self)
        self.sc_pause.activated.connect(self.copy_former_one)

        self.sc_recovery = QShortcut("R", self)
        self.sc_recovery.activated.connect(self.recovery)

    def change_now_shot_index(self, j):
        self.shot_idx = j

    def init_shot_info(self, j):
        #List the info of No.j entry
        info_area = QWidget()
        entry = self.entries[j]
        keywords = entry["keywords"]
        artists = entry["artists"]
        genres = entry["genres"]
        grid = QGridLayout()
        label1 = QLabel("keywords")
        label2 = QLabel("atrists")
        label3 = QLabel("genres")
        grid.addWidget(label1, 0, 0)
        # grid.addWidget(label2, 0, 2)
        grid.addWidget(label3, 0, 4)
        #Create buttons for each tag
        for i in range(len(keywords)):
            button = QPushButton(keywords[i])
            grid.addWidget(button, i+1, 0)
            self.buttons_keywords.append(button)
            button.clicked.connect(partial(self.delete_keywords, j, keywords[i]))
            button.clicked.connect(partial(self.change_color, button))
        # display artists
        # for i in range(len(artists)):
        #     button = QPushButton(artists[i])
        #     grid.addWidget(button, i+1, 2)
        #     self.buttons_artists.append(button)
        #     button.clicked.connect(partial(self.delete_artists, j, artists[i]))
        #     button.clicked.connect(partial(self.change_color, button))
        for i in range(len(genres)):
            button = QPushButton(genres[i])
            grid.addWidget(button, i+1, 4)
            self.buttons_genres.append(button)
            button.clicked.connect(partial(self.delete_genres, j, genres[i]))
            button.clicked.connect(partial(self.change_color, button))

        # Add select all function
        selectall_keywords = QPushButton("Select all")
        selectall_genres = QPushButton("Select all")
        grid.addWidget(selectall_keywords, 0, 1)
        grid.addWidget(selectall_genres, 0, 5)
        selectall_keywords.clicked.connect(partial(self.delete_all_keywords, grid, j))
        selectall_genres.clicked.connect(partial(self.delete_all_genres, grid, j))
        info_area.setLayout(grid)
        self.info_scroll.setWidget(info_area)
        info_area = QWidget()
        form = QFormLayout()
        
    #TODO: delete button and corresponding entry
    def delete_keywords(self, index, keyword_name):
        # self.entries[index]['keywords'] = self.entries[index]['keywords'].remove(keyword_name)
        if keyword_name in self.entries[index]['keywords']:
            self.entries[index]['keywords'].remove(keyword_name)
        else:
            self.entries[index]['keywords'].append(keyword_name)

    def delete_artists(self, index, artists_name):
        # self.entries[index]['keywords'] = self.entries[index]['keywords'].remove(keyword_name)
        if artists_name in self.entries[index]['artists']:
            self.entries[index]['artists'].remove(artists_name)
        else:
            self.entries[index]['artists'].append(artists_name)
    def delete_genres(self, index, genres_name):
        # self.entries[index]['keywords'] = self.entries[index]['keywords'].remove(keyword_name)
        if genres_name in self.entries[index]['genres']:
            self.entries[index]['genres'].remove(genres_name)
        else:
            self.entries[index]['genres'].append(genres_name)
    
    def change_color(self, button):
        if button.palette().button().color().value() != 255:
            button.setStyleSheet("background-color: red")
        else:
            button.setStyleSheet("background-color: light gray")
    
    def change_color_red(self, button):
        button.setStyleSheet("background-color: red")

    def change_color_shot(self, button):
        if button.palette().button().color().value() != 255:
            button.setStyleSheet("background-color: green")
        # else:
        #     button.setStyleSheet("background-color: light gray")

    def delete_all_keywords(self, grid, index):
        self.entries[index]['keywords'] = []
        for i in range(1, grid.rowCount()):
            button = grid.itemAtPosition(i, 0)
            if button:
                button = button.widget()
                self.change_color_red(button)

    def delete_all_genres(self, grid, index):
        self.entries[index]['genres'] = []
        for i in range(1, grid.rowCount()):
            button = grid.itemAtPosition(i, 4)
            if button:
                button = button.widget()
                self.change_color_red(button)

    def save_file(self):
        with open(self.file_path , 'w',encoding="utf-8") as outputfile:
            for entry in self.entries:
                json.dump(entry, outputfile, ensure_ascii=False)
                outputfile.write('\n')

    #copy keywords and genres from the former shot(i.e. i-1) 
    def copy_former_one(self):
        if self.shot_idx>0:
            self.entries[self.shot_idx]['keywords'] = self.entries[self.shot_idx - 1]['keywords']
            self.entries[self.shot_idx]['genres'] = self.entries[self.shot_idx - 1]['genres']
            self.init_shot_info(self.shot_idx)
            print("Copy succ")
        else:
            print("now is shot 0")

    def recovery(self):
        self.entries[self.shot_idx]['keywords'] = self.keywords_origin
        self.entries[self.shot_idx]['genres'] = self.genres_origin
        self.init_shot_info(self.shot_idx)
        print("Recovery from the last shot")