from PyQt5.QtWidgets import QApplication, QAction, QMainWindow, QWidget, QStatusBar, QMenu, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QSlider, QStyle, QSizePolicy, QFileDialog, QMenuBar
from VideoPlayer import VideoPlayer
from PyQt5.QtGui import QIcon, QPalette
from PyQt5 import QtGui
from PyQt5.QtCore import  Qt, QRect
from ann_keyword import VideoLabel
from ann_keywithpred import VideoLabelandprediction
from genres_load_json import VideoGenresLabel
from functools import partial

class container(QMainWindow):
    def __init__(self):
        super().__init__()
        self.videoplayer = VideoPlayer()
        self.videolabel = VideoLabel(self.videoplayer)
        # self.videolabel = VideoLabelandprediction(self.videoplayer)
        self.setWindowTitle("Video Annotator")
        self.setGeometry(350, 100, 900, 800)
        self.setWindowIcon(QIcon('window_icon.png'))
        self.system = 1
        self.init_menubar()
        self.init_ui()
    
    def init_ui(self):
        p = self.palette()
        p.setColor(QPalette.Window, Qt.white)
        self.setPalette(p)
        self.system_label = QLabel()
        self.system_label.setText("System: " + "Keywords Annotate")
        self.system_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.vboxLayout = QVBoxLayout()
        self.vboxLayout.addWidget(self.system_label)
        self.vboxLayout.addWidget(self.videoplayer)
        self.mid = QWidget()
        self.mid.setLayout(self.vboxLayout)
        self.hboxLayout = QHBoxLayout()
        self.hboxLayout.addWidget(self.mid)
        self.hboxLayout.addWidget(self.videolabel)
        wid = QWidget()
        wid.setLayout(self.hboxLayout)
        self.setCentralWidget(wid)

    def init_menubar(self):
        # menubar = QtGui.MenuBar()
        # menubar = QMenuBar(self)
        menubar = self.menuBar()
        menu_file = QMenu('FILE', self)
        menu_system = QMenu('SYSTEM', self)
        menubar.addMenu(menu_file)
        menubar.addMenu(menu_system)
        action_open = QAction('OPEN VIDEO', self)
        action_save = QAction('SAVE LABEL', self)
        # action_open_json = QAction('OPEN LABEL')
        action_genrefilter = QAction('GENRE FILTER', self)
        action_keywords_annotate = QAction('KEYWORDS ANNOTATE', self)
        action_keywords_filter = QAction('KEYWORDS FILTER', self)
        menu_file.addAction(action_open)
        menu_file.addAction(action_save)
        menu_system.addAction(action_genrefilter)
        menu_system.addAction(action_keywords_annotate)
        menu_system.addAction(action_keywords_filter)
        # menu_file.addAction(action_open_json)
        # add an open file corresponding action
        action_genrefilter.triggered.connect(self.change_genre_filter)
        action_keywords_annotate.triggered.connect(self.change_keyword_annotate)
        action_keywords_filter.triggered.connect(self.change_keyword_filter)
        action_open.triggered.connect(self.open_file)
        action_save.triggered.connect(self.videolabel.save_file)
        # action_open_json.triggered.connect(videolabel.open_file)
        
        # TODO: try to load the video and json at the same time
        # menu_file.triggered[QAction].connect(partial(videolabel.change_text, ""))
        # menu_file.triggered[QAction].connect(videolabel.change_text)

        # menubar.setGeometry(QRect(0, 0, 878, 20))
        # self.setMenuBar(menubar)


    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Video")

        self.videoplayer.open_file(file_path)
        label_file_path = file_path.split('.')[0]
        label_file_path += '.json'
        self.videolabel.open_file(label_file_path)
    
    def change_keyword_annotate(self):
        self.videoplayer = VideoPlayer()
        self.videolabel = VideoLabel(self.videoplayer)
        self.setWindowTitle("Video Annotator")
        self.setGeometry(350, 100, 900, 800)
        
        self.init_ui()

        self.system_label.setText("System: " + "Keywords Annotate")
        self.show()

    def change_keyword_filter(self):
        self.videoplayer = VideoPlayer()
        self.videolabel = VideoLabelandprediction(self.videoplayer)
        self.setWindowTitle("Video Annotator")
        self.setGeometry(350, 100, 900, 800)
    
        self.init_ui()

        self.system_label.setText("System: " + "Keywords Filter")
        self.show()

    def change_genre_filter(self):
        self.videoplayer = VideoPlayer()
        self.videolabel = VideoGenresLabel(self.videoplayer)
        self.setWindowTitle("Video Annotator")
        self.setGeometry(350, 100, 900, 800)
    
        self.init_ui()

        self.system_label.setText("System: " + "Genre Filter")
        self.show()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = container()
    window.show()
    # window.show()
    sys.exit(app.exec_())

