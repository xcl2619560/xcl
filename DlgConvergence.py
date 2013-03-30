from PyQt4.QtGui import *
from PyQt4.QtCore import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QTAgg as NavigationToolbar)
from MCMCHistory import MCMCHistory

class DlgConvergence(QDialog):
    def __init__(self, mcmcHistory, parent=None):
        if not isinstance(mcmcHistory, MCMCHistory): raise TypeError

        super(DlgConvergence, self).__init__(parent)
        tr = self.tr
        self.setWindowTitle(tr('Convergence'))
        self.setAttribute(Qt.WA_DeleteOnClose)

        self._create_main_frame()
        self._updatePlot(mcmcHistory)

    def _create_main_frame(self):
        self.main_frame = QWidget()

        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)
        self.NvgtToolbar = NavigationToolbar(self.canvas, self.main_frame)

        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)  # the matplotlib canvas
        vbox.addWidget(self.NvgtToolbar)
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Close)
        vbox.addWidget(self.buttonBox)
        self.main_frame.setLayout(vbox)
        hbox = QHBoxLayout()
        hbox.addWidget(self.main_frame)
        self.setLayout(hbox)

        self.connect(self.buttonBox, SIGNAL('rejected()'), self.reject)

    def _updatePlot(self, mcmcHistory, label=[]):
        self.fig.clear()

        labels   = mcmcHistory.getPrettyLabel(fmt=MCMCHistory.FmtLatex)
        xx       = list(range(mcmcHistory.size()))

        ax = self.fig.add_subplot(111)
        ax.hold('on')
        for idx in range(4):
            values  = mcmcHistory.getHistory(idx=idx, exclBurnin=False)
            normFactor = mcmcHistory.getNormFactor(idx)
            if not normFactor is None:
                ax.plot(xx, values/normFactor,
                        label = labels[idx]+r'/%.4g'%normFactor)
            else:
                ax.plot(xx, values, label = labels[idx])

        ax.set_xlabel('Times (N)', fontsize=16)
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.11),
                  fancybox=True, shadow=False, ncol=4)

        xlabels = ax.get_xticklabels()
        for lbl in xlabels:
            lbl.set_rotation(-15)
            lbl.set_ha('left')
        ax.grid(True)
        self.canvas.draw()
