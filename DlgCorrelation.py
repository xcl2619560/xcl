from PyQt4.QtGui import *
from PyQt4.QtCore import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QTAgg as NavigationToolbar)
from MCMCHistory import MCMCHistory

class DlgCorrelation(QDialog):
    palette = ['r.', 'b.', 'g.']

    def __init__(self, mcmcHistory, parent = None):
        super(DlgCorrelation,self).__init__(parent)
        tr = self.tr
        self.setWindowTitle(tr('Correlation'))
        self.setAttribute(Qt.WA_DeleteOnClose)

        self._create_main_frame()
        self._updatePlot(mcmcHistory)

    def _create_main_frame(self):
        self.main_frame = QWidget()

        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)
        self.NvgtToolbar = NavigationToolbar(self.canvas, self.main_frame)

        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)
        vbox.addWidget(self.NvgtToolbar)
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Close)
        vbox.addWidget(self.buttonBox)
        self.main_frame.setLayout(vbox)
        hbox = QHBoxLayout()
        hbox.addWidget(self.main_frame)
        self.setLayout(hbox)

        self.connect(self.buttonBox, SIGNAL('rejected()'), self.reject)

    def _updatePlot(self, mcmcHistory):
        self.fig.clear()
        labels = MCMCHistory.getPrettyLabel(fmt=MCMCHistory.FmtLatex)

        nVars = len(labels)
        nPlots = nVars*(nVars-1)/2
        if nPlots<=4:       pos = 220
        elif nPlots<=6:     pos = 230
        elif nPlots<=9:     pos = 330
        elif nPlots<=12:    pos = 340
        else: raise ValueError

        for iy in xrange(nVars):
            for ix in xrange(iy+1, nVars):
                pos += 1

                xx = mcmcHistory.getHistory(ix)
                yy = mcmcHistory.getHistory(iy)
                xLabel = labels[ix]
                yLabel = labels[iy]
                color = self.palette[pos % len(self.palette)]

                ax = self.fig.add_subplot(pos)
                ax.plot(xx, yy, color)
                ax.set_xlabel(xLabel, fontsize=16)
                ax.set_ylabel(yLabel, fontsize=16)

                xlabels = ax.get_xticklabels()
                for lbl in xlabels:
                    lbl.set_rotation(-15)
                    lbl.set_ha('left')
                    ax.grid(True)

        self.canvas.draw()
