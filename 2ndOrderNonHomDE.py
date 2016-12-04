import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.pylab import *
import numpy as np

"""---------------------------------------------------------------------------"""
""" CHANGE THIS DATA AND THIS DATA ONLY - if u're not completely confident """

""" Initial conditions """
v0 = 1  # velocity
x0 = 0.1  # amplitude
F0 = 10  # force

""" Time step and time domain """
end_time = 20
dt = 0.005

""" Physical properties """
m = 1  # mass
k = 10  # stiffness
w0 = np.sqrt(k / m)  # natural frequency
dfact = 0.01  # damping factor
wd = w0 * np.sqrt(1 - np.square(dfact))  # damped frequency
wf = 10  # force frequency

print('Lastna frekvenca znaša: ' + str(w0))

"""---------------------------------------------------------------------------"""

##### NABOR MOŽNIH VPRAŠANJ ZA ŠTUDENTE #####
# Kakpen pomen ima partikularni in kakšen homogeni deli
# zakaj Y apmlitutuda partikularne reštive pade ko se dviga frekvenca?

""" DO NOT CHANGE !!! """
y = []
y1 = []
y2 = []
t = []
beta = []
wfw0 = []

xNUM = []
T = []

def initialize():
    for i in range(int(end_time / dt)):
        global w0, wd, k, dfact, F0, wf

        w0 = np.sqrt(k / m)
        wd = w0 * np.sqrt(1 - dfact * dfact)
        t.append(i * dt)
        T = t[i]

        # Homogeni Del
        yh = (x0 * np.cos(wd * T) + v0 / wd * np.sin(wd * T)) * np.exp(-dfact * w0 * T)
        # Partikularni del
        X = F0 / k * np.sqrt(1 / (np.square(1 - np.square(wf / w0)) + np.square(2 * dfact * wf / w0)))
        fi = np.arctan(2 * dfact * wf / w0 / (1 - np.square(wf / w0)))
        yp = X * np.sin(wf * T - fi)
        # Sumarum
        y.append(yh)
        y1.append(yp)
        y2.append(yh + yp)
    update()


""" ~ ~ ~ End of initialization ~ ~ ~ """


def changeK(val):
    global w0, wd, k, dfact, F0, wf
    k = val
    w0 = np.sqrt(k / m)
    wd = w0 * np.sqrt(1 - dfact * dfact)
    print('lastna frekvenca: ' + str(w0))
    y.clear()
    y1.clear()
    y2.clear()
    t = []
    for i in range(int(end_time / dt)):
        t.append(i * dt)
        T = t[i]
        # Homogeni Del
        yh = (x0 * np.cos(wd * T) + v0 / wd * np.sin(wd * T)) * np.exp(-dfact * w0 * T)
        # Partikularni del
        X = F0 / k * np.sqrt(1 / (np.square(1 - np.square(wf / w0)) + np.square(2 * dfact * wf / w0)))
        fi = np.arctan(2 * dfact * wf / w0 / (1 - np.square(wf / w0)))
        yp = X * np.sin(wf * T - fi)
        # Sumarum
        y.append(yh)
        y1.append(yp)
        y2.append(yh + yp)
    update()


def changeForce(val):
    global w0, wd, k, dfact, F0, wf
    F0 = val
    w0 = np.sqrt(k / m)
    wd = w0 * np.sqrt(1 - dfact * dfact)
    print('lastna frekvenca: ' + str(w0))
    y.clear()
    y1.clear()
    y2.clear()
    t = []
    for i in range(int(end_time / dt)):
        t.append(i * dt)
        T = t[i]
        # Homogeni Del
        yh = (x0 * np.cos(wd * T) + v0 / wd * np.sin(wd * T)) * np.exp(-dfact * w0 * T)
        # Partikularni del
        X = F0 / k * np.sqrt(1 / (np.square(1 - np.square(wf / w0)) + np.square(2 * dfact * wf / w0)))
        fi = np.arctan(2 * dfact * wf / w0 / (1 - np.square(wf / w0)))
        yp = X * np.sin(wf * T - fi)
        # Sumarum
        y.append(yh)
        y1.append(yp)
        y2.append(yh + yp)

    #numerically()
    update()


def changeWf(val):
    global w0, wd, k, dfact, F0, wf
    wf = val
    w0 = np.sqrt(k / m)
    wd = w0 * np.sqrt(1 - dfact * dfact)
    print('lastna frekvenca: ' + str(w0))
    y.clear()
    y1.clear()
    y2.clear()
    t = []
    for i in range(int(end_time / dt)):
        t.append(i * dt)
        T = t[i]
        # Homogeni Del
        yh = (x0 * np.cos(wd * T) + v0 / wd * np.sin(wd * T)) * np.exp(-dfact * w0 * T)
        # Partikularni del
        X = F0 / k * np.sqrt(1 / (np.square(1 - np.square(wf / w0)) + np.square(2 * dfact * wf / w0)))
        fi = np.arctan(2 * dfact * wf / w0 / (1 - np.square(wf / w0)))
        yp = X * np.sin(wf * T - fi)
        # Sumarum
        y.append(yh)
        y1.append(yp)
        y2.append(yh + yp)
    update()


