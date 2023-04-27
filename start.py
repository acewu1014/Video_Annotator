from PyQt5.QtWidgets import QApplication, QAction, QMainWindow, QWidget, QStatusBar, QMenu, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QSlider, QStyle, QSizePolicy, QFileDialog, QMenuBar
from VideoPlayer import VideoPlayer
from PyQt5.QtGui import QIcon, QPalette
from PyQt5 import QtGui
from PyQt5.QtCore import  Qt, QRect
from load_json import VideoLabel
from functools import partial
class container(QMainWindow):
    def __init__(self):
        super().__init__()
        self.videoplayer = VideoPlayer()
        self.videolabel = VideoLabel(self.videoplayer)
        self.setWindowTitle("Video Annotator")
        self.setGeometry(350, 100, 900, 800)
        self.setWindowIcon(QIcon('window_icon.png'))
        
        self.init_menubar()
        self.init_ui()
    
    def init_ui(self):
        p = self.palette()
        p.setColor(QPalette.Window, Qt.white)
        self.setPalette(p)
        self.test_label = QLabel()
        self.test_label.setText("Json loader")
        self.test_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.hboxLayout = QHBoxLayout()
        self.hboxLayout.addWidget(self.videoplayer)
        self.hboxLayout.addWidget(self.videolabel)
        wid = QWidget()
        wid.setLayout(self.hboxLayout)
        self.setCentralWidget(wid)

    def init_menubar(self):
        # menubar = QtGui.MenuBar()
        # menubar = QMenuBar(self)
        menubar = self.menuBar()
        menu_file = QMenu('FILE', self)
        menubar.addMenu(menu_file)
        action_open = QAction('OPEN VIDEO', self)
        # action_open_json = QAction('OPEN LABEL')
    
        menu_file.addAction(action_open)
        # menu_file.addAction(action_open_json)
        # add an open file corresponding action
        
        action_open.triggered.connect(self.open_file)
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
    


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = container()
    window.show()
    # window.show()
    sys.exit(app.exec_())

