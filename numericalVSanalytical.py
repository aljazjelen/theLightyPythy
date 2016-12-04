""" Systems imports """
from scipy.integrate import odeint
from scipy.interpolate import UnivariateSpline
import numpy as np
from timeit import default_timer as timer
from statistics import stdev
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter


""" PODATKI """
RPM = 900
engfreq = 900 / 60
drifreq = engfreq * 6 / 2
wf = drifreq * 2 *np.pi

j1 = 1.8
k1 = 2e4
c1 = 30

J = j1
k = k1
c = c1


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""                   ANALITIČNO                     """""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
beta = []
wfw0 = []
xNUM = []
T = []

dt = 0.0001
graphTime = int(np.round(2 / dt))

v0 = 1.2  # velocity
x0 = 0  # amplitude
F0 = 10  # force

print("   <<   Started solving phase   >>   ")

startTimer = timer()
def analytical(tstep,SimuSize):
    #global fiA
    global t, y, y1, y2
    GraphTime = int(np.round(2 / tstep))

    t = np.zeros(SimuSize)
    y = np.zeros(SimuSize)
    y1 = np.zeros(SimuSize)
    y2 = np.zeros(SimuSize)

    for i in range(SimuSize):
        w0 = np.sqrt(k / J)
        dfact = c / 2 / J / w0
        wd = w0 * np.sqrt(1 - dfact * dfact)
        #t.append(i * dt)
        t[i] = i * tstep
        T = t[i]
        # Homogeni Del
        yh = (x0 * np.cos(wd * T) + v0 / wd * np.sin(wd * T)) * np.exp(-dfact * w0 * T)
        # Partikularni del
        X = 500 / k * np.sqrt(1 / (np.square(1 - np.square(wf / w0)) + np.square(2 * dfact * wf / w0)))
        fi = np.arctan(2 * dfact * wf / w0 / (1 - np.square(wf / w0)))

        yp = X * np.sin(wf * T - fi + np.pi) # ZAKAJ + PI !??! TODO !?
        #yp = X * np.cos(wf * T - fi)
        # Sumarum
        y[i] = yh
        y1[i] = yp
        y2[i] = yh + yp
        len(y2)
        #y.append(yh)
        #y1.append(yp)
        #y2.append(yh + yp)

    # ANALITICAL FI


    fiA_inner = y2[GraphTime:]
    return fiA_inner

simuSize = (int(np.round(4/dt)))
t = np.zeros(simuSize)
y = np.zeros(simuSize)
y1 = np.zeros(simuSize)
y2 = np.zeros(simuSize)
fiA = analytical(dt,simuSize)

endTimer = timer()
print("   <<<   Analytical solution obtained!   >>>   ")
print("    in roughly  " + str(endTimer-startTimer) + " seconds")





""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""                   NUMERIČNO                      """""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def M(t):
    #return 300 + 500 * np.sin(wf * t)
    return 500 * np.sin(wf * t)

class ODEsolver():
    def __init__(self, J, c, k, atol, rtol, step):
        """ Model Properties """
        self.J = J
        self.c = c
        self.k = k
        """ Time Domain """
        self.tSettings = {'startTime': 0.0, 'endTime': 4,
                      'timeStep': step}
        self.tDomain = np.arange(self.tSettings['startTime'],
                             self.tSettings['endTime'], self.tSettings['timeStep'])
        """ Initial Data """
        self.initData = [0.0, 0.0]
        """ Solution """
        self.atol = atol
        self.rtol = rtol
        self.derivSolution = []
        self.derive()

    def equation(self, u, t):
        J = self.J
        k = self.k
        c = self.c
        gamma1 = u[0]
        gamma2 = u[1]
        dudt = [gamma2, 1 / J * (M(t) - c * gamma2 - k * gamma1)]
        return dudt

    def derive(self):
        self.derivSolution = odeint(self.equation, self.initData, self.tDomain, atol=self.atol, rtol=1e-5)



Atolerances = [1e-4,1e-5,1e-6,1e-7,1e-8]
num_tol = 5
Rtolerances = [1e-4,1e-5,1e-6]
simpleOneDcase = []
fiNum = []
fiDiff = []



