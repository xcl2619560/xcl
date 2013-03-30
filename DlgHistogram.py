__all__ = ['DlgHistogram']

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QTAgg as NavigationToolbar)

from MCMCHistory import MCMCHistory

class TabPlot(QWidget):
    def __init__(self,data, label, parent=None):
        '''
        :param data:  list or 1D numpy.adarray
        :param label: x-axis label
        '''
        super(TabPlot, self).__init__(parent)
        self.data = data
        self.label = label

        self._create_main_frame()
        self._updatePlot()

    def _create_main_frame(self):
        self.main_frame = QWidget()

        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)
        self.NvgtToolbar = NavigationToolbar(self.canvas, self.main_frame)

        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)
        vbox.addWidget(self.NvgtToolbar)
        self.main_frame.setLayout(vbox)
        hbox = QHBoxLayout()
        hbox.addWidget(self.main_frame)
        self.setLayout(hbox)

    def _updatePlot(self):
        tr = self.tr
        self.fig.clear()
        data = self.data
        label = self.label

        ax = self.fig.add_subplot( 111 )
        ax.hist( data, bins=11, normed=True, facecolor='green' )
        ax.set_title(tr('mean: %1').arg(sum(data)/len(data), 0, 'g', 4), fontsize=18)
        ax.set_xlabel(label, fontsize=18)
        ax.set_ylabel(tr('Frequency'), fontsize=18)

        xlabels = ax.get_xticklabels()
        for lbl in xlabels:
            lbl.set_rotation(-15)
            lbl.set_ha('left')

        ax.grid(True)
        self.canvas.draw()

class DlgHistogram(QDialog):
    def __init__(self, mcmcHistory, parent=None):
        '''
        '''
        if not isinstance(mcmcHistory, MCMCHistory):
            raise TypeError

        super(DlgHistogram,self).__init__(parent)
        tr = self.tr

        self.mcmcHistory = mcmcHistory
        unicodeLabels = mcmcHistory.getPrettyLabel(fmt=mcmcHistory.FmtUnicode)
        latexLabels   = mcmcHistory.getPrettyLabel(fmt=mcmcHistory.FmtLatex)
        tabWidget = QTabWidget()

        #Init tab widget
        nTab = len(unicodeLabels)
        for idx in xrange(nTab):
            tab = TabPlot(mcmcHistory.getHistory(idx), latexLabels[idx])
            tabWidget.addTab(tab, unicodeLabels[idx])

        self.btBox = QDialogButtonBox(QDialogButtonBox.Close)

        self.setWindowTitle(tr('Histogram'))
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(tabWidget)
        self.mainLayout.addWidget(self.btBox)
        self.setLayout(self.mainLayout)

        self.connect(self.btBox, SIGNAL('rejected()'), self.reject)
