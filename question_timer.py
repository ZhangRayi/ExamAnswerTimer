from PyQt6.QtCore import QSize, Qt, QMetaObject, QTimer, QUrl
from PyQt6.QtGui import QMouseEvent, QAction, QIcon
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton, QApplication, QMenu, QSystemTrayIcon
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setObjectName("MainWidget")
        self.setWindowIcon(QIcon('./src/logo.png'))
        self.resize(300, 200)
        self.setMinimumSize(QSize(300, 200))
        self.setMaximumSize(QSize(300, 200))
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton = QPushButton(parent=self)
        self.pushButton.setMinimumSize(QSize(200, 70))
        self.pushButton.setMaximumSize(QSize(200, 70))
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 0, 1, 1)
        self.pushButton_2 = QPushButton(parent=self)
        self.pushButton_2.setMinimumSize(QSize(200, 70))
        self.pushButton_2.setMaximumSize(QSize(200, 70))
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 1, 0, 1, 1)
        self.label = QLabel(parent=self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.pushButton_3 = QPushButton(parent=self)
        self.pushButton_3.setMinimumSize(QSize(70, 70))
        self.pushButton_3.setMaximumSize(QSize(70, 70))
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 1, 1, 1, 1)

        # custom move
        self.drag_start_position = None

        # custom timer
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.total_sec = 300
        self.remaining_minutes = self.total_sec // 60
        self.remaining_seconds = self.total_sec % 60
        # noinspection PyUnresolvedReferences
        self.timer.timeout.connect(self.update_countdown)

        QMetaObject.connectSlotsByName(self)

        # custom tray icon
        self.trayIcon = QSystemTrayIcon(parent=self)
        self.trayIcon.setIcon(QIcon("./src/logo.png"))
        self.trayIcon.setToolTip('答题计时器 - QuestionTimer')
        self.trayIcon.menu = QMenu()
        self.trayIcon.showAction1 = QAction("主窗口", self.trayIcon)
        # noinspection PyUnresolvedReferences
        self.trayIcon.showAction1.triggered.connect(self.showNormal)
        self.trayIcon.showAction2 = QAction("最小化", self.trayIcon)
        # noinspection PyUnresolvedReferences
        self.trayIcon.showAction2.triggered.connect(self.showMinimized)
        self.trayIcon.showAction3 = QAction("退出", self.trayIcon)
        # noinspection PyUnresolvedReferences
        self.trayIcon.showAction3.triggered.connect(QApplication.exit)
        self.trayIcon.menu.addAction(self.trayIcon.showAction1)
        self.trayIcon.menu.addAction(self.trayIcon.showAction2)
        self.trayIcon.menu.addAction(self.trayIcon.showAction3)
        self.trayIcon.setContextMenu(self.trayIcon.menu)
        self.trayIcon.show()
        # noinspection PyUnresolvedReferences
        self.trayIcon.activated.connect(self.show_main_window)

        self.media_player = QMediaPlayer(self)
        self.audio_output = QAudioOutput()
        self.audio_output.setVolume(1)
        self.media_player.setAudioOutput(self.audio_output)

        self.setWindowTitle("答题计时器")
        self.label.setText("5分0秒")
        self.pushButton.setText("开始")
        self.pushButton.setIcon(QIcon('./src/start.png'))
        self.pushButton.setIconSize(QSize(48, 48))
        self.pushButton_2.setText("结束")
        self.pushButton_2.setIcon(QIcon('./src/stop.png'))
        self.pushButton_2.setIconSize(QSize(48, 48))
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setText("延时")
        self.pushButton_3.setIcon(QIcon('./src/more_time.png'))
        self.pushButton_3.setIconSize(QSize(32, 32))
        # noinspection PyUnresolvedReferences
        self.pushButton.clicked.connect(self.click_start)
        # noinspection PyUnresolvedReferences
        self.pushButton_2.clicked.connect(self.click_stop)
        # noinspection PyUnresolvedReferences
        self.pushButton_3.clicked.connect(self.more_time)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_position = event.position().toPoint()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() & Qt.MouseButton.LeftButton:
            delta = event.position().toPoint() - self.drag_start_position
            self.move(self.pos() + delta)

    def show_main_window(self, signal):
        if signal == QSystemTrayIcon.ActivationReason.Trigger:
            self.showNormal()

    def click_start(self):
        self.media_player.setSource(QUrl.fromLocalFile('./src/qs.mp3'))
        self.media_player.play()
        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(True)
        self.timer.start()

    def click_stop(self):
        self.total_sec = 300
        self.label.setStyleSheet('color: black;')
        self.label.setText('5分0秒')
        self.media_player.setSource(QUrl.fromLocalFile('./src/qe.mp3'))
        self.media_player.play()
        self.pushButton.setEnabled(True)
        self.pushButton_2.setEnabled(False)
        self.timer.stop()

    def more_time(self):
        self.total_sec += 300
        self.remaining_minutes = self.total_sec // 60
        self.remaining_seconds = self.total_sec % 60
        formatted_time = f"{self.remaining_minutes:0>2}分{self.remaining_seconds:0>2}秒"
        self.label.setText(formatted_time)
        self.media_player.setSource(QUrl.fromLocalFile('./src/qm.mp3'))
        self.media_player.play()

    def update_countdown(self):
        self.total_sec -= 1
        self.remaining_minutes = self.total_sec // 60
        self.remaining_seconds = self.total_sec % 60
        if self.remaining_minutes == 0 and self.remaining_seconds == 0:
            self.click_stop()
        elif self.remaining_minutes == 0 and self.remaining_seconds <= 59:
            self.label.setStyleSheet("color: red;")
        else:
            self.label.setStyleSheet("color: green;")

        formatted_time = f"{self.remaining_minutes:0>2}分{self.remaining_seconds:0>2}秒"
        self.label.setText(formatted_time)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mw = MainWidget()
    mw.show()
    sys.exit(app.exec())