""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""               PRIMERJAVA GRAFOV                  """""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def distributiveGraphs():
    """ Function to calculate error distribution as a function of tolerance """
    for tolerance in range(num_tol):
        startTimer = timer()
        simpleOneDcase.append(ODEsolver(J, c, k, Atolerances[tolerance], 1e-10, dt))
        # fiNum.append(simpleOneDcase[tolerance].derivSolution[int(2/simpleOneDcase[tolerance].tSettings['timeStep']):, 0])
        fiNum.append(simpleOneDcase[tolerance].derivSolution[graphTime:, 0])
        print(len(fiNum[0]))
        print(graphTime)
        print(len(fiA))
        print(len(fiNum[0]))
        fiDiff.append(np.divide(fiA - fiNum[tolerance], np.abs(fiA)))
        # fiDiff.append(np.divide(fiA - fiNum[tolerance], 1))
        print("   <<<   Numerical solution obtained!   >>>   ")
        endTimer = timer()
        print("    in roughly  " + str(endTimer - startTimer) + " seconds")

    print("Drawing graphs")
    for i in range(num_tol):
        n = len(fiDiff[i])
        print("graph " + str( i + 1) + " ...")
        s = fiDiff[i]
        p, x = np.histogram(s, bins=n)  # bin it into n = N/10 bins
        x = x[:-1] + (x[1] - x[0]) / 2  # convert bin edges to centers
        f = UnivariateSpline(x, p, s=int(n))
        plt.plot(x, f(x), label="Porazdelitev pri toleranci: " + str(Atolerances[i]))

    print("Graphs drawn")
    plt.xlabel("Reltivna razlika analitične in numerične rešitve")
    plt.ylabel("Število zadetkov v območju")
    plt.title("Graf porazdelitve absolutne razlike med numerično in analitično rešitvijo")
    plt.legend(loc=1)
    plt.grid()
    plt.show()

distributiveGraphs()


def izris_rel_grafa():
    simple1Dcase = ODEsolver(J,c,k,1e-4,1e-6,dt)
    simpleFiNum = simple1Dcase.derivSolution[graphTime:, 0]
    simpleFiDiff = np.divide(fiA - simpleFiNum,np.abs(fiA))

    n = len(simpleFiDiff)
    s = simpleFiDiff
    p, x = np.histogram(s, bins=n)
    x = x[:-1] + (x[1] - x[0]) / 2
    f = UnivariateSpline(x, p, s=int(n))

    """ PLOT ODMIK OD RAVNOVESNE ZA ANALITIČNO IN NUMERIČNO """
    def plotDifference():
        plt.subplot(2, 1, 1)
        plt.plot(t[graphTime:], simple1Dcase.derivSolution[graphTime:, 0],'ro', label='Odmik od ravnovesne lege (numerično)')
        plt.grid()
        plt.plot(t[graphTime:],y2[graphTime:],'b', label='Odmik od ravnovesne lege (analitično)')
        plt.ylabel("Odmik od ravnovesne lege [rad]")
        plt.xlabel("Čas [s]")
        plt.legend(loc=1)
        #plt.show()

    plotDifference()

    plt.subplot(2, 1, 2)
    plt.plot(x, f(x), label="Porazdelitvena funkcija - relativna razlika")
    plt.xlabel("Relativna razlika analitične in numerične rešitve")
    plt.ylabel("Število prisotnih zadetkov v območju")
    plt.ylim(0,200)
    plt.legend(loc=1)
    plt.grid()
    plt.show()


izris_rel_grafa()



def funTolDeviationGraph():
    """ Funkcija, ki izriše deviacijo numerične rešitve od analitične v odvisnosti od numerične tolerance
        'odeint' metode
    """
    Tolerances = []
    tolDevStandardDev = []
    Toltiming = []

    Tolfig, Tolax1 = plt.subplots()

    for i in range(1,5):
        sTimer = timer()
        Tolerances.append(1e-3/(i*10))
        tolDevAnaly = analytical(dt,simuSize)
        tolDev = ODEsolver(J,c,k,Tolerances[i-1],1e-6,dt)
        tolDevFi = tolDev.derivSolution[graphTime:, 0]
        #tolDevFiDiff = np.divide(fiA - tolDevFi,np.abs(fiA))
        tolDevFiDiff = tolDevAnaly - tolDevFi
        tolDevStandardDev.append(stdev(tolDevFiDiff))
        eTimer = timer()
        Toltiming.append(eTimer - sTimer)

    Tolax1.set_title('Standardna deviacija in računski čas v odvisnosti od tolerance',fontsize=20)
    Tolax1.plot(Tolerances,tolDevStandardDev,'bo',label='Standardna deviacija')
    Tolax1.set_xlabel('Numerična toleranca',fontsize=16)
    Tolax1.set_ylabel('Standardna deviacija',fontsize=16)
    Tolax1.set_xscale('log')
    Tolax1.set_yscale('log')
    Tolax1.set_xlim(min(Tolerances),max(Tolerances))

    majorFormatter = FormatStrFormatter('%3.1e')
    Tolax1.yaxis.set_major_formatter(majorFormatter)
    Tolax1.grid(which='both')

    Tolax2 = Tolax1.twinx()
    Tolax2.plot(Tolerances,Toltiming,'g',label='Računski čas')
    Tolax2.set_xlim(min(Tolerances),max(Tolerances))
    Tolax2.set_xlabel('Numerična toleranca',fontsize=16)
    Tolax2.set_ylabel('Čas računanja [s]',fontsize=16)

    lines, labels = Tolax1.get_legend_handles_labels()
    lines2, labels2 = Tolax2.get_legend_handles_labels()
    Tolax2.legend(lines + lines2, labels + labels2, loc=0)
    #Tolax2.grid(color='g', linestyle='-.')

    """ Glajenje grafa za lepši prikaz """
    n = len(tolDevStandardDev)
    f = UnivariateSpline(Tolerances, tolDevStandardDev, s=int(n))
    Tolax1.plot(Tolerances,f(Tolerances),'r')
    plt.show()


funTolDeviationGraph()


def funDtDeviationGraph():
    """ Funkcija, ki izriše deviacijo numerične rešitve od analitične v odvisnosti od časovnega koraka dt
    """
    timeSteps = []
    dtDevStandardDev = []
    dTtiming = []

    fig, ax1 = plt.subplots()

    for i in range(1,5):
        sTimer = timer()
        timeSteps.append(1e-0/i/10)
        #print(dt)
        #print(timeSteps[i-1])
        SimuSize = (int(np.round(4 / timeSteps[i-1])))
        graphTime = int(np.round(2 / timeSteps[i-1]))

        dtDevAnaly = analytical(timeSteps[i-1],SimuSize)
        dtDev = ODEsolver(J,c,k,1e-6,1e-6,timeSteps[i-1])
        dtDevFi = dtDev.derivSolution[graphTime:, 0]
        dtDevFiDiff = dtDevAnaly - dtDevFi
        dtDevStandardDev.append(stdev(dtDevFiDiff))
        eTimer = timer()
        dTtiming.append(eTimer - sTimer)

    ax1.set_title('Standardna deviacija in računski čas v odvisnosti od velikosti časovnega koraka',fontsize=20)
    ax1.plot(timeSteps,dtDevStandardDev,'bo',label='Standardna deviacija')
    ax1.set_xlabel('Časovni korak dt [s]',fontsize=16)
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_ylabel('Standardna deviacija',fontsize=16)
    ax1.set_xlim(min(timeSteps),max(timeSteps))
    ax1.grid(which='both')

    majorFormatter = FormatStrFormatter('%3.1e')
    ax1.yaxis.set_major_formatter(majorFormatter)
    #minorFormatter = FormatStrFormatter('%3.e')
    #ax1.xaxis.set_minor_formatter(minorFormatter)

    ax2 = ax1.twinx()
    ax2.plot(timeSteps,dTtiming,'g',label='Računski čas')
    ax2.set_xlabel('Časovni korak dt [s]',fontsize=16)
    ax2.set_ylabel('Čas računanja [s]',fontsize=16)
    ax2.set_xlim(min(timeSteps),max(timeSteps))

    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc=0)

    """ Glajenje grafa za lepši prikaz """
    n = len(dtDevStandardDev)
    f = UnivariateSpline(timeSteps, dtDevStandardDev, s=int(n))
    ax1.plot(timeSteps,f(timeSteps),'r')
    plt.show()

funDtDeviationGraph()