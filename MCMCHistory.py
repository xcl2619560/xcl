__all__ = ['MCMCHistory', 'MCMCBestFit']

import os
import numpy as np

class MCMCHistory(object):

    iSigmaSat = 0
    iL0       = 1
    iW        = 2
    iS        = 3
    iLogp     = 4

    FmtUnicode = 0
    FmtLatex   = 1
    prettyLabels = [
        (unichr(0x03C3)+'_sat',  r'$\sigma_{sat}$'),
        ('LET_th',               r'$L_0$'),
        ('W',                    r'$W$'),
        ('S',                    r'$S$')
    ]

    def __init__(self, history=None, nburnin=0):
        '''
        :param history:       array([ [sigma_sat, let0, lam, k, logp],... ])
        '''
        if not isinstance(history, np.ndarray) and not isinstance(history, list):
            raise TypeError

        n, _ = np.shape(history)
        if n <= nburnin:
            raise ValueError # insufficient data when burn-in data is removed

        self.history       = history
        self.nburnin       = nburnin

    @classmethod
    def fromDataFile(cls, fname):
        if not os.path.exists(fname):
            return

        #param data: np.array([['sigma_sat', 'LET_th', 'W', 'S','logp']])
        data = np.loadtxt(fname)
        return cls.fromDataList(data)

    @classmethod
    def fromDataList(cls, data):
        return MCMCHistory(data)

    @classmethod
    def getPrettyLabel(cls, fmt=FmtUnicode):
        labels = [ label[fmt] for label in MCMCHistory.prettyLabels ]
        return labels

    def saveDataFile(self,fname):
        history = self.getHistory()
        np.savetxt(fname, history, fmt='%-12g', delimiter=' ')

    def size(self):
        n, _ = np.shape(self.history)
        return n

    def getHistory(self, idx=None, exclBurnin=True):
        if idx is None:
            if exclBurnin:
                return self.history[self.nburnin:, :-1]
            else:
                return self.history

        if not isinstance(idx, int):
            raise TypeError

        if exclBurnin:
            return self.history[self.nburnin:, idx]
        else:
            return self.history[:, idx]

    def getNormFactor(self, idx):
        if idx == self.iSigmaSat:
            normFactor = self.getHistory(idx)[-1]
            return normFactor
        else:
            return None

class MCMCBestFit(object):
    def __init__(self, exptXS, bestFit):
        self.exptXS = exptXS
        self.bestFit = bestFit
