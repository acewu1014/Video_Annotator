import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QSlider, QStyle, QSizePolicy, QShortcut
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import  Qt, QUrl, QTimer
from PyQt5.QtGui import QKeySequence

class VideoPlayer(QWidget):
    def __init__(self):
        super().__init__()
        # self.setWindowTitle("Video Player")
        # self.setGeometry(350, 100, 700, 500)
        # self.setWindowIcon(QIcon('window_icon.png'))
        self.video_name = "ssssssss"
        # p = self.palette()
        # p.setColor(QPalette.Window, Qt.white)
        # self.setPalette(p)
        self.init_ui()
        self.init_sc()
        self.timer = QTimer()
                            

    def init_ui(self):
        
        #create a media player object
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        
        #create videowidget object
        videowidget = QVideoWidget()

        #create open button
        openbtn = QPushButton('Open Video')
        openbtn.clicked.connect(self.open_file)
        
        #create a button for playing
        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)

        #create slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        #connect slider movement with mediaplayer
        self.slider.sliderMoved.connect(self.set_position) 

        #create a label that indicate the current playback time
        self.playback_time = QLabel()
        self.playback_time.setText("Start")
        self.playback_time.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        #create a label that indicate the end time of current media
        self.end_time = QLabel()
        self.end_time.setText("End")
        self.end_time.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        #create an blank
        self.blank = QLabel()
        self.blank.setText("")
        self.blank.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        #create a video name label
        self.name = QLabel()
        self.name.setText("Name of the video")
        self.name.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        #create hbox layout
        hboxLayout = QHBoxLayout()
        hboxLayout.setContentsMargins(0,0,0,0)

        #set widgets to hbox layout
        # hboxLayout.addWidget(openbtn)
        hboxLayout.addWidget(self.playBtn)
        hboxLayout.addWidget(self.playback_time)
        hboxLayout.addWidget(self.slider)
        hboxLayout.addWidget(self.end_time)

        #create vbox layout
        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(self.name)
        vboxLayout.addWidget(videowidget)
        vboxLayout.addLayout(hboxLayout)
        # vboxLayout.addWidget(self.label)

        self.setLayout(vboxLayout)


        #setting mediaPlayer output
        self.mediaPlayer.setVideoOutput(videowidget)

        #Connect media states changed
        self.mediaPlayer.stateChanged.connect(self.media_state_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)


    def open_file(self, file_path):
        # filename, _ = QFileDialog.getOpenFileName(self, "Open Video")
        self.video_name = file_path.split('/')[-1].split('.')[0]
        # print(self.video_name)
        self.name.setText(str(self.video_name))
        if file_path != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
            self.playBtn.setEnabled(True)

    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        
        else:
            self.mediaPlayer.play()

    def media_state_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    #position is the current playback position(in miliseconds) 
    def position_changed(self, position):
        self.slider.setValue(position)
        self.playback_time.setText(str(position))
        
    def name_of_video(self):
        print(self.video_name)
        return self.video_name
    #duration is the total playback time in miliseconds of current media
    def duration_changed(self, duration):
        self.slider.setRange(0, duration)
        self.end_time.setText(str(duration))

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)


    def init_sc(self):
        self.sc_pause = QShortcut("Q", self)
        self.sc_pause.activated.connect(self.play_video)
    # def play_segment(self, length):