def changeDamping(val):
    global w0, wd, k, dfact, F0, wf
    dfact = val
    w0 = np.sqrt(k / m)
    wd = w0 * np.sqrt(1 - dfact * dfact)
    print('lastna frekvenca: ' + str(w0))
    y.clear()
    y1.clear()
    y2.clear()
    t = []
    for i in range(int(end_time / dt)):
        t.append(i * dt)
        T = t[i]
        # Homogeni Del
        yh = (x0 * np.cos(wd * T) + v0 / wd * np.sin(wd * T)) * np.exp(-dfact * w0 * T)
        # Partikularni del
        X = F0 / k * np.sqrt(1 / (np.square(1 - np.square(wf / w0)) + np.square(2 * dfact * wf / w0)))
        fi = np.arctan(2 * dfact * wf / w0 / (1 - np.square(wf / w0)))
        yp = X * np.sin(wf * T - fi)
        # Sumarum
        y.append(yh)
        y1.append(yp)
        y2.append(yh + yp)
    update()

def changeBeta():
    global w0, wd, k, dfact, F0, wf, beta
    print('Beta znaša: ' + str(np.sqrt(1 / (np.square(1 - np.square(wf/w0)) + np.square(2 * dfact * wf/w0)))))
    beta.clear()
    wfw0.clear()
    for i in range(1000):
        wfw0.append(0 + i * 0.003)
        beta.append(np.sqrt(1 / (np.square(1 - np.square(wfw0[i])) + np.square(2 * dfact * wfw0[i]))))

fig, ax = plt.subplots(nrows=1,ncols=2)
subplots_adjust(left=0.05,right=0.95, bottom=0.25)
line, = plot(t, y, linewidth=2, color='r')

xlabel('X - Title')
ylabel('Y - title')
title('$Our Chart$')
grid(True)

axcolor = 'lightgoldenrodyellow'
k_ax = axes([0.15, 0.15, 0.65, 0.03], axisbg=axcolor)
dfact_ax = axes([0.15, 0.12, 0.65, 0.03], axisbg=axcolor)
force_ax = axes([0.15, 0.09, 0.65, 0.03], axisbg=axcolor)
wf_ax = axes([0.15, 0.06, 0.65, 0.03], axisbg=axcolor)

k_slider = Slider(k_ax, 'togost', 0.1, 100.0, valinit=k)
dfact_slider = Slider(dfact_ax, 'faktor dušenja', 0.0, 1.0, valinit=dfact)
force_slider = Slider(force_ax, 'sila', 0.0, 10.0, valinit=F0)
wf_slider = Slider(wf_ax, 'vzbujevalna krožna fr', 1, 20.0, valinit=wf)


def update():
    plt.subplot(2, 1, 1)
    plt.cla()
    plt.plot(t, y, label='Homogeni del')
    plt.plot(t, y1, 'r', label='Partikularni del')
    plt.plot(t, y2, 'g', label='Komplementarni del - generalna resitev')
    plt.axhline(y=F0/k,xmin=t[0],xmax=t[int(end_time/dt-1)],c="purple",linestyle='--',linewidth=0.5,zorder=0,label='Kvazistaticni del')

    #plt.plot(F0/k,'yo',label='Kvazistatični del')
    #plt.plot(T, xNUM,'y' ,label='Numericni del')   #TODO NUMERIČNI DEL

    plt.xlabel('čas [s]')
    plt.ylabel('amplituda [m]')
    plt.grid()
    plt.legend(loc=1)


    changeBeta()
    plt.subplot(2, 1, 2)
    plt.cla()
    plt.plot(wfw0, beta, label='beta potek')
    plt.axvline(x=wf/w0,ymin=beta[0],ymax=beta[999],c="black",linestyle='--',label='izbrani wf/w0')
    plt.grid()
    plt.xlabel('wf/w0')
    plt.ylabel('beta')
    plt.legend(loc=1)



def numerically():
    global F0, wf, m, k, dfact, w0, x0
    #d = 2*m*dfact*

    dkr = 2 * np.sqrt(k*m)
    d = dkr * dfact
    dt = 0.0001
    T.clear()
    xNUM.clear()

    print(d)
    xNUM.append(x0)
    T.append(0)

    #x1 = (F0 * np.sin(wf * dt) * dt * dt + xNUM[0] * (2 * m - dt * dt * k) + xNUM[0] * (-m + dt * d / 2)) / (m + dt * d / 2)
    x1 = dt*v0+x0
    xNUM.append(x1)
    T.append(dt)

    for i in range(1,int(end_time / dt)-1):
        xn = (F0*np.sin(wf*dt*(i))*dt*dt+xNUM[i]*(2*m-dt*dt*k)+xNUM[i-1]*(-m+dt*d/2))/(m+dt*d/2)
        xNUM.append(xn)
        T.append(dt*i)


""" Initialize """
initialize()
#numerically()

""" Event functions defined """
k_slider.on_changed(changeK)
dfact_slider.on_changed(changeDamping)
force_slider.on_changed(changeForce)
wf_slider.on_changed(changeWf)

plt.title("Odziv sistema z eno prostostno stopnjo na harmonsko motnjo")
plt.show()