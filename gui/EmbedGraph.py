import sys
import numpy as np
import PyQt5
from matplotlib.backends.qt_compat import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvas
from numpy.linalg import norm
from matplotlib.figure import Figure
from preprocess.entropyChecker import EntropyChecker

class EmbedGraph(QtWidgets.QWidget):

    def __init__(self, parent):
        super().__init__()
        self.static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.layout = QtWidgets.QVBoxLayout(parent)
        self.layout.addWidget(self.static_canvas)


    def addData(self, y, startPos, queryY):
        for i in range(self.layout.count()):
            self.layout.itemAt(i).widget().close()
        self.static_canvas = FigureCanvas(Figure())
        self.static_canvas.figure.subplots_adjust(left=0, right=1, top=1, bottom=0)
        self.normalized_canvas = FigureCanvas(Figure())
        self.normalized_canvas.figure.subplots_adjust(left=0, right=1, top=1, bottom=0)
        self.layout.addWidget(self.static_canvas)
        self.layout.addWidget(self.normalized_canvas)
        self._static_ax = self.static_canvas.figure.subplots()
        self._normal_ax = self.normalized_canvas.figure.subplots()
        self._static_ax.plot(np.linspace(0, len(y), len(y)), y, "-")
        self._static_ax.plot(np.linspace(startPos, startPos + len(queryY), len(queryY)),
                             queryY, "-")
        self._static_ax.spines['right'].set_color('none')
        self._static_ax.spines['top'].set_color('none')
        self._static_ax.axis('off')
        self._static_ax.set_autoscale_on(True)


        normalized_targetY = y[startPos:startPos + len(queryY)]
        normalized_targetY = normalized_targetY / np.sqrt(np.sum(normalized_targetY ** 2))
        self._normal_ax.plot(np.linspace(0, len(queryY), len(queryY)), normalized_targetY, "-")
        normalized_queryY = queryY / np.sqrt(np.sum(queryY ** 2))
        self._normal_ax.plot(np.linspace(0, len(queryY), len(queryY)),
                             normalized_queryY, "-")
        self._normal_ax.spines['right'].set_color('none')
        self._normal_ax.spines['top'].set_color('none')
        self._normal_ax.axis('off')
        self._normal_ax.set_autoscale_on(True)

if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    matchHeatGraph = PyQt5.QtWidgets.QGraphicsView()
    matchHeatGraph.setGeometry(QtCore.QRect(0, 0, 351, 351))
    # matchHeatGraph.setWidgetResizable(True)
    matchHeatGraph.setObjectName("matchHeatGraph")
    # layout = QtWidgets.QVBoxLayout(matchHeatGraph)
    #
    # graph = EmbedGraph(matchHeatGraph)
    # graph.addData(np.tan(np.linspace(0, 600, 600)))
    layout = QtWidgets.QVBoxLayout(matchHeatGraph)
    static_canvas = FigureCanvas(Figure())
    static_canvas.figure.subplots_adjust(left=0, right=1, top=1, bottom=0)
    layout.addWidget(static_canvas)
    axis = static_canvas.figure.subplots()
    x = np.linspace(0, 600, 600)
    y = np.tan(x)
    z = np.sin(np.linspace(0, 150, 150))
    axis.plot(x, y, "-")
    axis.plot(np.linspace(80, 80 + 150, 150), z, "-")
    # static_canvas.show()
    axis.axis('off')
    axis.set_autoscale_on(True)
    axis.set_xmargin(0)
    axis.set_ymargin(0)
    matchHeatGraph.show()
    # graph.addData(np.square(np.linspace(0, 600, 600)))
    # graph.addData(np.tan(np.linspace(0, 600, 600)))

    qapp.exec_()