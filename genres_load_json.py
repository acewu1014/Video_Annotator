from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QScrollArea, QFormLayout, QGridLayout, QShortcut, QSizePolicy
from PyQt5.QtCore import Qt
from functools import partial
import json

class VideoGenresLabel(QWidget):
    def __init__(self, videoplayer):
        super().__init__()
        self.file_name = ""
        self.file_path = ""
        self.videoplayer = videoplayer
        self.shot_idx = 0
        self.entries = []
        self.buttons_shots = []
        self.buttons_genres = [[]]
        self.init_ui()
        self.init_sc()

    def init_ui(self):
        self.scroll = QScrollArea(self)
        self.name = QLabel()
        self.name.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
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
        if len(self.entries):
            self.save_file()

        self.file_path = file_path
        self.entries = []
        self.buttons_shots = []
        self.file_name = file_path.split('/')[-1].split('.')[0]

        if file_path != '':
            with open(file_path, "r", encoding="utf-8") as json_file:
                data = json.load(json_file)
                for entry in data:
                    start_time = entry.get("start_time", 0)
                    end_time = entry.get("end_time", 0)
                    genres = entry.get("genres", "")
                    self.entries.append({
                        "boundary_timecode": [start_time*1000, end_time*1000],
                        "genres": genres,
                    })

            self.init_shot_bar()

    def clear(self):
        for i in reversed(range(self.hbox.count())):
            self.hbox.itemAt(i).widget().deleteLater()

    def init_shot_bar(self):
        shot_area = QWidget()
        form = QFormLayout()

        for i, entry in enumerate(self.entries):
            start_time, end_time = entry["boundary_timecode"]
            button = QPushButton(f"Shot: {i}\nStart: {start_time}\nEnd: {end_time}")
            form.addRow(button)
            self.buttons_shots.append(button)
            button.clicked.connect(partial(self.videoplayer.play_segment, [start_time, end_time]))
            button.clicked.connect(partial(self.init_shot_info, i))
            button.clicked.connect(partial(self.change_now_shot_index, i))
            button.clicked.connect(partial(self.change_color_shot, button))

        shot_area.setLayout(form)
        self.scroll.setWidget(shot_area)
        self.setLayout(self.hbox)
        self.show()

    def init_sc(self):
        self.sc_pause = QShortcut("C", self)
        self.sc_pause.activated.connect(self.copy_former_one)

    def change_now_shot_index(self, j):
        self.shot_idx = j

    def init_shot_info(self, j):
        info_area = QWidget()
        entry = self.entries[j]
        genres = entry["genres"]
        grid = QGridLayout()
        label1 = QLabel("Genres")
        grid.addWidget(label1, 0, 0)

        for i, genre in enumerate(genres):
            button = QPushButton(genre)
            grid.addWidget(button, i + 1, 0)
            self.buttons_genres.append(button)
            button.clicked.connect(partial(self.delete_genres, j, genre))
            button.clicked.connect(partial(self.change_color, button))

        selectall_genres = QPushButton("Select all")
        grid.addWidget(selectall_genres, 0, 1)
        selectall_genres.clicked.connect(partial(self.delete_all_genres, grid, j))

        info_area.setLayout(grid)
        self.info_scroll.setWidget(info_area)
        info_area = QWidget()
        form = QFormLayout()

    def delete_genres(self, index, genre):
        if genre in self.entries[index]['genres']:
            self.entries[index]['genres'].remove(genre)
        else:
            self.entries[index]['genres'].append(genre)

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

    def delete_all_genres(self, grid, index):
        self.entries[index]['genres'] = []
        for i in range(1, grid.rowCount()):
            button = grid.itemAtPosition(i, 0)
            if button:
                button = button.widget()
                self.change_color_red(button)

    def save_file(self):
        with open(self.file_path, 'w', encoding="utf-8") as outputfile:
            for entry in self.entries:
                json.dump(entry, outputfile, ensure_ascii=False)
                outputfile.write('\n')

    def copy_former_one(self):
        if self.shot_idx > 0:
            self.entries[self.shot_idx]['genres'] = self.entries[self.shot_idx - 1]['genres']
            self.init_shot_info(self.shot_idx)
            print("Copy success")
        else:
            print("Now is shot 0")