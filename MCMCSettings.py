__all__ =['MCMCSettings']


class MCMCSettings(object):
    '''This class stores the MCMC settings
    '''
    __slots__ = [
                 'data',    'nbit',
                 'nburnin', 'nkeep',
                 'nskip',   'seed',
                 'logstep', 'factor',
                 'bitUnit'
                ]

    def __init__(self, data = [], nbit = 1,nburnin = 1000,
                 nkeep = 2000, nskip = 10, seed = 1010,
                 logstep = 0.004, factor = 1.1,  bitUnit = 'Mb'):
        self.data    = data
        self.nbit    = nbit
        self.nburnin = nburnin
        self.nkeep   = nkeep
        self.nskip   = nskip
        self.seed    = seed
        self.logstep = logstep
        self.factor  = factor
        self.bitUnit = bitUnit

    def __getattr__(self, key):
        return key
