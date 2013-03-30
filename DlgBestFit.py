from PyQt4.QtGui import *
from PyQt4.QtCore import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QTAgg as NavigationToolbar)
from MCMCHistory import MCMCBestFit

class DlgBestFit(QDialog):
    def __init__(self, mcmcBestFit, parent = None):
        '''
        '''
        if not isinstance(mcmcBestFit, MCMCBestFit):
            raise TypeError

        super(DlgBestFit,self).__init__(parent)
        tr = self.tr
        self.setWindowTitle(tr('BestFit'))
        self.setAttribute(Qt.WA_DeleteOnClose)

        self._create_main_frame()
        self._updatePlot(mcmcBestFit)

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

    def _updatePlot(self, mcmcBestFit):
        tr = self.tr
        self.fig.clear()

        ax = self.fig.add_subplot(111)

        xx = mcmcBestFit.bestFit[:,0]
        yy = mcmcBestFit.bestFit[:,1]
        ax.plot(xx, yy, label='Fitting')

        xx = mcmcBestFit.exptXS[:,0]
        yy = mcmcBestFit.exptXS[:,1]
        ax.scatter(xx, yy, marker='s', s=60, c='red', label='Experiment')

        ax.set_xlabel(r"LET $(\mathrm{MeV}/\mathrm{cm}^2/\mathrm{mg})$", fontsize=16)
        ax.set_ylabel(r"$\sigma /bit\,(cm^2)$", fontsize=16, fontweight="bold")
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.11),
                  fancybox=True, shadow=False, ncol=1)

        xlabels = ax.get_xticklabels()
        for lbl in xlabels:
            lbl.set_rotation(-15)
            lbl.set_ha('left')
        ax.grid(True)
        self.canvas.draw()
