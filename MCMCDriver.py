__all__ = ['MCMCDriver']

from MCMCEngine import Params, Probability, Propose, \
     Normaldev, Mcmc, norm_logpdf
from MCMCSettings import MCMCSettings
from MCMCHistory import MCMCHistory, MCMCBestFit
import numpy as np

class MCMCDriver(object):
    def __init__(self,mcmcSettings):
        if not isinstance(mcmcSettings,MCMCSettings):
            raise TypeError

        self.settings = mcmcSettings
        self._initParams()

    def _initParams(self):
        settings = self.settings
        data     = settings.data
        nbit     = settings.nbit
        seed     = settings.seed
        logstep  = settings.logstep
        factor   = settings.factor

        self.crossSections = np.zeros((len(data), 2))

        sigma_max = 0.0
        let_min = 1e100

        for i, (let, phi, k) in enumerate(data):
            crossSection = float( k/(nbit*phi) )
            sigma_max    = max(sigma_max, crossSection)
            let_min      = min(let_min, let)

            self.crossSections[i] = (let, crossSection)

        # initial guess for the Weibull parameters
        sigma_sat = sigma_max
        lam            = 1.0
        k              = 0.5
        let0           = let_min/2
        self.state0    = Params(sigma_sat, let0, lam, k)

        # create MCMC engine objects
        self.propose=Propose(seed, logstep, let_min, sigma_sat)
        prob=Probability(data, nbit, factor)
        self.mcmc=Mcmc(prob)

    def run(self):
        settings = self.settings
        nburnin  = settings.nburnin
        nkeep    = settings.nkeep
        nskip    = settings.nskip

        history = np.empty((nburnin+nkeep, 5))
        mcmc    = self.mcmc
        propose = self.propose
        state = self.state0
        for i in xrange(nburnin):
            state, accept=mcmc.step(nskip, state, propose)
            history[i] = (state.sigma_sat, state.let0, state.lam, state.k, state.logp)
        naccept=0
        for i in xrange(nburnin, nburnin+nkeep):
            state, accept=mcmc.step(nskip, state, propose)
            history[i] = (state.sigma_sat, state.let0, state.lam, state.k, state.logp)
            naccept +=accept

        acceptRate = float(naccept)/nkeep

        mcmcHistory = MCMCHistory(history, nburnin)

        # best fitting
        bestState = mcmc.bestState
        LETs = self.crossSections[:, 0]
        nPts = 101
        fitCurve = np.zeros((nPts,2))
        for i,let in enumerate(np.linspace(min(LETs), max(LETs), 101)):
            fitCurve[i,:] = (let, bestState.sigma(let))

        bestFit = MCMCBestFit(self.crossSections, fitCurve)

        return mcmcHistory, bestFit, acceptRate
