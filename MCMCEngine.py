import random
from scipy.stats import binom
from math import exp,log,sqrt
import math
import matplotlib



def norm_logpdf(x,mu,sigma_sqr):
    ''' pdf(x)=1/sqrt(2*pi*sigma_sqr) * exp(-(x-mu)*(x-mu)/(2*sigma_sqr))'''
    logp=-0.5*log(2*math.pi*sigma_sqr)-(x-mu)**2/(2*sigma_sqr)
    return logp

class Params(object):
    def __init__(self,sigma_sat=None,let0=None,lam=None,k=None,epsilon=None):
        """Constructor weibull function:sigma(let)=sigma_sat(1-exp(-((let-let0)/lam)**k) )"""
        self.sigma_sat=sigma_sat
        self.let0=let0
        self.lam=lam
        self.k=k
        self.epsilon=epsilon
        self.logp=None

    def sigma(self,let):
        if let >self.let0:
            y=self.k*log((let-self.let0)/self.lam)
            if y>300:
                return self.sigma_sat
            return self.sigma_sat*( 1 - exp(-(((let-self.let0)/self.lam)**self.k) ))
        else:
            return 0.0

class Probability(object):
    def __init__(self,data,nsram,fact=1.0):
        self.ndat=len(data)
        self.nsram=nsram
        self.data=[]
        self.fact=fact
        for i in range(len(data)):
            k=float(data[i][2])
            n=float(data[i][1]*self.nsram)
            self.data.append((data[i][0],n,k))
        #print self.data

    def logpdp(self,params):
        if isinstance(params,Params):
            ans=0.0
            for i in range(self.ndat):
                lad=params.sigma(self.data[i][0])*self.data[i][1]
                logp=norm_logpdf(self.data[i][2],lad,lad*self.fact)
                ans=ans+logp
            params.logp=ans
            return ans
        else:
            raise TypeError

class Normaldev():
    def __init__(self,seed,mu,sig):
        self.seed=seed
        self.mu=mu
        self.sig=sig
        random.seed(seed)

    def dev(self):
        while True:
            u=random.random()
            v=1.7156*(random.random()-0.5)
            x= u - 0.449871
            y = abs(v) + 0.386595
            q = x*x + y*(0.19600*y-0.25472*x)
            if not ( q>0.27597 and (q>0.27846 or (v*v) >(-4.*log(u)*u*u))):
                break
        return self.mu+self.sig*v/u

    def rand(self):
        return random.random()

class  Propose(object):
    def __init__(self,ranseed,logstep,let0Max,sigmaMin=0.0):
        """Constructor"""
        self.gau=Normaldev(ranseed,0.,1.)
        self.logstep=logstep
        self.qratio =1.
        self.let0Max=let0Max
        self.sigmaMin=sigmaMin

    def rndwalk(self,s1,s2):
        if isinstance(s1,Params) and isinstance(s2,Params):
            while True:
                s2.let0 = s1.let0*exp(self.logstep*self.gau.dev())
                if s2.let0<self.let0Max: break
            while True:
                s2.sigma_sat= s1.sigma_sat*exp(self.logstep*self.gau.dev())
                if s2.sigma_sat > 0.9*self.sigmaMin: break
            s2.lam      = s1.lam*exp(self.logstep*self.gau.dev())
            s2.k        = s1.k*exp(self.logstep*self.gau.dev())
            self.qratio = (s2.lam/s1.lam)*(s2.let0/s1.let0)*(s2.k/s1.k)*(s2.sigma_sat/s1.sigma_sat)

class Mcmc(object):
    def __init__(self, probEval):
        if not isinstance(probEval,Probability): raise TypeError
        self.probEval = probEval

        # best state and it's log10 probability
        self.bestState=None
        self.logp=None

    def step(self,m,s,propose):
        '''
        @param m: number of steps
        @param s: state
        '''
        if not isinstance(s, Params):	     raise TypeError
        if not isinstance(propose, Propose): raise TypeError
        if self.bestState is None:
            self.bestState = s
            self.logp = self.probEval.logpdp(s)

        accept=0.0
        self.probEval.logpdp(s)
        for i in xrange(m):
            sprop=Params()
            propose.rndwalk(s,sprop)
            self.probEval.logpdp(sprop)
            log=sprop.logp-s.logp

            log = min(log, 200)
            log = max(log, -200)

            rho=min( 1.,  propose.qratio*exp(log) )
            ran=propose.gau.rand()
            if (ran < rho):
                s=sprop
                if s.logp>self.logp:
                    self.bestState=s
                    self.logp=s.logp
                accept+=1
        return s,accept/m