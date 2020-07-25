from PyQt5 import QtWidgets, QtCore
from gui.videoQueryUI import VideoQueryUI
import sys
import os
import json
if __name__ == "__main__":
    with open('config.json', 'r') as f:
        config = json.load(f)
    app = QtWidgets.QApplication(sys.argv)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
    MainWindow = QtWidgets.QMainWindow()
    ui = VideoQueryUI(config)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

